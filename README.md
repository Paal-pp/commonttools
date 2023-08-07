# commontools

commontools 是一个用于常用数据库操作、日志设置等功能的 Python 库。

## 功能

- MySQL 数据库连接和查询(包含重试系统)
- 日志记录和配置
- 其他实用工具（待开发）

## 安装

使用以下命令从 GitHub 安装：

```bash
pip install git+https://github.com/username/mylibrary.git
```
## 快速入门
```python
from commontools import MySQLConnection

conn = MySQLConnection('localhost', 'user', 'pass', 'mydb')
results = conn.query('SELECT * FROM mytable')
```

更多使用示例，请查看 文档。

## 要求
Python 3.6+
pymysql

## 贡献
如果你有好的意见或建议，欢迎提 issue 或者提交 pull request。

## 许可
该项目基于 MIT 许可证。