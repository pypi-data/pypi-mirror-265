from typing import Type, Callable, Tuple, Optional, Any
from inspect import iscoroutinefunction
from functools import wraps
from types import TracebackType

from emptylog import LoggerProtocol

from escape.errors import SetDefaultReturnValueForContextManagerError


class Wrapper:
    def __init__(self, default: Any, exceptions: Tuple[Type[BaseException], ...], logger: LoggerProtocol, success_callback: Callable[[], Any]) -> None:
        self.default: Any = default
        self.exceptions: Tuple[Type[BaseException], ...] = exceptions
        self.logger: LoggerProtocol = logger
        self.success_callback: Callable[[], Any] = success_callback

    def __call__(self, function: Callable[..., Any]) -> Callable[..., Any]:
        @wraps(function)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = None
            success_flag = False

            try:
                result = function(*args, **kwargs)
                success_flag = True

            except self.exceptions as e:
                exception_massage = '' if not str(e) else f' ("{e}")'
                self.logger.exception(f'When executing function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was suppressed.')
                result = self.default

            except BaseException as e:
                exception_massage = '' if not str(e) else f' ("{e}")'
                self.logger.exception(f'When executing function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was not suppressed.')
                raise e

            if success_flag:
                self.run_success_callback()

            return result


        @wraps(function)
        async def async_wrapper(*args: Any, **kwargs: Any) -> Any:
            result = None
            success_flag = False

            try:
                result = await function(*args, **kwargs)
                success_flag = True

            except self.exceptions as e:
                exception_massage = '' if not str(e) else f' ("{e}")'
                self.logger.exception(f'When executing coroutine function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was suppressed.')
                result = self.default

            except BaseException as e:
                exception_massage = '' if not str(e) else f' ("{e}")'
                self.logger.exception(f'When executing coroutine function "{function.__name__}", the exception "{type(e).__name__}"{exception_massage} was not suppressed.')
                raise e

            if success_flag:
                self.run_success_callback()

            return result


        if iscoroutinefunction(function):
            return async_wrapper
        return wrapper

    def __enter__(self) -> 'Wrapper':
        if self.default is not None:
            raise SetDefaultReturnValueForContextManagerError('You cannot set a default value for the context manager. This is only possible for the decorator.')

        return self

    def __exit__(self, exception_type: Optional[Type[BaseException]], exception_value: Optional[BaseException], traceback: Optional[TracebackType]) -> bool:
        if exception_type is not None:
            exception_massage = '' if not str(exception_value) else f' ("{exception_value}")'

            for muted_exception_type in self.exceptions:
                if issubclass(exception_type, muted_exception_type):
                    self.logger.exception(f'The "{exception_type.__name__}"{exception_massage} exception was suppressed inside the context.')
                    return True
            self.logger.exception(f'The "{exception_type.__name__}"{exception_massage} exception was not suppressed inside the context.')

        else:
            self.run_success_callback()

        return False

    def run_success_callback(self) -> None:
        try:
            self.success_callback()
        except self.exceptions as e:
            exception_massage = '' if not str(e) else f' ("{e}")'
            self.logger.exception(f'When executing the callback ("{self.success_callback.__name__}"), the exception "{type(e).__name__}"{exception_massage} was suppressed.')
        except BaseException as e:
            exception_massage = '' if not str(e) else f' ("{e}")'
            self.logger.error(f'When executing the callback ("{self.success_callback.__name__}"), the exception "{type(e).__name__}"{exception_massage} was not suppressed.')
            raise e
