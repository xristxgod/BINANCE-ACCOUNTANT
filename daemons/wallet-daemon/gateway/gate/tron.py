import logging
from typing import NoReturn, List

import src.settings as settings
import gateway.gate.base as base


class BlockManager(base.BaseBlockManager):
    file_path = settings.BLOCKS_DIR + 'tron_block.txt'

    def __init__(self, gate, *args, **kwargs):
        from tronpy.async_tron import AsyncTron

        self.gate: AsyncTron = gate

        super(BlockManager, self).__init__(*args, **kwargs)

    async def get_block_by_id(self, block: int) -> List[base.DefaultBlock]:
        block = await self.gate.get_block(block)
        # Packed
        ...

    async def get_block_now(self) -> int:
        return await self.gate.get_latest_block_number()

    async def get_block_in_storage(self) -> int:
        block_number = await self.manager.read()
        if block_number:
            return int(block_number)
        return await self.get_block_now()

    async def save_block_to_storage(self, block: int) -> NoReturn:
        return await self.manager.write(block=block)


class TransactionManager(base.BaseTransactionManager):
    pass


class Node(base.BaseNode):

    gate_url = settings.TRON_GATE_URL

    block_manager = BlockManager
    transaction_manager = TransactionManager

    def __init__(self, logger: logging, **kwargs):
        from tronpy.async_tron import AsyncTron, AsyncHTTPProvider

        self.gate = AsyncTron(provider=AsyncHTTPProvider(endpoint_uri=self.gate_url))

        super(Node, self).__init__(gate=self.gate, **kwargs)

    def reconnect(self):
        pass

    @property
    def node(self):
        try:
            # If node died
            return self.gate
        except:
            pass
