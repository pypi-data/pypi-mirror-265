
from ode.use_case_decorator import UseCaseDecorator
import threading

class UseCaseDispatcher:
    def __init__(self, use_case, execute_on=None, result_on=None):
        self.decorator = DispatcherDecorator(use_case, execute_on, result_on)

    def dispatch(self, param=None):
        return self.decorator.dispatch(param)

class DispatcherDecorator(UseCaseDecorator):
    def __init__(self, use_case, execute_on=None, result_on=None):
        super().__init__(use_case)
        self.execute_on = execute_on
        self.result_on = result_on

    def dispatch(self, param=None):
        return threading.Thread(target=self.process, args=(param,)).start()

    def on_error(self, error):
        threading.Thread(target=lambda: self.use_case.on_error(error)).start()

    def on_result(self, output):
        threading.Thread(target=lambda: self.use_case.on_result(output)).start()