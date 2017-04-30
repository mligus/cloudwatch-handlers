# AWS CloudWatch logging handlers

This library contains custom Python logging handlers for AWS CloudWatch services.

## Handlers

### CloudWatch Logs

Send logs to [AWS CloudWatch Logs](https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#logs:)

#### Example

```
import logging

from cloudwatch_handlers import CloudWatchLogsHanlder

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

cwh = CloudWatchLogsHandler(group='test')
cwh.setFormatter(formatter)

logger.addHandler(cwh)

logger.debug('debug message')
logger.info('info message')
logger.warn('warn message')
logger.error('error message')
logger.critical('critical message')
```
