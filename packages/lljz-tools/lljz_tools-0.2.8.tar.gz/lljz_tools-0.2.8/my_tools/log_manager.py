# coding=utf-8

import logging
import os.path
import sys
from logging.handlers import TimedRotatingFileHandler

import colorlog

from my_tools.color import Color


class LogManager:

    def __init__(self, log_name, level=logging.DEBUG, formatter: str = None, to_console=True, console_colors=None,
                 log_file: str =None,
                 # log_file='/pythonlog/out.log',
                 file_formatter: str = None, file_level=None,
                 error_log_file: str = None, error_level=logging.ERROR
                 ):
        def _init_log_file_path(default_path):
            if 'PYTHONPATH' in os.environ:
                python_path = os.environ['PYTHONPATH']
                log_path = os.path.join(python_path, 'logs')
                if not os.path.exists(log_path):
                    os.mkdir(path=log_path)
                return log_path
            print(Color.yellow(f'没有指定PYTHONPATH环境变量，使用默认路径：{default_path}'))
            return default_path

        if not formatter:
            formatter = '%(asctime)s.%(msecs)03d - %(name)s - "%(pathname)s:%(lineno)d" - ' \
                        '%(levelname)s - %(funcName)s : %(message)s'
        if not file_formatter:
            file_formatter = formatter
        self._colors = console_colors or {}
        self.formatter = '%(log_color)s' + formatter
        self._file_formatter = file_formatter
        if not file_level:
            file_level = level
        self._log_file = os.path.join(_init_log_file_path('/pythonlog'), 'out.log') if not log_file else log_file
        self._error_log_file = os.path.join(_init_log_file_path('/pythonlog'), 'error.log') if not error_log_file else error_log_file
        self._file_level = file_level
        self._error_file_level = error_level
        logging.root.setLevel(logging.NOTSET)
        self._logger = logging.getLogger(log_name)
        self._logger.setLevel(level)

        self._to_console = to_console
        self._console = to_console


    @staticmethod
    def _make_dir(path):
        parent_dir = os.path.dirname(os.path.abspath(path))
        if not os.path.exists(parent_dir):
            os.makedirs(parent_dir)

    def get_logger(self):
        if self._logger.handlers:
            return self._logger
        if self._to_console:
            colors = {
                'DEBUG': 'white',  # cyan white green black
                'INFO': 'blue',
                'WARNING': 'yellow',
                'ERROR': 'red',
                'CRITICAL': 'purple',
            }
            colors.update(self._colors)
            # 输出到控制台
            console_formatter = colorlog.ColoredFormatter(
                fmt=self.formatter,
                datefmt='%Y-%m-%d %H:%M:%S',
                log_colors=colors,
            )
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.DEBUG)
            console_handler.setFormatter(console_formatter)
            self._logger.addHandler(console_handler)
            console_handler.close()
        if self._log_file:
            # 输出到文件
            file_formatter = logging.Formatter(
                fmt=self._file_formatter,
                datefmt='%Y-%m-%d  %H:%M:%S'
            )
            self._make_dir(self._log_file)
            file_handler = TimedRotatingFileHandler(
                filename=self._log_file,
                when='midnight',
                interval=1,
                backupCount=10,
                encoding='utf8',
                delay=True
            )
            # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
            file_handler.setLevel(self._file_level)
            file_handler.setFormatter(file_formatter)
            self._logger.addHandler(file_handler)
            file_handler.close()
        if self._error_log_file:
            # 输出到文件
            file_formatter = logging.Formatter(
                fmt=self._file_formatter,
                datefmt='%Y-%m-%d %H:%M:%S'
            )
            self._make_dir(self._error_log_file)
            error_file_handler = TimedRotatingFileHandler(
                filename=self._error_log_file,
                when='midnight',
                interval=1,
                backupCount=10,
                encoding='utf8',
                delay=True
            )
            # 日志级别，logger 和 handler以最高级别为准，不同handler之间可以不一样，不相互影响
            error_file_handler.setLevel(self._error_file_level)
            error_file_handler.setFormatter(file_formatter)
            self._logger.addHandler(error_file_handler)
            error_file_handler.close()

        return self._logger


if __name__ == '__main__':

    logger2 = LogManager("my log").get_logger()

    logger2.debug("Hello World")
    logger2.info("Hello World")
    logger2.warning("Hello World")
    logger2.error("Hello World")
    logger2.critical("Hello World")
