#!/usr/bin/env python
# -*- coding:utf-8 -*-
from utils.config import Config,LOG_PATH
from logging.handlers import TimedRotatingFileHandler
import logging
import os


class Logger(object):
    def __init__(self, logger_name='framework'):
        self.logger = logging.getLogger(logger_name)
        logging.root.setLevel(logging.NOTSET)
        conf = Config().get('log')
        self.log_file_name = conf.get('file')
        self.backup_count = conf.get('backup_count')
        self.console_level = conf.get('console_level')
        self.file_out_level = conf.get('file_out_level')
        pattern = conf.get('pattern')
        self.formatter = logging.Formatter(pattern)

    def get_logger(self):
        if not self.logger.handlers:
            console_handler = logging.StreamHandler()
            console_handler.setLevel(self.console_level)
            console_handler.setFormatter(self.formatter)
            self.logger.addHandler(console_handler)

            file_handler = TimedRotatingFileHandler(filename=os.path.join(LOG_PATH, self.log_file_name),
                                                    when='D',
                                                    interval=1,
                                                    backupCount=self.backup_count,
                                                    delay=True,
                                                    encoding='utf-8'
                                                    )
            file_handler.setLevel(self.file_out_level)
            file_handler.setFormatter(self.formatter)
            self.logger.addHandler(file_handler)
        return self.logger


logger = Logger().get_logger()


