from setup import *
from bitcoin.wallet import P2SHBitcoinAddress
from bitcoin.core.script import *
from utils import *

RANDOM_SEED_01 = 234
RANDOM_SEED_02 = 77017
RANDOM_SEED_03 = 500

# load config
print(get_log('create or load data from file'))
task02_dir = f"{CONFIG_FILE_PATH}/task02_config"
# create multisig by user_01 and user_02 then the receiver is user_03 
user_01 = load_private_key(seed=RANDOM_SEED_01, task_name='task02_pr1', dir=task02_dir)
user_02 = load_private_key(seed=RANDOM_SEED_02, task_name='task02_pr2', dir=task02_dir)
user_03 = load_private_key(seed=RANDOM_SEED_03, task_name='task02_pr3', dir=task02_dir)


base_transaction = {'transaction_id': 'd47a284c8607cc27d50605f7ce3030f291f687d1705abfd4eddf4950303fd230',
                    'utxo_index': 0}

txNew = create_verified_multisig_transaction(
    base_transaction=base_transaction,
    sender_01=user_01,
    sender_02=user_02,
    receiver=user_03
)

# broadcast transaction
# response = broadcast_tx(txNew)
# print(response.text)