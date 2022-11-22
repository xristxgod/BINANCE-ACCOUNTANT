import abc
from typing import NoReturn, Type

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


class BaseTransactionManager:
    pass


class BaseNode:
    gate_url: str

    block_manager: Type[BaseBlockManager]
    transaction_manager: Type[BaseTransactionManager]

    def __init__(self, **kwargs):
        self.block_controller = self.block_manager(gate=kwargs.get('gate'))
        self.transaction_controller = self.transaction_manager(gate=kwargs.get('gate'))
