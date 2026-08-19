import logging
from config import settings

class HealthCheckFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool: #expected to return a boolean value. if it returns True, the log record will be processed and written to the log file. if it returns False, the log record will be ignored and not written to the log file.
        # Exclude health check logs from the log file
        return "/health" not in record.getMessage()

# Logging configuration class
class LoggingConfig:
    LOGGING = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': {
            # Simple formatter for regular logs
            'simple': {
                'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                "use_colors": True
            },
            # Detailed formatter for logs with additional information like filename, function, and line number
            'large': {
                'format':
                    '%(asctime)s - %(levelname)s - %(filename)s - %(funcName)s - Line:  %(lineno)d: %(message)s',
            },
            # Formatter used for access logs (e.g., HTTP access logs)
            "access": {
                "()": "uvicorn.logging.AccessFormatter",
                "fmt": '%(asctime)s :: %(client_addr)s - %(levelname)s - "%(request_line)s" %(status_code)s',
                "use_colors": False
            },
        },
        'filters': {
            'notHealthCheckFilter': {
                '()': HealthCheckFilter,
            }
        },
        'handlers': {
            'console': {
                'level': 'INFO',
                'class': 'logging.StreamHandler',
                'formatter': 'simple',
            },
            'file_logger': {
                'level': 'INFO',
                'class': 'logging.FileHandler',
                'filename': settings.log_file,
                'formatter': 'large',
            },
            "access": {
                "formatter": "access",
                "class": "logging.StreamHandler",
                'filters': ['notHealthCheckFilter']
            },
            "access_file": {
                "formatter": "access",
                'class': 'logging.FileHandler',
                'filename': settings.log_file,
                'filters': ['notHealthCheckFilter']
            },
        },
        'loggers': {
            '': {
                'handlers': ['console', 'file_logger'],
                'level': 'DEBUG',
                'propagate': False,
            },
            "uvicorn.access": {
                "handlers": ["access", "access_file"],
                "level": "INFO",
                "propagate": False
            },
        }
    }

    @staticmethod
    def get_log_config():
        return LoggingConfig.LOGGING
