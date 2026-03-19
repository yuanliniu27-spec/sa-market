# 客户意向分析演示 Skill

## 功能说明

这是一个演示用的 Skill，用于展示如何开发和发布应用到 SA Market。

## 使用方法

```python
from main import analyze_customer_intent

result = analyze_customer_intent("CUST001")
print(result)
# 输出: {'intent_score': 75, 'stage': 'consideration', ...}
```

## 输入参数

- `customer_id` (必填): 客户ID

## 输出结果

```json
{
  "intent_score": 75,
  "stage": "consideration",
  "message": "Customer CUST001 analysis completed"
}
```

## 依赖项

无

## 测试

```bash
python main.py
```
