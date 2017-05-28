"""This module contains logging handlers for CloudWatch Logs service

Following restriction applies when handler sends logs to service:

  * The maximum batch size is 1,048,576 bytes (size is calculated as the sum
    of all event messages in UTF-8, plus 26 bytes for each log event).
  * None of the log events in the batch can be more than 2 hours in the future.
  * None of the log events in the batch can be older than 14 days or
    the retention period of the log group.
  * The log events in the batch must be in chronological ordered by their
    timestamp (the time the event occurred, expressed as the number of
    milliseconds since Jan 1, 1970 00:00:00 UTC).
  * The maximum number of log events in a batch is 10,000.
  * A batch of log events in a single request cannot span more than 24 hours.
    Otherwise, the operation fails.

Those restrctions are discribed in AWS CloudWatch Logs
`documentation <http://docs.aws.amazon.com/AmazonCloudWatchLogs/
latest/APIReference/API_PutLogEvents.html>`_.
"""


import datetime
import logging

import boto3

from . import exceptions

MAX_PUT_SIZE = 1048576
MAX_PUT_COUNT = 10000
EVENT_META_SIZE = 26
DEFAULT_EVENT_ENCODING = 'utf-8'
DEFAULT_BUFFER_CAPACITY = 10


def deafult_stream_name():
    return datetime.date.today().strftime('%Y-%m-%d')


class CloudWatchLogsHandler(logging.Handler):

    def __init__(self, group,
                 stream=None, capacity=None, retain_days=None,
                 *args, **kwargs):
        """Initialize CloudWatch Logs handler

        :param group: name of the log group
        :param stream: name of the stream (if empty current date will be used)
        :param capacity: handler's buffer capacity
        :param retain_days: number of days to retain logs for in group
        """
        # Initialize base logging handler
        super(self.__class__, self).__init__(*args, **kwargs)
        self._client = boto3.client('logs')
        self._buffer = []
        self._buffer_size = 0
        self._max_capacity = capacity or DEFAULT_BUFFER_CAPACITY
        if self._max_capacity > MAX_PUT_COUNT or self._max_capacity < 0:
            raise ValueError(
                'Maximum capacity not in range 0 ... ' + str(MAX_PUT_COUNT))
        self._group = group
        self._stream = stream
        self._ensure_group(self._group, retain_days)

    def _ensure_group(self, group, retain_days=None):
        """Check presence or create CloudWatch Logs log group

        .. note::
            If group already present retantion policy won't be updated.

        :param group: name of log group
        :param retain_days: retention policy in days for current group

        :raises LogsHandlerError: on group creation failure
        """
        client = self._client
        group_found = False
        next_token = None
        # Try to get log group (check presence)
        while True:
            if next_token is None:
                r = client.describe_log_groups(logGroupNamePrefix=group)
            else:
                r = client.describe_log_groups(logGroupNamePrefix=group,
                                               nextToken=next_token)
            for group_meta in r['logGroups']:
                if group_meta['logGroupName'] == group:
                    group_found = True
                    break
            if group_found:
                break
            elif r.get('nextToken'):
                next_token = r.get('nextToken')
            else:
                break
        # Create log group if not found
        if not group_found:
            r = client.create_log_group(logGroupName=group)
            if r['ResponseMetadata']['HTTPStatusCode'] == 400:
                raise exceptions.LogsHandlerError(str(r))
            if retain_days:
                r = client.put_retention_policy(
                    logGroupName=group,
                    retentionInDays=int(retain_days))
                if r['ResponseMetadata']['HTTPStatusCode'] == 400:
                    raise exceptions.LogsHandlerError(str(r))

    def _ensure_stream(self, group, stream):
        """Checks for existance or create log stream

        :param group: name of the log group
        :param stream: name of the stream

        :raises LogsHandlerError: on stream creation failure

        :return: next upload sequence
        """
        # Try to get stream or create it if not found
        client = self._client
        next_token = None
        stream_found = False
        while True:
            if next_token is None:
                r = client.describe_log_streams(
                    logGroupName=group,
                    logStreamNamePrefix=stream,
                )
            else:
                r = client.describe_log_streams(
                    logGroupName=group,
                    logStreamNamePrefix=stream,
                    nextToken=next_token
                )
            for stream_meta in r['logStreams']:
                if stream_meta['logStreamName'] == stream:
                    stream_found = True
                    next_sequence = stream_meta.get('uploadSequenceToken', '0')
                    break
            if stream_found:
                break
            elif r.get('nextToken'):
                next_token = r.get('nextToken')
            else:
                break
        if not stream_found:
            r = client.create_log_stream(
                logGroupName=group,
                logStreamName=stream,
            )
            if r['ResponseMetadata']['HTTPStatusCode'] == 400:
                raise exceptions.LogsHandlerError(str(r))
            else:
                next_sequence = '0'
        return next_sequence

    def _format_event(self, record, suffix=' ...',
                      encoding=DEFAULT_EVENT_ENCODING):
        """Format log record as CloudWatch Logs event


        This method will check record size and truncate if it exceeds API
        call size limit. ``LogRecord`` creation time will be used as
        a timestamp for event.

        If ``suffix`` is provided it will be added to the end of message
        in case if message is truncated.
        Default ``suffix`` is `` ...``.

        :param msg: log record
        :param suffix: string to be added at the end of truncated message
        :param encoding: encoding to use

        :return: size of event in bytes and event message dictionary
        :rtype: tuple
        """
        byte_limit = MAX_PUT_SIZE - EVENT_META_SIZE
        msg = self.format(record)
        msg = msg.encode(encoding)
        if len(msg) > byte_limit:
            byte_limit -= len(suffix)
            msg = msg[:byte_limit] + suffix
        else:
            msg = msg[:byte_limit]
        size = len(msg) + EVENT_META_SIZE
        msg = msg.decode(encoding, 'ignore')
        event = {
            'timestamp': int(record.created * 1000),
            'message': msg,
        }
        return (size, event)

    def emit(self, record):
        """Store event in a buffer and flush buffer if needed

        Buffer will be flushed if capacity is reached or
        size exceeds maximum API call size.

        :param record: log record
        """
        buffer_filled = len(self._buffer) >= self._max_capacity
        buffer_oversized = self._buffer_size >= MAX_PUT_SIZE
        if buffer_filled or buffer_oversized:
            self.flush()
        size, event = self._format_event(record)
        self._buffer.append(event)
        self._buffer_size += size

    def flush(self):
        """Flush events from buffer to CloudWatch Logs stream

        :raises LogsHandlerError: if events rejected or no response from API
        """
        if not self._buffer:
            return
        stream = self._stream or deafult_stream_name()
        next_sequence = self._ensure_stream(self._group, stream)
        r = self._client.put_log_events(
            logGroupName=self._group,
            logStreamName=stream,
            logEvents=self._buffer,
            sequenceToken=next_sequence,
        )
        if r.get('rejectedLogEventsInfo'):
            raise exceptions.LogsHandlerError(
                'This events are rejected: ' + str(r['rejectedLogEventsInfo'])
            )
        elif r:
            self._buffer = []
            self._buffer_size = 0
        else:
            raise exceptions.LogsHandlerError(
                'CloudWatch Logs API call response is empty')

    def close(self):
        """Flush buffer and close the handler."""
        try:
            self.flush()
        finally:
            super(self.__class__, self).close()
