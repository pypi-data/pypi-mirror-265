import datetime
import errno
import os
import signal
import time
from functools import wraps

from typing import Any


class TimeoutException(Exception):
    pass


class ApiServiceException(Exception):
    """Api error"""

    def __init__(self, message: str, extra_info: dict[str, Any] | None = None) -> None:
        super().__init__(message)
        self.extra_info = extra_info


# пример обработки:
# try:
#     raise ApiServiceException("Произошла ошибка", {"code": 400, "time": "12:34"})
# except ApiServiceException as e:
#     print(f"Сообщение об ошибке: {e}")
#     print(f"Дополнительная информация: {e.extra_info}")


def retry(num_retries, exception_to_check, sleep_time=0):
    """Decorator that retries the execution of a function if it raises a specific exception."""

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            exc = None
            for i in range(1, num_retries + 1):
                try:
                    return func(*args, **kwargs)
                except exception_to_check as e:
                    exc = e
                    if isinstance(e, ApiServiceException):
                        print(f"{func.__name__} raised: {e}, extra_info: {e.extra_info}")
                    else:
                        print(f"{func.__name__} raised {e.__class__.__name__}. Retrying...")
                    if i < num_retries:
                        time.sleep(sleep_time)
            raise exc

        return wrapper

    return decorate


def timeout(seconds, error_message=os.strerror(errno.ETIME)):
    """Декоратор, который возбуждает исключение если функция выполняется дольше заданного промежутка времени"""

    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutException(error_message)

        @wraps(func)
        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wrapper

    return decorator


def get_prev_week_mon_sun(dt: datetime.date | None = None) -> dict[str, datetime.date]:
    """Получим дату пн и вс предыдущей недели к переданной дате (если ничего не передано, тогда от текущей даты).
    Пример вывода: {'monday': datetime.date(2023, 12, 25), 'sunday': datetime.date(2023, 12, 31)}
    """
    if dt is None:
        dt = datetime.date.today()
    monday = dt - datetime.timedelta(days=dt.isoweekday() - 1, weeks=1)
    sunday = dt - datetime.timedelta(days=dt.isoweekday())
    return {"monday": monday, "sunday": sunday}


# assert get_prev_week_mon_sun(datetime.date(2024, 1, 4)) == {'monday': datetime.date(2023, 12, 25), 'sunday': datetime.date(2023, 12, 31)}
# assert get_prev_week_mon_sun(datetime.date(2024, 1, 1)) == {'monday': datetime.date(2023, 12, 25), 'sunday': datetime.date(2023, 12, 31)}
# assert get_prev_week_mon_sun(datetime.date(2024, 1, 22)) == {'monday': datetime.date(2024, 1, 15), 'sunday': datetime.date(2024, 1, 21)}
# assert get_prev_week_mon_sun(datetime.date(2024, 1, 21)) == {'monday': datetime.date(2024, 1, 8), 'sunday': datetime.date(2024, 1, 14)}
# assert get_prev_week_mon_sun(datetime.date(2024, 1, 26)) == {'monday': datetime.date(2024, 1, 15), 'sunday': datetime.date(2024, 1, 21)}
# assert get_prev_week_mon_sun(datetime.date(2024, 5, 28)) == {'monday': datetime.date(2024, 5, 20), 'sunday': datetime.date(2024, 5, 26)}
