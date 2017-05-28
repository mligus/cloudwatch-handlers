"""This module is a simple usage example of CloudWatch hanlders"""

import logging

from cloudwatch_handlers import CloudWatchLogsHandler

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')

cwh = CloudWatchLogsHandler(group='test', retain_days=3)
cwh.setFormatter(formatter)

logger.addHandler(cwh)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
