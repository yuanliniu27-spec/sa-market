# SA Market 应用清单规范

所有上传到 SA Market 的应用都必须包含 `manifest.json` 文件，位于 zip 包的根目录。

## Skill 类型清单

```json
{
  "type": "skill",
  "skill_id": "customer-intent-analysis",
  "name": "客户意向分析",
  "version": "1.0.0",
  "description": "基于客户沟通记录、行为数据，自动评估客户购车意向度",
  "category": "客户管理",
  "tags": ["CRM", "AI", "数据分析"],
  "icon_url": "https://example.com/icon.png",

  "input_schema": {
    "type": "object",
    "properties": {
      "customer_id": {
        "type": "string",
        "description": "客户ID"
      },
      "days": {
        "type": "integer",
        "description": "分析天数",
        "default": 7
      }
    },
    "required": ["customer_id"]
  },

  "output_schema": {
    "type": "object",
    "properties": {
      "intent_score": {
        "type": "integer",
        "description": "意向度分数 (0-100)"
      },
      "stage": {
        "type": "string",
        "description": "客户阶段"
      },
      "next_action": {
        "type": "string",
        "description": "建议的下一步动作"
      }
    }
  },

  "dependencies": [
    {
      "skill_id": "nlp-understanding",
      "version": ">=1.0.0"
    }
  ],

  "compatibility": {
    "min_salesagent_version": "1.0.0"
  },

  "author": {
    "name": "张三",
    "email": "zhangsan@lixiang.com",
    "department": "市场营销-营销系统"
  }
}
```

## Agent 类型清单

```json
{
  "type": "agent",
  "agent_id": "inventory-manager",
  "name": "库存管理助手",
  "version": "1.0.0",
  "description": "自动化库存查询、预测和预警",
  "category": "供应链",
  "tags": ["库存", "自动化", "预测"],

  "skills": [
    {
      "skill_id": "inventory-query",
      "version": ">=1.0.0"
    },
    {
      "skill_id": "stock-forecast",
      "version": "^2.1.0"
    },
    {
      "skill_id": "low-stock-alert",
      "version": "~1.5.0"
    }
  ],

  "compatibility": {
    "min_salesagent_version": "1.0.0"
  },

  "author": {
    "name": "李四",
    "email": "lisi@lixiang.com",
    "department": "供应链管理"
  }
}
```

## 字段说明

### 通用字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `type` | string | ✅ | 应用类型：`skill` 或 `agent` |
| `name` | string | ✅ | 应用名称 |
| `version` | string | ✅ | 版本号（遵循 semver） |
| `description` | string | ✅ | 功能描述 |
| `category` | string | ✅ | 分类 |
| `tags` | array | ❌ | 标签数组 |
| `icon_url` | string | ❌ | 图标 URL |
| `author` | object | ❌ | 作者信息 |
| `compatibility` | object | ❌ | 兼容性要求 |

### Skill 特定字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `skill_id` | string | ✅ | Skill 唯一标识 |
| `input_schema` | object | ✅ | 输入参数 JSON Schema |
| `output_schema` | object | ✅ | 输出结果 JSON Schema |
| `dependencies` | array | ❌ | 依赖的其他 Skills |

### Agent 特定字段

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `agent_id` | string | ✅ | Agent 唯一标识 |
| `skills` | array | ✅ | 包含的 Skills 列表（至少 1 个） |

## 版本号格式

遵循语义化版本（Semver）：`MAJOR.MINOR.PATCH`

依赖版本约束：
- `1.0.0` - 精确版本
- `>=1.0.0` - 大于等于
- `^1.2.0` - 兼容版本（允许 1.x.x，不允许 2.0.0）
- `~1.2.3` - 补丁版本（允许 1.2.x，不允许 1.3.0）

## 文件结构示例

```
my-skill.zip
├── manifest.json          # 必需：应用清单
├── main.py                # 主代码文件
├── requirements.txt       # Python 依赖
├── README.md              # 使用文档
├── tests/                 # 测试文件
│   └── test_main.py
└── data/                  # 数据文件（如有）
    └── model.pkl
```

## 审核检查项

上传后自动进行以下检查：

1. **元数据完整性**：必填字段是否完整
2. **版本号格式**：是否符合 semver 规范
3. **依赖关系**：依赖的 Skills 是否存在
4. **代码安全**：是否包含危险代码
5. **功能测试**：基本导入和运行测试

## 最佳实践

- ✅ 清晰的命名和描述
- ✅ 完善的输入输出 schema
- ✅ 合理的版本依赖约束
- ✅ 包含测试用例
- ✅ 提供使用文档

- ❌ 硬编码密钥或密码
- ❌ 使用危险函数（os.system, eval 等）
- ❌ 依赖未发布的 Skills
- ❌ 过于宽松的依赖版本约束
