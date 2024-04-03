from abc import abstractmethod
from typing import TypeVar, Optional
from ode.use_case import UseCase
from ode.output import Output
import asyncio

P = TypeVar('P')
R = TypeVar('R')


class UseCaseDecorator(UseCase[P, R]):
    def __init__(self, use_case: UseCase[P, R]):
        self.use_case = use_case

    def on_error(self, error: Exception):
        self.use_case.on_error(error)

    def execute(self, param: Optional[P] = None) -> Output[R]:
        return self.use_case.execute(param)

    def on_result(self, output: Output[R]):
        self.use_case.on_result(output)

    def guard(self, param: Optional[P] = None) -> bool:
        return self.use_case.guard(param)

class UseCaseDispatcher:
    def __init__(
        self,
        use_case: UseCase[P, R],
        execute_on: asyncio.AbstractEventLoop = None,
        result_on: asyncio.AbstractEventLoop = None
    ):
        self.decorator = self.DispatcherDecorator(use_case, execute_on, result_on)

    async def dispatch(self, param: Optional[P] = None):
        return self.decorator.dispatch(param)

    class DispatcherDecorator(UseCaseDecorator[P, R]):
        def __init__(
            self,
            use_case: UseCase[P, R],
            execute_on: asyncio.AbstractEventLoop = None,
            result_on: asyncio.AbstractEventLoop = None
        ):
            super().__init__(use_case)
            self.execute_on = execute_on
            self.result_on = result_on

        async def dispatch(self, param: Optional[P] = None):
            return asyncio.create_task(self.process(param), loop=self.execute_on)

        async def on_error(self, error: Exception):
            asyncio.to_thread(self.use_case.on_error, error, loop=self.result_on)

        async def on_result(self, output: Output[R]):
            asyncio.to_thread(self.use_case.on_result, output, loop=self.result_on)
