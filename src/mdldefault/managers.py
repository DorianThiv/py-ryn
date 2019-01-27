
from bases import BaseManager
from mdldefault.specifics.commands import DefaultBaseCommand
from mdldefault.operators import DefaultOperator
from mdldefault.registries import DefaultRegistry
from mdldefault.specifics.exceptions import DefaultCommandError

class DefaultManager(BaseManager):

    def __init__(self, mod):
        super().__init__(mod, DefaultBaseCommand())

        self.operator = DefaultOperator(self)
        self.registry = DefaultRegistry()

        def emit(self, data):
            try:
                super().emit(data)
            except DefaultCommandError as e:
                data.payload = e.message
                data.binder.write(data)
            except Exception as e:
                print("[ERROR - DEFAULT - OPERATOR - UPDATE] : {} : {}".format(sys.exc_info()[-1].tb_lineno, e)) 
                self.logger.log(0, "Default operator: (error: {}, data: {})".format(e, data))    		