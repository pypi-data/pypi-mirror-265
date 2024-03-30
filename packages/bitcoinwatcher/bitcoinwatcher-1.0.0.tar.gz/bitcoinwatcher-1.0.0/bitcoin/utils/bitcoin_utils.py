from bitcoin.core import CTransaction
from bitcoinutils.keys import PublicKey
from bitcoinutils.transactions import TxOutput


def get_tx_id_from_tx(tx: CTransaction) -> str:
    tx_id = tx.GetTxid()
    # convert it to hex
    txid_hex = tx_id[::-1].hex()
    return txid_hex


def get_address_from_output(output: TxOutput):
    public_key = output.script_pubkey.to_hex()
    address = PublicKey(public_key)
    print(address)
