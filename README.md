https://travis-ci.org/mligus/cloudwatch-handlers.svg?branch=master

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


## Development Environment

All testing and code execution is done on Vagrant box.
By default [ubuntu/xenial64](https://atlas.hashicorp.com/ubuntu/boxes/xenial64/) box is used.

To start and provision the run:

```
vagrant up
```

Provision includes required Ubuntu packages installation (Python 3.6, etc.) and will set up 
Python virtual environment with all requirements from `requirements.txt`.


### Requirements

File `requirements-to-freeze.txt` contains initial library requirements without versions.
To install development requirements you may use 

```
pip install -r requirements.txt
```
