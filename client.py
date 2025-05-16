from algosdk import account, algod, transaction
from algosdk.future.transaction import ApplicationNoOpTxn
from algosdk.v2client import algod

ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_TOKEN = "YourPureStakeApiKeyHere"
HEADERS = {"X-API-Key": ALGOD_TOKEN}

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS, HEADERS)

def send_payment(private_key, app_id, receiver_address, amount):
    sender = account.address_from_private_key(private_key)
    params = algod_client.suggested_params()
    max_amount = amount
    app_args = [b"settle", amount.to_bytes(8, "big")]
    txn = ApplicationNoOpTxn(sender, params, app_id, app_args, [receiver_address])
    signed_txn = txn.sign(private_key)
    tx_id = algod_client.send_transaction(signed_txn)
    response = transaction.wait_for_confirmation(algod_client, tx_id, 4)
    return response

if __name__ == "__main__":
    private_key = "YourPrivateKeyHere"
    app_id = 123456  # deployed app id here
    receiver = "RECEIVER_ADDRESS"
    amount = 1000
    resp = send_payment(private_key, app_id, receiver, amount)
    print(resp)
