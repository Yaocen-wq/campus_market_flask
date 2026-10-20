# BUG_015 重复邮箱注册被拦，提示却写「用户名已存在」
- **模块**：注册
- **严重程度**：中
- **优先级**：P2
- **涉及用例**：注册唯一性校验
- **测试方法**：错误推测法 + 数据构造
- **发现日期**：2026-09-20
- **状态**：已修复，回归通过
---
**复现步骤**
  1. 运行 app.py
  2. Postman 打开注册请求，方法 POST，地址 http://127.0.0.1:5000/register
  3. Body 选 x-www-form-urlencoded：username 填全新值（huang_test_04），email 填已存在邮箱（t99@school.edu），phone 填 13800138099
  4. 点 Send

**预期结果**  
按实际冲突字段给提示：邮箱重复应提示「邮箱已存在」；用户名重复才提示用户名已存在

**实际结果**  
返回 code 1，提示「注册失败：用户名已存在」；SQL 查库无 huang_test_04，实际冲突字段是 email

**原因**  
register() 的 except pymysql.err.IntegrityError 不区分冲突字段，提示写死「用户名已存在」；users 表 email 建有唯一索引，撞邮箱唯一索引时也报这一句
---
**修复建议**  
捕获 IntegrityError 后按报错信息区分冲突字段（username / email），返回对应提示；