# BLOCKCHAIN_LAB2
Setup on Linux (recommended distro: Ubuntu 20.04.6 LTS)
```
sudo apt-get update -y
sudo apt-get install -y python3-venv
python3 -m venv .venv
source .venv/bin/activate
pip install bitcoin
pip install python-bitcoinlib
```

To create P2PKH address on testnet, run:
```
python3 createAddress.py
```

To get testnet bicoin, use this faucet https://coinfaucet.eu/en/btc-testnet/

To broadcast transaction, use this link https://live.blockcypher.com/btc/pushtx/ and select Network: Bitcoin Testnet

Transaction details can also be queried on blockcypher.com