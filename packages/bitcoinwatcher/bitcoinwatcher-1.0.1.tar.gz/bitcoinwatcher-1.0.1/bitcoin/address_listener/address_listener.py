import dataclasses
import os
from abc import ABC, abstractmethod
from enum import Enum

from bitcoinlib.transactions import Transaction
from ordipool.ordipool.mempoolio import Mempool

from bitcoin.tx_listener.abstract_tx_listener import AbstractTxListener
from bitcoin.utils.constants import default_host


class AddressTxType(Enum):
    INPUT = "input"
    OUTPUT = "output"


@dataclasses.dataclass
class AddressTxData:
    tx_id: str
    address: str
    type: AddressTxType
    # figure out the way to get amount in vin
    _amount: int = 0

    def get_amount(self):
        return self._amount

    def amount_in_btc(self):
        if self.type == AddressTxType.INPUT:
            return "Amount is not supported for input type, yet"
        return self._amount / 100000000


class AbstractAddressListener(AbstractTxListener, ABC):
    DECIMAL_SCALE = 5
    host = os.environ.get("RPC_HOST", default_host)
    base_url = f"http://{host}:3006/api"
    mempool = Mempool(base_url=base_url)

    def __init__(self, addresses_to_listen: {str}):
        self.addresses_to_listen = addresses_to_listen

    @abstractmethod
    def consume(self, subscribed_address, address_tx_data: [AddressTxData]):
        pass

    def filter_address_tx_data(self, address_tx_data: [AddressTxData]) -> [str]:
        filtered_address_tx_data = list(filter(lambda x: x.address in self.addresses_to_listen and x.address != "",
                                               address_tx_data))
        # get all address
        return list(set((map(lambda x: x.address, filtered_address_tx_data))))

    def on_tx(self, tx: Transaction):
        # get all address in the inputs and outputs along with the amount
        if tx.coinbase:
            return
        outputs = tx.outputs
        tx_id = tx.txid
        tx = self.mempool.get_transaction(tx_id)
        address_tx_data = []
        # getting inputs data separately from mempool
        # as current library doesn't provide rich data like previous outputs and its value
        for input in tx.vins:
            address = input.prev_out.address
            amount = input.prev_out.value
            address_tx_data.append(AddressTxData(address=address,
                                                 type=AddressTxType.INPUT,
                                                 _amount=amount,
                                                 tx_id=tx_id))
        for output in outputs:
            amount = output.value
            address_tx_data.append(AddressTxData(address=output.address,
                                                 _amount=amount,
                                                 type=AddressTxType.OUTPUT,
                                                 tx_id=tx_id))

        # filter the address we are interested in
        addresses_for_events = self.filter_address_tx_data(address_tx_data)
        for address in addresses_for_events:
            self.consume(subscribed_address=address, address_tx_data=address_tx_data)
