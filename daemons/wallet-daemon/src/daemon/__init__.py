import abc


class BaseDaemon(abc.ABC):
    core: core.BaseDaemonCore

    @abc.abstractmethod
    async def handle(self):
        pass

    @abc.abstractmethod
    async def processing_block(self):
        pass

    @abc.abstractmethod
    async def processing_transaction(self):
        pass

    @abc.abstractmethod
    async def send(self):
        pass

    @abc.abstractmethod
    async def run(self):
        pass


class TronDaemon(BaseDaemon):
    core = core.TronDaemonCore

    def __init__(self):
        pass

    async def handle(self):
        pass

    async def processing_transaction(self):
        pass

    async def run(self):
        pass
