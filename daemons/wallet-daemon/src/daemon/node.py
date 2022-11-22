from typing import Type

import src.settings as settings
import src.daemon.block as block
import src.daemon.transaction as transaction


class BaseNode:
    gate_url: str

    block_manager: Type[block.BaseBlockManager]
    transaction_manager: Type[transaction.BaseTransactionManager]

    def __init__(self, **kwargs):
        self.block_controller = self.block_manager(gate=kwargs.get('gate'))
        self.transaction_controller = self.transaction_manager(gate=kwargs.get('gate'))


class TronNode(BaseNode):

    gate_url = settings.TRON_GATE_URL

    block_manager = block.TronBlockManager
    transaction_manager = transaction.TronTransactionManager

    def __init__(self, **kwargs):
        from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

        self.gate = AsyncTron(provider=AsyncHTTPProvider(endpoint_uri=self.gate_url))

        super(TronNode, self).__init__(gate=self.gate, **kwargs)

    def reconnect(self):
        pass

    @property
    def node(self):
        return self.gate

    @property
    def block(self) -> block.BaseBlockManager:
        return self.block_controller

    @property
    def transaction(self) -> transaction.BaseTransactionManager:
        return self.transaction_controller
