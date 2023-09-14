import logging
from logging.handlers import TimedRotatingFileHandler
import os
from datetime import datetime

class Logger:
    # 用于存储已创建的日志实例的字典
    _instances = {}

    # 定义日志格式
    FORMAT = '%(asctime)s - %(levelname)s - %(message)s - %(process)s - {%(pathname)s:%(lineno)d}'

    # 使用__new__方法来实现多例模式，每个app_name只创建一个实例
    def __new__(cls, app_name, *args, **kwargs):
        if app_name not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[app_name] = instance
        return cls._instances[app_name]

    def __init__(self, app_name, log_dir='logs', level=logging.INFO):
        """
        使用应用名称初始化日志器。
        :param app_name: 应用的名称
        :param log_dir: 存储日志文件的目录。默认为 'logs'
        :param level: 日志的级别。默认为 logging.INFO
        """
        # 检查是否已经初始化以避免重复初始化
        if hasattr(self, '_initialized'):
            return

        # 创建logger实例并设置级别
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(level)

        # 确保日志目录存在
        os.makedirs(log_dir, exist_ok=True)

        # 定义日志文件的名称和路径
        log_file = os.path.join(log_dir, f'{app_name}_{datetime.now().strftime("%Y-%m-%d")}.log')

        # 定义日志格式
        formatter = logging.Formatter(self.FORMAT)

        # 设置控制台流处理器
        stream_handler = logging.StreamHandler()
        stream_handler.setLevel(level)
        stream_handler.setFormatter(formatter)

        # 设置文件处理器，保存日志文件并每天轮替
        file_handler = TimedRotatingFileHandler(log_file, when='midnight', interval=1, backupCount=31)
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)

        # 将处理器添加到日志实例中
        self.logger.addHandler(stream_handler)
        self.logger.addHandler(file_handler)

        # 标记为已初始化
        self._initialized = True

    def get_logger(self):
        """
        获取日志记录器实例。
        :return: 日志记录器实例
        """
        return self.logger

    def close(self):
        """
        关闭所有的处理器，确保日志被正确写入文件。
        """
        for handler in self.logger.handlers:
            handler.close()
            self.logger.removeHandler(handler)
