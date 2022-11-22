import decimal
from typing import Optional

from tronpy.async_tron import AsyncContract

import src.settings as settings
import gateway.gate.base as base
from gateway.schemas import BlockHeaderSchema, ParticipantSchema, TransactionSchema, BlockSchema


TOKENS = {
    'USDT': {'address': '...', 'decimals': 8}
}


class Node(base.AbstractNode):
    network_name = 'tron'
    endpoint_uri = settings.TRON_GATE_URL

    class SmartContract:
        @classmethod
        async def connect(cls, address: str) -> AsyncContract:
            return AsyncContract(address)

    def __init__(self):
        from tronpy.async_tron import AsyncTron, AsyncHTTPProvider
        self.node = AsyncTron(provider=AsyncHTTPProvider(endpoint_uri=self.endpoint_uri))

        self.decimals = decimal.Context()
        self.decimals.prec = 6

    async def get_block(self, block_number: int) -> BlockSchema:
        response = await self.node.get_block(block_number)
        headers = BlockHeaderSchema(
            block=response['block_header']['raw_data']['number'],
            timestamp=response['block_header']['raw_data']['timestamp']
        )
        transactions = []
        for transaction in response['transactions']:
            token = None
            fee = self.decimals.create_decimal(0)

            contract = transaction['raw_data']['contract']

            if contract[0]['type'] == 'TransferContract':
                amount = self.decimals.create_decimal(contract[0]['parameter']['value']['amount'])
                fee = self.decimals.create_decimal(0)

                inputs = [ParticipantSchema(
                    address=contract[0]['parameter']['value']['owner_address'],
                    amount=amount
                )]
                outputs = [ParticipantSchema(
                    address=contract[0]['parameter']['value']['to_address'],
                    amount=amount
                )]

            elif contract['type'] == '':
                amount = 0
                fee = 0
                inputs = []
                outputs = []
            else:
                continue

            transactions.append(TransactionSchema(
                transactionId=transaction['txID'],
                amount=amount,
                fee=fee,
                inputs=inputs,
                outputs=outputs,
                timestamp=transaction['raw_data']['timestamp'],
                token=token
            ))

        return BlockSchema(
            headers=headers,
            transactions=transactions
        )

    async def get_latest_block_number(self) -> int:
        return await self.node.get_latest_block_number()

    async def get_balance(self, address: str, token: Optional[str] = None) -> decimal.Decimal:
        if not token:
            amount = await self.node.get_account_balance(address)
        else:
            token = TOKENS[token]
            contract = await self.SmartContract.connect(token['address'])
            amount = await contract.functions.balanceOf(address)
            if amount > 0:
                amount = amount / 10 ** token['decimals']

        return self.decimals.create_decimal(amount)
