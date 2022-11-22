from typing import Optional

import src.settings as settings
import src.daemon.block as block


class BaseNode:
    gate_url: str

    block_manager: Optional[block.BaseBlockManager]


class TronNode(BaseNode):

    gate_url = settings.TRON_GATE_URL

    block_manager = block.TronBlockManager

    def __init__(self):
        from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

        self.gate = AsyncTron(provider=AsyncHTTPProvider(endpoint_uri=self.gate_url))

        self.block_controller = self.block_manager(gate=self.gate)

    def reconnect(self):
        pass

    @property
    def node(self):
        return self.gate

    @property
    def block(self) -> block.BaseBlock:
        return self.block_controller

    @property
    def transaction(self):
        raise NotImplemented
