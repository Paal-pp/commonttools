import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

class Logger:
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(process)s - {%(pathname)s:%(lineno)d}'

    def __init__(self, app_name, log_dir='logs', level=logging.INFO):
        """
        使用应用名称初始化日志器。
        :param app_name: 应用的名称
        :param log_dir: 存储日志文件的目录。默认为 'logs'
        :param level: 日志的级别。默认为 logging.INFO
        """
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(level)

        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)

        log_file = os.path.join(log_dir, f'{app_name}_{datetime.now().strftime("%Y-%m-%d")}.log')

        formatter = logging.Formatter(self.FORMAT)

        # 控制台记录的流处理器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)

        # 文件处理器，保存日志文件并每天轮替
        file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=31)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # 将处理器添加到日志记录器中
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

    def get_logger(self):
        """
        获取日志记录器实例。
        :return: 日志记录器实例
        """
        return self.logger

    def close(self):
        """关闭所有的处理器，确保日志被写入文件。"""
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)

# 示例使用
app_log = Logger('my_app_name', level=logging.DEBUG)
logger = app_log.get_logger()
logger.info('这是一条测试日志消息。')
app_log.close()
