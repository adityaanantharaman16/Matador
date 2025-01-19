import logging
import json
from datetime import datetime
from typing import Any, Dict, Optional, Union, List
from functools import wraps
import traceback
import os
from logging.handlers import RotatingFileHandler, TimedRotatingFileHandler

class MatadorLogger:
    LOG_LEVELS = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    def __init__(self, app_name: str = 'MATADOR', log_level: str = 'INFO'):
        self.app_name = app_name
        self.logger = logging.getLogger(app_name)
        self.logger.setLevel(self.LOG_LEVELS.get(log_level, logging.INFO))

        # Create logs directory if it doesn't exist
        if not os.path.exists('logs'):
            os.makedirs('logs')

        self._setup_handlers()

    def _setup_handlers(self):
        """Setup logging handlers for console, file, and error logs"""
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

        # Console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Main log file handler with rotation
        file_handler = RotatingFileHandler(
            'logs/matador.log',
            maxBytes=10 * 1024 * 1024,  # 10MB
            backupCount=5
        )
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)

        # Error log file handler with daily rotation
        error_handler = TimedRotatingFileHandler(
            'logs/errors.log',
            when='midnight',
            interval=1,
            backupCount=30
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(formatter)
        self.logger.addHandler(error_handler)

    def _format_message(self,
                        message: str,
                        user_id: Optional[str] = None,
                        extra_data: Optional[Dict] = None) -> str:
        """Format log message with consistent structure"""
        log_data = {
            'timestamp': datetime.utcnow().isoformat() + 'Z',
            'message': message,
            'user_id': user_id,
            'app_name': self.app_name
        }

        if extra_data:
            log_data.update(extra_data)

        return json.dumps(log_data)

    # User-related logging
    def log_user_action(self,
                        action: str,
                        user_id: str,
                        details: Optional[Dict] = None,
                        level: str = 'INFO'):
        """Log user-related actions (profile updates, follows, etc.)"""
        message = self._format_message(
            f"User Action: {action}",
            user_id=user_id,
            extra_data={
                'action_details': details,
                'action_type': 'user',
            }
        )
        self.logger.log(self.LOG_LEVELS[level], message)

    def log_karma_update(self,
                         user_id: str,
                         karma_type: str,
                         old_value: float,
                         new_value: float,
                         reason: str):
        """Log karma changes"""
        message = self._format_message(
            f"Karma Update: {karma_type}",
            user_id=user_id,
            extra_data={
                'karma_type': karma_type,
                'old_value': old_value,
                'new_value': new_value,
                'change': new_value - old_value,
                'reason': reason
            }
        )
        self.logger.info(message)

    # Pitch-related logging
    def log_pitch_event(self,
                        event_type: str,
                        pitch_id: str,
                        user_id: str,
                        pitch_type: str,  # 'stock' or 'crypto'
                        details: Optional[Dict] = None,
                        level: str = 'INFO'):
        """Log pitch-related events (creation, updates, performance)"""
        message = self._format_message(
            f"Pitch Event: {event_type}",
            user_id=user_id,
            extra_data={
                'pitch_id': pitch_id,
                'pitch_type': pitch_type,
                'event_details': details
            }
        )
        self.logger.log(self.LOG_LEVELS[level], message)

    def log_pitch_interaction(self,
                              pitch_id: str,
                              user_id: str,
                              interaction_type: str,  # 'like', 'comment', 'share'
                              details: Optional[Dict] = None):
        """Log user interactions with pitches"""
        message = self._format_message(
            f"Pitch Interaction: {interaction_type}",
            user_id=user_id,
            extra_data={
                'pitch_id': pitch_id,
                'interaction_type': interaction_type,
                'interaction_details': details
            }
        )
        self.logger.info(message)

    # API and Performance logging
    def log_api_call(self,
                     api_name: str,
                     endpoint: str,
                     response_time: float,
                     status: str,
                     details: Optional[Dict] = None,
                     level: str = 'INFO'):
        """Log external API calls (YahooFinance, CoinGecko)"""
        message = self._format_message(
            f"API Call: {api_name}",
            extra_data={
                'endpoint': endpoint,
                'response_time': response_time,
                'status': status,
                'details': details
            }
        )
        self.logger.log(self.LOG_LEVELS[level], message)

    def log_performance_metric(self,
                               metric_name: str,
                               value: Any,
                               user_id: Optional[str] = None,
                               details: Optional[Dict] = None):
        """Log performance metrics"""
        message = self._format_message(
            f"Performance Metric: {metric_name}",
            user_id=user_id,
            extra_data={'value': value, 'details': details}
        )
        self.logger.info(message)

    # Error logging
    def log_error(self,
                  error: Exception,
                  user_id: Optional[str] = None,
                  context: Optional[Dict] = None):
        """Log errors with full context"""
        message = self._format_message(
            f"Error: {str(error)}",
            user_id=user_id,
            extra_data={
                'error_type': error.__class__.__name__,
                'stack_trace': traceback.format_exc(),
                'context': context
            }
        )
        self.logger.error(message)

def log_function_call(logger: MatadorLogger):
    """Decorator for logging function calls"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            try:
                result = func(*args, **kwargs)
                execution_time = (datetime.now() - start_time).total_seconds()

                logger.logger.debug(
                    logger._format_message(
                        f"Function call: {func.__name__}",
                        extra_data={
                            'execution_time': execution_time,
                            'status': 'success'
                        }
                    )
                )
                return result
            except Exception as e:
                execution_time = (datetime.now() - start_time).total_seconds()
                logger.log_error(
                    e,
                    context={
                        'function': func.__name__,
                        'execution_time': execution_time,
                        'args': str(args),
                        'kwargs': str(kwargs)
                    }
                )
                raise

        return wrapper
    return decorator

# Example usage
if __name__ == "__main__":
    logger = MatadorLogger()

    # Example logging pitch event
    logger.log_pitch_event(
        event_type="create",
        pitch_id="stock_pitch_123",
        user_id="user_456",
        pitch_type="stock",
        details={
            "symbol": "AAPL",
            "thesis": "Strong Q4 earnings expected",
            "pitch_price": 150.00
        }
    )

    # Example logging karma update
    logger.log_karma_update(
        user_id="user_456",
        karma_type="stockKarma",
        old_value=100,
        new_value=120,
        reason="Successful pitch performance"
    )