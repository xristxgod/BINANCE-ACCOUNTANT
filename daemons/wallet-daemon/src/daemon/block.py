import abc
from typing import NoReturn

import src.settings as settings
from src.services import FileBlockController


class BaseBlockManager:
    file_path: str
    file_controller = FileBlockController

    def __init__(self, *args, **kwargs):
        self.controller = self.file_controller(file=self.file_path)

    @abc.abstractmethod
    async def get_block_now(self) -> int: ...

    @abc.abstractmethod
    async def get_block_in_storage(self) -> int: ...

    @abc.abstractmethod
    async def save_block_to_storage(self, block: int) -> NoReturn: ...


class TronBlockManager(BaseBlockManager):
    file_path = settings.BLOCKS_DIR + 'tron_block.txt'

    def __init__(self, gate, *args, **kwargs):
        from tronpy.async_tron import AsyncTron

        self.gate: AsyncTron = gate

        super(TronBlockManager, self).__init__(*args, **kwargs)

    def get_block_now(self) -> int:
        return await self.gate.get_latest_block_number()

    def get_block_in_storage(self) -> int:
        return await self.controller.read()

    def save_block_to_storage(self, block: int) -> NoReturn:
        return await self.controller.write(block=block)
