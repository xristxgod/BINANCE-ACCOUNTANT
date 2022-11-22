import src.settings as settings
import gateway.gate.base as base

from gateway.schemas import BlockSchema


class Node(base.AbstractNode):
    network_name = 'tron'
    endpoint_uri = settings.TRON_GATE_URL

    class SmartContract:
        @classmethod
        async def connect(cls):
            pass

    def __init__(self):
        from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

        self.node = AsyncTron(provider=AsyncHTTPProvider(endpoint_uri=self.endpoint_uri))

    async def get_block(self, block_number: int) -> BlockSchema:
        response = await self.node.get_block(block_number)

