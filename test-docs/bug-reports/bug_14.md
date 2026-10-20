# BUG_014 注册接口参数缺失直接 500
- **模块**：注册接口（Flask 版）
- **严重程度**：中
- **优先级**：P2
- **涉及用例**：接口健壮性（新场景）
- **测试方法**：错误推测法
- **发现日期**：2026-09-19
- **状态**：已修复，回归通过
---
**复现步骤**
  1. 运行 app.py
  2. Postman 打开注册请求，方法 POST，地址 http://127.0.0.1:5000/register
  3. Body 选 x-www-form-urlencoded，取消 password 这一行的勾选，其余字段正常填
  4. 点 Send

**预期结果**  
返回 code 1 与密码不能为空，服务器正常响应

**实际结果**  
HTTP 500 Internal Server Error，报错页显示 TypeError: object of type 'NoneType' has no len()

**原因**  
参数缺失时 request.form.get() 返回 None；代码先判断 password == ""（None 不等于空字符串，判断通过），下一句 len(password) 对 None 求长度抛异常。CLI 版键盘输入必有值，仅接口版出现
---
**修复建议**  
取参后先判空再校验长度，如 if password is None or password == "": 返回密码不能为空