# Micro-Payment Channel on Algorand

A PyTeal based micro-payment channel smart contract that allows off-chain payments with on-chain settlement.

## Files

- `escrow.py` - The PyTeal smart contract for the escrow channel.
- `deploy.py` - Script to compile and deploy the contract.
- `client.py` - Example client to interact with the contract.

## Usage

1. Deploy the contract using `deploy.py`.
2. Use `client.py` to send payments and settle them on-chain.
3. Modify addresses and keys in the scripts as needed.

## Requirements

- Python 3.x
- PyTeal
- Algorand SDK for Python
