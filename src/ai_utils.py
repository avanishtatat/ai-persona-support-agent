import time 
from collections.abc import Callable 
from typing import Any

TEMPORARY_AI_ERRORS = [
    "503",
    "unavailable",
    "high demand",
    "rate limit",
    "quota",
    "deadline exceeded",
    "internal server error",
    "resource exhausted",
    "service unavailable",
]

def is_temporary_ai_error(err: Exception) -> bool:
    """
    Check if the error is a temporary AI error based on its message.
    """
    error_text = str(err).lower()

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
            return func(*args, **kwargs)
        except Exception as error:
            last_error = error
            if is_temporary_ai_error(error) and attempt < retries - 1:
                delay = initial_delay * (2 ** attempt)
                time.sleep(delay)
                continue
            
            raise 

    raise last_error