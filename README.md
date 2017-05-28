[![Build Status](https://travis-ci.org/mligus/cloudwatch-handlers.svg?branch=master)](https://travis-ci.org/mligus/cloudwatch-handlers)


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
$ vagrant up
```

Provision includes required Ubuntu packages installation (Python 3.6, etc.) and will set up 
Python virtual environment with all requirements from `requirements.txt`.


### Requirements

File `requirements-to-freeze.txt` contains initial library requirements without versions.
To install development requirements you may use 

```
$ pip install -r requirements.txt
```


### Configure AWS CLI

AWS CLI will be configured and accessed via Vagrant box, so first of all login to box 
and activate Python virtual environment:

```
$ vagrant ssh
$ source venv/bin/activate
$ cd /vagrant
```

Check that AWS CLI is accessible (Vagrant should install it from `requirements.txt`):

```
$ aws --version
aws-cli/1.11.93 Python/3.6.1 Linux/4.4.0-78-generic botocore/1.5.56
```

After you'll have to configure AWS CLI accrding to [manual](http://docs.aws.amazon.com/cli/latest/userguide/cli-chap-getting-started.html).

```
$ aws configure
AWS Access Key ID [none]: <your AWS access key> 
AWS Secret Access Key [none]: <your AWS secret access key>
Default region name [none]: us-east-1
Default output format [none]: json
```

Check that AWS is accessible via CLI:

```
$ aws ec2 describe-instances
{
    "Reservations": []
}
```

All your AWS configuration is stored in `~/.aws/config` and `~/.aws/credentials` on Vagrant box.


### Tools

1. [isort](https://pypi.python.org/pypi/isort) to sort Python imports automatically.
