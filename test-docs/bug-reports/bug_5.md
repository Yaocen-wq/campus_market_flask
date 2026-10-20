# BUG_005 发布商品缺 title 参数直接 500
- **模块**：发布商品
- **严重程度**：中
- **优先级**：P2
- **涉及用例**：接口健壮性
- **测试方法**：错误推测法 + 数据构造
- **发现日期**：2026-09-21
- **状态**：已修复
---
**复现步骤**
  1. 运行 app.py
  2. Postman 打开发布商品请求，方法 POST，地址 http://127.0.0.1:5000/publish_product
  3. Body 选 x-www-form-urlencoded：取消 title 一行的勾选，description、price、category 正常填
  4. 点 Send

**预期结果**  
返回 code 1 与请输入商品名，服务器正常响应

**实际结果**  
HTTP 500 Internal Server Error，报错页显示 AttributeError: 'NoneType' object has no attribute 'strip'

**原因**  
title 缺失时 request.form.get("title") 返回 None；代码直接执行 title.strip() 判空，None 没有 strip，抛异常。
---
**修复建议**  
取参后先判空再校验：if title is None or title.strip() == "": 返回请输入商品名；发布接口四个字段、注册接口四个字段一并排查.
