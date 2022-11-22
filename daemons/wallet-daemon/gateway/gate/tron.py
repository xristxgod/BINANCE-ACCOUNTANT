import src.settings as settings
import gateway.gate.base as base


class Node(base.BaseNode):
    gate_url = settings.TRON_GATE_URL

    def __init__(self):
        from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

        self.node = AsyncTron(provider=AsyncHTTPProvider(endpoint_uri=self.gate_url))

    def get_latest_block_number(self) -> base.DefaultBlock:
        pass

    def get_latest_block(self):
        pass


class GateClient(base.BaseGateClient):

    cls_node = Node

    def __init__(self, **kwargs):
        self.logger: object

        super(GateClient, self).__init__(**kwargs)
