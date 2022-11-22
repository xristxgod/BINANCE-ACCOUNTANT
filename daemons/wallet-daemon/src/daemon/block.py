import abc

import src.settings as settings
from src.services import FileController


class BaseBlock:
    file_path: str
    file_controller = FileController

    @abc.abstractmethod
    async def get_block_now(self) -> int: ...

    @abc.abstractmethod
    async def get_last_block(self) -> int: ...

    @abc.abstractmethod
    async def save_block(self, block: int) -> int: ...


class TronBlock(BaseBlock):
    file_path = settings.BLOCKS_DIR + 'tron_block.txt'

    def __init__(self, gate):
        pass

    def get_block_now(self):
        pass