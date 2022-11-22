import os
import abc
from typing import NoReturn, Type

import aiofiles

import meta
import src.settings as settings
import new_gateway.logger as logger
from new_gateway.schemas import BlockSchema


class AbstractNode:
    network_name: str

    class SmartContract(abc.ABC):
        @abc.abstractclassmethod
        async def connect(cls): ...

    @property
    def network(self) -> str:
        return self.network

    @abc.abstractmethod
    async def get_block(self, block_number: int) -> BlockSchema: ...

    @abc.abstractmethod
    async def get_latest_block_number(self) -> int: ...


class DefaultBlockManager:

    class FileBlockManager:

        def __init__(self, name: str):
            self.file_path = os.path.join(settings.BLOCKS_DIR, f'{name}_block.txt')

        async def write(self, block_number: int) -> NoReturn:
            async with aiofiles.open(self.file_path, 'w', encoding='utf-8') as file:
                await file.write(str(block_number))

        async def read(self) -> str:
            async with aiofiles.open(self.file_path, "r", encoding='utf-8') as file:
                return await file.read()

    __slots__ = (
        '__node', 'manager'
    )

    def __init__(self, node: AbstractNode):
        self.__node = node
        self.manager = self.FileBlockManager(name=self.__node.network)

    async def get_block_by_id(self, block_number: int) -> BlockSchema:
        return await self.__node.get_block(block_number)

    async def get_latest_block_number(self) -> int:
        return await self.__node.get_latest_block_number()

    # Daemon function

    async def get_block_in_storage(self) -> int:
        block_number = await self.manager.read()
        if block_number:
            return int(block_number)
        return await self.get_latest_block_number()

    async def save_block_to_storage(self, block: int) -> NoReturn:
        return await self.manager.write(block_number=block)


class DefaultTransactionManager:

    def __init__(self, node: AbstractNode, cls_logger: Type, **kwargs):
        self.logger = cls_logger()
        self.__node = node

    async def create_transaction(self):
        pass

    async def send_transaction(self):
        pass


class BaseGateClient:

    cls_node: Type[AbstractNode]

    cls_logger: Type[meta.Logger] = logger.GateClientLogger

    cls_block_manager: Type[DefaultBlockManager] = DefaultBlockManager
    cls_transaction_manager: Type[DefaultTransactionManager] = DefaultTransactionManager
