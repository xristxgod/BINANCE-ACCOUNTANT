import abc
import decimal
import logging
from dataclasses import dataclass
from typing import NoReturn, Type, List

import aiofiles


@dataclass()
class DefaultBlockHeader:
    block: int
    timestamp: int


@dataclass()
class DefaultParticipant:
    address: str
    amount: decimal.Decimal


@dataclass()
class DefaultTransaction:
    transactionId: str
    amount: decimal.Decimal
    fee: decimal.Decimal
    inputs: List[DefaultParticipant]
    outputs: List[DefaultParticipant]
    timestamp: int
    token: str


@dataclass()
class DefaultBlock:
    headers: DefaultBlockHeader
    transactions: List[DefaultTransaction]


class BaseNode:
    pass


class BaseBlockManager:
    file_path: str

    class FileManager:

        def __init__(self, file: str):
            self.file = file

        async def write(self, block_number: int) -> NoReturn:
            async with aiofiles.open(self.file, 'w', encoding='utf-8') as file:
                await file.write(str(block_number))

        async def read(self) -> str:
            async with aiofiles.open(self.file, "r", encoding='utf-8') as file:
                return await file.read()

    def __init__(self, *args, **kwargs):
        self.gate = kwargs.get('gate')
        self.manager = self.FileManager(file=self.file_path)

    async def get_block_by_id(self, block: int) -> DefaultBlock:
        return await self.gate.get_latest_block(block)

    async def get_block_number(self) -> int:
        return await self.gate.get_latest_block_number()

    # Daemon function

    async def get_block_in_storage(self) -> int:
        block_number = await self.manager.read()
        if block_number:
            return int(block_number)
        return await self.get_block_number()

    async def save_block_to_storage(self, block: int) -> NoReturn:
        return await self.manager.write(block_number=block)


class BaseSmartContract:

    @abc.abstractclassmethod
    async def connect(cls, address: str): ...


class BaseTransactionManager:

    def __init__(self, logger: logging, cls_smart_contract: Type[BaseSmartContract], **kwargs):
        self.logger = logger
        self.smart_contract = cls_smart_contract

    @abc.abstractmethod
    async def create_transaction(self, from_: str, to: str, amount: decimal.Decimal) -> object: ...

    @abc.abstractmethod
    async def send_transaction(self, transaction_hash: str, private_key: str) -> DefaultTransaction: ...

    @abc.abstractmethod
    async def get_transaction_by_transaction_id(self, transaction_id: str) -> DefaultTransaction: ...

    @abc.abstractmethod
    async def get_transactions_by_wallet_address(self, address: str) -> List[DefaultTransaction]: ...


class BaseWalletManager:

    def __init__(self, cls_smart_contract: Type[BaseSmartContract], **kwargs):
        self.smart_contract = cls_smart_contract

    @abc.abstractmethod
    async def get_balance(self, token: str) -> decimal.Decimal: ...

    @abc.abstractmethod
    async def get_optimal_fee(self, from_: str, to: str, amount: decimal.Decimal) -> decimal.Decimal: ...


class BaseGateClient:
    cls_node: Type[BaseNode]

    cls_smart_contract: Type[BaseSmartContract]

    cls_block_manager: Type[BaseBlockManager]
    cls_transaction_manager: Type[BaseTransactionManager]
    cls_wallet_manager: Type[BaseWalletManager]

    cls_response_transaction: DefaultTransaction
    cls_response_block: DefaultBlock

    def __init__(self, **kwargs):
        self.node = self.cls_node()

        self.__block = self.cls_block_manager(
            node=self.node
        )
        self.__transaction = self.cls_transaction_manager(
            node=self.node,
            logger=kwargs.get('logger'),
            cls_smart_contract=self.cls_smart_contract
        )
        self.__wallet = self.cls_wallet_manager(
            node=self.node,
            logger=kwargs.get('logger'),
            cls_smart_contract=self.cls_smart_contract
        )

    def block(self) -> BaseBlockManager:
        return self.__block

    def transaction(self) -> BaseTransactionManager:
        return self.__transaction

    def wallet(self) -> BaseWalletManager:
        return self.__wallet

    def node(self): ...
