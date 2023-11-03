#!/usr/bin/env python3
import re


def filter_datum(fields, redaction, message, separator):
    pattern = """r'{}(?!{})'.format(separator,
            separator.join(map(re.escape, fields)))"""
    return re.sub(pattern, redaction, message)
