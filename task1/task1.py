# P2PKH Script
import bitcoin
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress, CBitcoinAddress
from bitcoin.core.script import CScript, OP_DUP, OP_HASH160, OP_EQUALVERIFY, OP_CHECKSIG, SignatureHash, SIGHASH_ALL
from bitcoin.core import b2x, lx, CMutableTxIn, CMutableTxOut, COutPoint, CMutableTransaction, Hash160
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
import os


def create_txin(txid, output_index):
    return CMutableTxIn(COutPoint(lx(txid), output_index))


def create_txout(amount_to_send, destination_address):
    return CMutableTxOut(amount_to_send,CBitcoinAddress(destination_address).to_scriptPubKey())

# Assume that transaction has only 1 input
def create_signed_transaction(txins, txouts, private_keys):
    tx = CMutableTransaction(txins, txouts)
    seckey = CBitcoinSecret(private_keys[0])
    txin_scriptPubKey = CScript([OP_DUP, OP_HASH160, Hash160(seckey.pub), OP_EQUALVERIFY, OP_CHECKSIG])
    sighash = SignatureHash(txin_scriptPubKey, tx, 0, SIGHASH_ALL)
    sig = seckey.sign(sighash) + bytes([SIGHASH_ALL])
    txins[0].scriptSig = CScript([sig, seckey.pub])
    VerifyScript(txins[0].scriptSig, txin_scriptPubKey, tx, 0, (SCRIPT_VERIFY_P2SH,))
    return tx

def broadcast_tx(tx):
    print(b2x(tx.serialize()))

if __name__ == '__main__':
    bitcoin.SelectParams("testnet")

    private_key = "cNXjTfF22zerXJ8Y7oQvkADWZXt8tPeW1X11h1UxRsZdmJ5ZopL3"
    address = "mzBURj9ECP9L1hgpptw3WCrL5Doy8E6miK"
    # Create a transaction input (UTXO)
    txid = "14b435f4f480f67ac60de3ce1c365190f27ac8808a88dcdd60b1ccd268b71500"
    output_index = 1
    txin = create_txin(txid, output_index)

    # Create a transaction output to the desired destination
    destination_address = "mke673EfHY1stJmwVrgxzf9xPoX7ggq4jr"
    amount_to_send = 250000 # Amount to send in satoshis
    txout = create_txout(amount_to_send, destination_address)

    # Create the transaction
    tx = create_signed_transaction([txin], [txout], [private_key])
    # Broadcast the transaction
    broadcast_tx(tx)