#!/usr/bin/env python3
import re


class LogFilter:
    def __init__(self, fields):
        self.fields = fields

    def filter_datum(self, redaction, message, separator):
        pattern = r'({})(?={}|$)'.format('|'.join(map(re.escape, self.fields)), re.escape(separator))
        return re.sub(pattern, redaction, message)

    def format(self, message, separator):
        redaction = 'REDACTED'
        return self.filter_datum(redaction, message, separator)
