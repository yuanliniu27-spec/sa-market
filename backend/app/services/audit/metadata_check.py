import json
import re
import zipfile
from typing import Dict, List, Any


class MetadataValidator:
    """Validator for manifest.json in uploaded packages"""

    REQUIRED_FIELDS = ['type', 'name', 'version', 'description', 'category']
    SKILL_REQUIRED_FIELDS = ['skill_id', 'input_schema', 'output_schema']
    AGENT_REQUIRED_FIELDS = ['agent_id', 'skills']

    def validate(self, zip_path: str) -> Dict[str, Any]:
        """Validate manifest.json in zip file"""
        issues = []

        try:
            with zipfile.ZipFile(zip_path, 'r') as zf:
                # Check manifest.json exists
                if 'manifest.json' not in zf.namelist():
                    return {
                        'status': 'failed',
                        'issues': [{
                            'severity': 'high',
                            'type': 'missing_manifest',
                            'description': '缺少 manifest.json 文件'
                        }]
                    }

                # Parse manifest
                try:
                    manifest_content = zf.read('manifest.json').decode('utf-8')
                    manifest = json.loads(manifest_content)
                except json.JSONDecodeError as e:
                    return {
                        'status': 'failed',
                        'issues': [{
                            'severity': 'high',
                            'type': 'invalid_json',
                            'description': f'manifest.json 格式错误: {str(e)}'
                        }]
                    }

                # Validate fields
                issues.extend(self._validate_required_fields(manifest))
                issues.extend(self._validate_version(manifest))
                issues.extend(self._validate_type_specific(manifest))

        except Exception as e:
            return {
                'status': 'failed',
                'issues': [{
                    'severity': 'high',
                    'type': 'validation_error',
                    'description': f'验证失败: {str(e)}'
                }]
            }

        status = 'failed' if any(i['severity'] == 'high' for i in issues) else 'passed'

        return {
            'status': status,
            'issues': issues,
            'manifest': manifest if status == 'passed' else None
        }

    def _validate_required_fields(self, manifest: dict) -> List[Dict[str, Any]]:
        """Check required fields"""
        issues = []

        for field in self.REQUIRED_FIELDS:
            if field not in manifest:
                issues.append({
                    'severity': 'high',
                    'type': 'missing_field',
                    'field': field,
                    'description': f'缺少必填字段: {field}'
                })

        return issues

    def _validate_version(self, manifest: dict) -> List[Dict[str, Any]]:
        """Validate version format (semver)"""
        issues = []

        if 'version' in manifest:
            version = manifest['version']
            if not re.match(r'^\d+\.\d+\.\d+$', version):
                issues.append({
                    'severity': 'high',
                    'type': 'invalid_version',
                    'description': f'版本号格式错误: {version}，应为 x.y.z'
                })

        return issues

    def _validate_type_specific(self, manifest: dict) -> List[Dict[str, Any]]:
        """Validate type-specific fields"""
        issues = []

        app_type = manifest.get('type')

        if app_type == 'skill':
            for field in self.SKILL_REQUIRED_FIELDS:
                if field not in manifest:
                    issues.append({
                        'severity': 'high',
                        'type': 'missing_skill_field',
                        'field': field,
                        'description': f'Skill 类型必须包含字段: {field}'
                    })

        elif app_type == 'agent':
            for field in self.AGENT_REQUIRED_FIELDS:
                if field not in manifest:
                    issues.append({
                        'severity': 'high',
                        'type': 'missing_agent_field',
                        'field': field,
                        'description': f'Agent 类型必须包含字段: {field}'
                    })

            # Check skills array
            if 'skills' in manifest:
                if not isinstance(manifest['skills'], list) or len(manifest['skills']) == 0:
                    issues.append({
                        'severity': 'high',
                        'type': 'invalid_skills',
                        'description': 'Agent 必须包含至少 1 个 Skill'
                    })

        return issues
