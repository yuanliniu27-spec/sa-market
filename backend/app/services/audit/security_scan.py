import ast
import re
import zipfile
from typing import Dict, List, Any


class SecurityScanner:
    """Security scanner for uploaded code packages"""

    DANGEROUS_FUNCTIONS = [
        'os.system',
        'subprocess.call',
        'subprocess.Popen',
        'subprocess.run',
        'eval',
        'exec',
        '__import__',
        'compile',
        'pickle.loads',
        'marshal.loads'
    ]

    DANGEROUS_IMPORTS = [
        'os',
        'subprocess',
        'socket',
    ]

    ALLOWED_IMPORTS = [
        'requests',
        'json',
        'datetime',
        'typing',
        'pydantic'
    ]

    def scan(self, zip_path: str) -> Dict[str, Any]:
        """Scan zip file for security issues"""
        issues = []

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                for filename in zf.namelist():
                    if filename.endswith('.py'):
                        code = zf.read(filename).decode('utf-8')
                        file_issues = self._scan_code(code, filename)
                        issues.extend(file_issues)
        except Exception as e:
            return {
                'status': 'failed',
                'issues': [{
                    'severity': 'high',
                    'type': 'scan_error',
                    'description': f'Failed to scan zip: {str(e)}'
                }]
            }

        # Determine status
        has_high_risk = any(issue['severity'] == 'high' for issue in issues)
        status = 'failed' if has_high_risk else 'passed'

        return {
            'status': status,
            'issues': issues
        }

    def _scan_code(self, code: str, filename: str) -> List[Dict[str, Any]]:
        """Scan Python code for security issues"""
        issues = []

        try:
            tree = ast.parse(code)
        except SyntaxError as e:
            return [{
                'severity': 'high',
                'type': 'syntax_error',
                'file': filename,
                'line': e.lineno,
                'description': f'Syntax error: {e.msg}'
            }]

        # Check dangerous function calls
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                func_name = self._get_function_name(node)
                if func_name in self.DANGEROUS_FUNCTIONS:
                    issues.append({
                        'severity': 'high',
                        'type': 'dangerous_function',
                        'file': filename,
                        'line': node.lineno,
                        'description': f'检测到危险函数调用: {func_name}'
                    })

            # Check dangerous imports
            if isinstance(node, ast.Import):
                for alias in node.names:
                    if alias.name in self.DANGEROUS_IMPORTS:
                        if alias.name not in self.ALLOWED_IMPORTS:
                            issues.append({
                                'severity': 'medium',
                                'type': 'dangerous_import',
                                'file': filename,
                                'line': node.lineno,
                                'description': f'导入了敏感模块: {alias.name}'
                            })

        # Check for hardcoded secrets
        secret_patterns = [
            (r'(password|passwd|pwd)\s*=\s*["\'][^"\']+["\']', 'password'),
            (r'(secret|secret_key|api_key)\s*=\s*["\'][^"\']+["\']', 'api_key'),
            (r'(token|auth_token)\s*=\s*["\'][^"\']+["\']', 'token'),
        ]

        for pattern, secret_type in secret_patterns:
            matches = re.finditer(pattern, code, re.IGNORECASE)
            for match in matches:
                line_num = code[:match.start()].count('\n') + 1
                issues.append({
                    'severity': 'high',
                    'type': 'hardcoded_secret',
                    'file': filename,
                    'line': line_num,
                    'description': f'检测到硬编码的 {secret_type}'
                })

        return issues

    def _get_function_name(self, node: ast.Call) -> str:
        """Extract function name from AST Call node"""
        if isinstance(node.func, ast.Name):
            return node.func.id
        elif isinstance(node.func, ast.Attribute):
            if isinstance(node.func.value, ast.Name):
                return f"{node.func.value.id}.{node.func.attr}"
        return ""
