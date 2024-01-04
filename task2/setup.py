# P2PKH Script
import os
import requests
from bitcoin import *
from bitcoin.core import *
from bitcoin.core.script import *
from bitcoin.core.scripteval import VerifyScript, SCRIPT_VERIFY_P2SH
from bitcoin.wallet import CBitcoinSecret, P2PKHBitcoinAddress, P2SHBitcoinAddress
from utils import *

CONFIG_FILE_PATH = './lab02_config'
if not os.path.exists(CONFIG_FILE_PATH):
    os.makedirs(CONFIG_FILE_PATH)
    
bitcoin.SelectParams('testnet')


def generate_private_key(seed, dir=CONFIG_FILE_PATH, task_name='task02'):
    """
    The function generates a random private key, derives the corresponding public key and Bitcoin
    address, and writes the configuration to a file.
    
    :param seed: The `seed` parameter is a value used to generate a random private key. It is typically
    a random number or a string that serves as the input for the random number generator
    :param dir: The `dir` parameter is the directory where the configuration file will be saved. It is
    set to `CONFIG_FILE_PATH` by default, which is likely a constant defined elsewhere in the code. You
    can change the value of `CONFIG_FILE_PATH` to specify the desired directory
    :param task_name: The `task_name` parameter is a string that represents the name of the task or
    operation being performed. It is used as part of the filename when writing the configuration file,
    defaults to task02 (optional)
    :return: a dictionary object named `config`. This dictionary contains the following keys and values:
    """
    config = {}
    rand_seed = random.Random(seed)
    
    # Generate a random private key
    secret_bytes = bytes_random(rand_seed, 32)
    private_key = CBitcoinSecret.from_secret_bytes(secret_bytes)
    config['private_key'] = private_key
    
    # Derive the public key and Bitcoin address
    public_key = private_key.pub
    address = P2PKHBitcoinAddress.from_pubkey(public_key)
    
    err, message = write_config(dir, task_name, config)
    if err:
        raise(message)
    else:
        print(message)
    
    config['public_key'] = public_key
    config['address'] = address
    return config

def load_private_key(seed, dir=CONFIG_FILE_PATH, task_name='task02'):
    """
    The function `load_private_key` loads a private key from a configuration file, or generates a new
    one if the file does not exist.
    
    :param seed: The `seed` parameter is used to generate a private key. It is a value that is used as
    input to a random number generator to generate a secure private key
    :param dir: The `dir` parameter is the directory where the configuration file is located. It is set
    to `CONFIG_FILE_PATH` by default, which is a variable that should contain the path to the directory
    :param task_name: The `task_name` parameter is a string that represents the name of the task or
    project for which the private key is being loaded or generated. It is used to create a directory and
    file name to store the private key and other configuration data, defaults to task02 (optional)
    :return: the `config` dictionary.
    """
    config = {}
    if os.path.exists(f'{dir}/{task_name}'):
        err, message, config = load_config(dir, task_name)
        if err:
            raise(message)
        else:
            print(message)
        
        # reconstruct by loaded data
        config['private_key'] = CBitcoinSecret(config['private_key'])
        config['public_key'] = config['private_key'].pub
        config['address'] = P2PKHBitcoinAddress.from_pubkey(config['public_key'])
    else:
        config = generate_private_key(seed=seed, dir=dir, task_name=task_name)
        
    return config


def create_multisig(user_01, user_02):
    """
    The function `create_multisig` creates a 2-of-2 multisig redeem script and a P2SH address from the
    public keys of two users.
    
    :param user_01: A dictionary containing information about the first user. It should have a key
    "public_key" which holds the public key of the first user
    :param user_02: The `user_02` parameter is a dictionary that contains information about the second
    user. It likely includes the public key of the second user, which is needed to create the multisig
    redeem script
    :return: two values: the redeem script and the P2SH address.
    """
    # Create a 2-of-2 multisig redeem script
    public_key1 = user_01['public_key']
    public_key2 = user_02['public_key']
    redeem_script = CScript([OP_2, public_key1, public_key2, OP_2, OP_CHECKMULTISIG])
    # Create a P2SH address from the redeem script
    address = P2SHBitcoinAddress.from_redeemScript(redeem_script)

    return redeem_script, address

def create_txin(txid, utxo_index):
    """
    The above function creates a transaction input and output for a Bitcoin transaction.
    
    :param txid: The txid parameter is the transaction ID of the previous transaction that contains the
    output you want to spend
    :param utxo_index: The `utxo_index` parameter represents the index of the unspent transaction output
    (UTXO) within the transaction specified by `txid`
    :return: The function `create_txin` returns a `CMutableTxIn` object, and the function `create_txout`
    returns a `CMutableTxOut` object.
    """
    return CMutableTxIn(COutPoint(lx(txid), utxo_index))

def create_txout(amount, address):
    """
    The function creates a transaction output with a specified amount and script public key.
    
    :param amount: The amount parameter is the amount of cryptocurrency to be sent in the transaction
    output. It is usually specified in the smallest unit of the cryptocurrency (e.g., satoshis for
    Bitcoin)
    :param scriptPubKey: The scriptPubKey is a script that specifies the conditions that must be met in
    order to spend the output of a transaction. It typically contains the recipient's public key or
    address, along with any additional conditions or requirements
    :return: a CMutableTxOut object.
    """
    return CMutableTxOut(amount, CScript(address.to_scriptPubKey()))

def broadcast_tx(tx):
    """
    The function `broadcast_transaction` sends a Bitcoin transaction to the BlockCypher API for
    broadcasting.
    
    :param tx: The `tx` parameter is the transaction object that needs to be broadcasted. It should be
    an instance of a transaction class, such as `bitcoinlib.Transaction` or `bitcoin.Transaction`
    :return: the response from the POST request made to the BlockCypher API.
    """
    return requests.post(
        'https://api.blockcypher.com/v1/btc/test3/txs/push',
        headers={'content-type': 'application/x-www-form-urlencoded'},
        data='{"tx": "%s"}' % b2x(tx.serialize())
)


def create_verified_multisig_transaction(base_transaction: dict, sender_01: dict, sender_02:dict, receiver:dict):
    # create multisig address
    print(get_log('create multisig address'))
    redeem_scripts, address = create_multisig(sender_01, sender_02)
    
    print(get_log('create transaction spend on multisig address'))
    txIn = create_txin(base_transaction['transaction_id'], base_transaction['utxo_index'])
    amount_to_send = 0.0001*COIN
    txOut = create_txout(amount=amount_to_send*0.95, address=receiver['address'])
    
    # create new transaction for spend this fund
    txTarget = CMutableTransaction([txIn], [txOut])
    signHash = SignatureHash(redeem_scripts, txTarget, 0, SIGHASH_ALL, amount_to_send)
    sig1 = sender_01['private_key'].sign(signHash) + bytes([SIGHASH_ALL])
    sig2 = sender_02['private_key'].sign(signHash) + bytes([SIGHASH_ALL])

    txIn.scriptSig = CScript([OP_0, sig1, sig2, redeem_scripts])
    
    print(get_log("created transaction successfully: \n"+ b2x(txTarget.serialize())))
    return txTarget
