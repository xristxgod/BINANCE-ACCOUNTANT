import src.settings as settings


class BaseNode:
    gate_url: str


class TronNode(BaseNode):

    gate_url = settings.TRON_GATE

    def __init__(self):
        from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

        self.gate = AsyncTron(provider=AsyncHTTPProvider(endpoint_uri=self.gate_url))

    def reconnect(self):
        pass

    @property
    def node(self):
        return self.gate
