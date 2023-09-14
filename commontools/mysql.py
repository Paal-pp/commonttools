import pymysql
from pymysql.cursors import DictCursor
from commontools.logger import Logger
import time

class MySQLConnection:
    def __init__(self, host, user, passwd, db, port=3306, charset='utf8'):
        mysql_log = Logger('mysql')
        self.logger = mysql_log.get_logger()
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.conn = None
        self._connect()

    def _connect(self):
        retry_count = 3
        while retry_count > 0:
            try:
                self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd,
                                            db=self.db, port=self.port, charset=self.charset,
                                            cursorclass=pymysql.cursors.DictCursor)
                self.logger.info("数据库连接成功")
                return True
            except pymysql.Error as e:
                self.logger.error("数据库连接失败: " + str(e))
                retry_count -= 1
                time.sleep(2)
        return False

    def _ensure_connection(self):
        if self.conn is None or not self.conn.open:
            self.logger.info("数据库连接断开，尝试重新连接")
            self._connect()

    def query(self, sql, params=None):
        try:
            self._ensure_connection()
            with self.conn.cursor() as cursor:
                cursor.execute(sql, params)
                results = cursor.fetchall()
                return results
        except pymysql.Error as e:
            self.logger.error("查询异常: " + str(e))
            return None

    def insert(self, sql, params=None):
        try:
            self._ensure_connection()
            with self.conn.cursor() as cursor:
                res = cursor.execute(sql, params)
                self.conn.commit()
                return res
        except pymysql.Error as e:
            self.conn.rollback()
            self.logger.error("插入异常: " + str(e))
            return False

    def close(self):
        if self.conn and self.conn.open:
            self.conn.close()
        self.logger.info("数据库连接已关闭")
        self.logger.close()
