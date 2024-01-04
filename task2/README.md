# Task 2: Multisignature Transactions

In this task, we will create a multisig address and simulate to spend this fund.

## Project structure

├── lab02_config
│   ├── task02_config
│   │   ├── task02_pr1
│   │   ├── task02_pr2
│   │   ├── task02_pr3
├── libeay32.dll
├── main\.py
├── setup\.py
├── utils\.py
├── README\.md
└── .gitignore

Our main works are conducted on `main.py`, detail about the generated private key is stored in `lib02_config/task02_config`. We write support functions in `utils.py`, and `setup.py` stored generate key functions, create multisig and simulate spend fund.

## Prerequisite

We run this code in window os. So there will be error if you install the incorrect version of library `python-bitcoinlib` and the `libeasy32.dll` is only suitable with the **python version 32bit**. Summary as bellow:

* Python version 32 bit.
* Install `python-bitcoinlib==0.12.0` as shown in `requirement.txt`.

## Setup
Activate the **bcl02** virtual environment. Install the requirements before runing the `main.py`

```
pip install -r requirements.txt
```

## Description
To run this task, we simply the below command.
```
python main.py
```

Firstly, the program turn generate or load the saved private keys in `lab02_config/task02_config`. We have set the `RANDOM_SEED` for each key to deterministic private keys.

Next, we generate the multisig address for 2 of pre-defined private keys, then we send bitcoin to this address on testnet in [btc-testnet]( https://coinfaucet.eu/en/btc-testnet/) as bellow.

![Figure 1: Send bitcoin to multisig address on btc-testnet.](/images/send_bitcoin_to_multisig_address.png)

Then, we checkout the multisig address and initialize transaction at [block-cypher](https://live.blockcypher.com/btc-testnet/) to confirm that we have received bitcoin from btc-testnet and obtain the transaction id for spend this fund.

![Figure 2: Check multisig address.](/images/check_multisig_address.png)

![Figure 3: Check initialize transaction.](/images/check_init_transaction.png)

After that, we create a signed multisig transaction, then broadcast that transaction into btc-testnet using api from block-cypher.

![Figure 3: Check initialize transaction.](/images/spend_this_fund.png)

Auxiliary part: here is our serialize values of created transaction. However, you could also verify it at this [link](https://live.blockcypher.com/btc-testnet/tx/66c5cc9cef51e027fd3902bc8b1c3b56c988822c4b25753cc2de3410e2c4c580/)
```
010000000130d23f305049dfedd4bf5a70d187f691f23030cef70506d527cc07864c287ad400000000da00483045022100bc95a49300a1a03702bc8fbc47225b257310434a4a8ad5528a1f79d43f28e9710220046224aba9d8548c6e2e4b73dd0c072539137daf74538f7b1f8da55894302192014730440220796e9741db8f0fee9e6c7fd8c307daabbcdb2cdc2ec70de49d7fea5a7abf8e5002204657dc40ac7e1c5208b428bfa48796922d3451bc0ca57a58374f11dec9dfb8fb01475221020b5939c400f7482be1b61dbd34619b1b345867eeabf5fdadc689bca493cc2bd22103faa96065ac172b6fd45d1fea57ad91f298e37bc75e805e3a83f22a73a9b52d4252aeffffffff0110270000000000001976a914758898627ce01ab46f1859b9bac93a418a7ade9788ac00000000
```