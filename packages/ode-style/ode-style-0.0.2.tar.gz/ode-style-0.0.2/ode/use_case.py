from abc import ABC
from typing import TypeVar, Generic
from ode.output import Output
from ode.error_output import ErrorOutput

P = TypeVar('P')
R = TypeVar('R')

class UseCase(ABC, Generic[P, R]):

    def execute(self, param: P = None) -> Output[R]:
        pass

    def process(self, param: P = None):
        try:
            if self.guard(param):
                result = self.execute(param)
                self.on_result(result)
            else:
                self.on_guard_error()
        except Exception as error:
            self.on_error(error)

    def on_error(self, error: Exception):
        self.on_result(ErrorOutput(error))

    def on_result(self, output: Output[R]):
        pass

    def guard(self, param: P = None) -> bool:
        return True

    def on_guard_error(self):
        pass
