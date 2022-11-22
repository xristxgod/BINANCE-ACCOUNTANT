import abc
import decimal
import logging
from dataclasses import dataclass
from typing import NoReturn, Type
from typing import List


@dataclass()
class BaseHeader:
    block: int
    timestamp: int


@dataclass()
class BaseTransaction:
    pass


@dataclass()
class BaseBlock:
    headers: BaseHeader
    transactions: List[BaseTransaction]


class BaseBlockManager:
    file_path: str

    class FileManager:

        def __init__(self, file: str):
            pass

        async def write(self, block: int):
            pass

        async def read(self):
            pass

    def __init__(self, *args, **kwargs):
        self.manager = self.FileManager(file=self.file_path)

    @abc.abstractmethod
    async def get_block_by_id(self, block: int) -> List[BaseBlock]: ...

    @abc.abstractmethod
    async def get_block_now(self) -> int: ...

    # Daemon function

    @abc.abstractmethod
    async def get_block_in_storage(self) -> int: ...

    @abc.abstractmethod
    async def save_block_to_storage(self, block: int) -> NoReturn: ...


class BaseSmartContract:

    @abc.abstractmethod
    def connect(self, address: str): ...


class BaseTransactionManager:

    def __init__(self, logger: logging, **kwargs):
        self.logger = logger

    @abc.abstractmethod
    async def get_transaction_by_transaction_id(self, transaction_id: str) -> object: ...

    @abc.abstractmethod
    async def get_transactions_by_wallet_address(self, address: str) -> List[object]: ...


class BasePaymentManager:

    def __init__(self, logger: logging, **kwargs):
        self.logger = logger

    @abc.abstractmethod
    async def get_balance(self, token: str) -> decimal.Decimal: ...

    @abc.abstractmethod
    async def create_transaction(self, from_: str, to: str, amount: decimal.Decimal) -> object: ...

    @abc.abstractmethod
    async def send_transaction(self, transaction_hash: str, private_key: str) -> object: ...


class BaseNode:
    gate_url: str

    smart_contract: Type[BaseSmartContract]

    block_manager: Type[BaseBlockManager]
    transaction_manager: Type[BaseTransactionManager]
    payment_manager: Type[BasePaymentManager]

    cls_response_transaction: BaseTransaction
    cls_response_block: BaseBlock

    def __init__(self, **kwargs):
        self.__block = self.block_manager(
            gate=kwargs.get('gate')
        )
        self.__transaction = self.transaction_manager(
            gate=kwargs.get('gate'),
            logger=kwargs.get('logger'),
            smart_contract=self.smart_contract
        )
        self.__payment = self.payment_manager(
            gate=kwargs.get('gate'),
            logger=kwargs.get('logger'),
            smart_contract=self.smart_contract
        )

    @abc.abstractproperty
    def node(self): ...

    def block(self) -> BaseBlockManager:
        return self.__block

    def transaction(self) -> BaseTransactionManager:
        return self.__transaction

    def payment(self) -> BasePaymentManager:
        return self.__payment
