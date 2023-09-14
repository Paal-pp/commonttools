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
# mysql 类使用方法
from commontools import MySQLConnection

def test_mysql_connection():
    # 使用你的MySQL的信息初始化
    db = MySQLConnection(host='localhost', user='your_username', passwd='your_password', db='testdb')

    # 插入数据
    db.insert("INSERT INTO sample_table (name) VALUES (%s)", ('John',))
    db.insert("INSERT INTO sample_table (name) VALUES (%s)", ('Jane',))

    # 查询数据
    results = db.query("SELECT * FROM sample_table")
    for row in results:
        print(row)

    # 结束操作后，记得关闭数据库连接
    db.close()

if __name__ == '__main__':
    test_mysql_connection()

```

```python
#looger 类使用方法

# 示例使用
app_log1 = Logger('app1')
logger1 = app_log1.get_logger()
logger1.info('这是app1的一条测试日志消息。')

app_log2 = Logger('app2')
logger2 = app_log2.get_logger()
logger2.info('这是app2的一条测试日志消息。')

app_log1_again = Logger('app1')
logger1_again = app_log1_again.get_logger()
logger1_again.info('这是app1的另一条测试日志消息。')

app_log1.close()
app_log2.close()

```

更多使用示例，请查看 文档。

## 要求
Python 3.6+
pymysql

## 贡献
如果你有好的意见或建议，欢迎提 issue 或者提交 pull request。

## 许可
该项目基于 MIT 许可证。