#!/usr/bin/env python3
import os
import logging
import re
import mysql.connector


# Define a constant for PII fields
PII_FIELDS = ('name', 'email', 'phone', 'ssn', 'password')

# Define a custom formatter that redacts PII fields
class RedactingFormatter(logging.Formatter):
    def format(self, record):
        message = super().format(record)
        for field in PII_FIELDS:
            message = re.sub(rf'{field}=\S+', f'{field}=REDACTED', message)
        return message

# Create a logger with the specified configuration
def get_logger():
    logger = logging.getLogger("user_data")
    logger.setLevel(logging.INFO)
    logger.propagate = False

    handler = logging.StreamHandler()
    handler.setFormatter(RedactingFormatter())

    logger.addHandler(handler)

    return logger

# Define the filter_datum function to obfuscate log messages
def filter_datum(fields, redaction, message, separator):
    pattern = r'({})(?={}|$)'.format('|'.join(map(re.escape, fields)), re.escape(separator))
    return re.sub(pattern, redaction, message)

# Implement the LogFilter class with format method
class LogFilter:
    def __init__(self, fields):
        self.fields = fields

    def format(self, message, separator):
        redaction = 'REDACTED'
        return filter_datum(self.fields, redaction, message, separator)

# Create a function to get a database connection
def get_db():
    db_username = os.getenv('PERSONAL_DATA_DB_USERNAME', 'root')
    db_password = os.getenv('PERSONAL_DATA_DB_PASSWORD', '')
    db_host = os.getenv('PERSONAL_DATA_DB_HOST', 'localhost')
    db_name = os.getenv('PERSONAL_DATA_DB_NAME')

    try:
        connection = mysql.connector.connect(
            user=db_username,
            password=db_password,
            host=db_host,
            database=db_name
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None

# Implement the main function
def main():
    # Get a database connection
    db_connection = get_db()
    if db_connection:
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM users")
        rows = cursor.fetchall()

        # Create a logger
        logger = get_logger()

        # Log each row with PII redacted
        for row in rows:
            log_message = ', '.join([f'{field}={value}' for field, value in zip(PII_FIELDS, row)])
            logger.info(LogFilter(PII_FIELDS).format(log_message, ', '))

        db_connection.close()

if __name__ == '__main__':
    main()
