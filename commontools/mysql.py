import pymysql
from pymysql.cursors import DictCursor

class MySQLConnection:
    def __init__(self,  host, user, passwd,
                 db, port=3306, charset='utf8',logger='logger'):
        self.logger = logger
        self.host = host
        self.user = user
        self.passwd = passwd
        self.db = db
        self.port = port
        self.charset = charset
        self.conn = None
        self.cursor = None
        self._connect()

    def _connect(self):
        try:
            self.conn = pymysql.connect(host=self.host, user=self.user, password=self.passwd,
                                        db=self.db, port=self.port, charset=self.charset,
                                        cursorclass=pymysql.cursors.DictCursor)
            self.logger.info("数据库连接成功")
            return True
        except pymysql.Error as e:
            self.logger.info("数据库连接失败: " + str(e))
            return False

    def _ensure_connection(self):
        if self.conn is None or not self.conn.open:
            self.logger.info("数据库连接断开，尝试重新连接")
            self._connect()

    def query(self, sql):
        try:
            self._ensure_connection()
            self.cursor = self.conn.cursor()
            self.cursor.execute(sql)
            results = self.cursor.fetchall()
            return results
        except pymysql.Error as e:
            self.logger.info("查询异常: " + str(e))
            return None

    def insert(self, sql):
        try:
            self._ensure_connection()
            self.cursor = self.conn.cursor()
            res = self.cursor.execute(sql)
            self.conn.commit()
            return res
        except pymysql.Error as e:
            self.conn.rollback()
            self.logger.info("插入异常: " + str(e))
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        self.logger.info("数据库连接已关闭")