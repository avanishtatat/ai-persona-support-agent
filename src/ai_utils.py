import re
import time 
from collections.abc import Callable 
from typing import Any

TEMPORARY_AI_ERRORS = [
    "503",
    "unavailable",
    "high demand",
    "rate limit",
    "deadline exceeded",
    "internal server error",
    "resource exhausted",
]

def get_retry_delay(err: Exception, fallback_delay: int) -> int:
    error_text = str(err).lower()

    match = re.search(r"retrydelay.*?(\d+)s", error_text)
    if match:
        return int(match.group(1)) + 1

    match = re.search(r"please retry in (\d+)s", error_text)
    if match:
        return int(match.group(1)) + 1

    return fallback_delay

def is_temporary_ai_error(err: Exception) -> bool:
    """
    Check if the error is a temporary AI error based on its message.
    """
    error_text = str(err).lower()

    if "quota exceeded" in error_text :
        return False  # These are not considered temporary errors for retry purposes

    return any(keyword in error_text for keyword in TEMPORARY_AI_ERRORS)


def retry_ai_call(
        func: Callable[..., Any],
        *args: Any,
        retries: int = 3,
        initial_delay: int = 2,
        **kwargs: Any
) -> Any:
    """
    Retries an AI function on temporary errors with exponential backoff.
    """

    last_error = None

    for attempt in range(retries):
        try: 
            result = func(*args, **kwargs)
            return result
        except Exception as error:
            last_error = error
            if is_temporary_ai_error(error) and attempt < retries - 1:
                fallback_delay = initial_delay * (2 ** attempt)
                delay = get_retry_delay(error, fallback_delay)
                
                time.sleep(delay)
                continue
            
            raise 

    raise last_error