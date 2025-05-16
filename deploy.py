import json
from algosdk import account, algod, transaction
from algosdk.v2client import algod
from algosdk.future.transaction import ApplicationCreateTxn
from algosdk.logic import get_application_address
from pyteal import compileTeal
from escrow import escrow_contract

ALGOD_ADDRESS = "https://testnet-algorand.api.purestake.io/ps2"
ALGOD_TOKEN = "YourPureStakeApiKeyHere"
HEADERS = {"X-API-Key": ALGOD_TOKEN}

algod_client = algod.AlgodClient(ALGOD_TOKEN, ALGOD_ADDRESS, HEADERS)

def compile_program(client, source_code):
    compile_response = client.compile(source_code)
    return compile_response['result'], compile_response['hash']

def create_app(client, private_key, approval_program, clear_program, global_schema, local_schema):
    sender = account.address_from_private_key(private_key)
    params = client.suggested_params()
    txn = ApplicationCreateTxn(sender, params, on_complete=transaction.OnComplete.NoOpOC,
                               approval_program=approval_program,
                               clear_program=clear_program,
                               global_schema=global_schema,
                               local_schema=local_schema)
    signed_txn = txn.sign(private_key)
    tx_id = client.send_transaction(signed_txn)
    response = transaction.wait_for_confirmation(client, tx_id, 4)
    return response['application-index']

def main():
    private_key = "YourPrivateKeyHere"
    approval_src = compileTeal(escrow_contract(), mode=1, version=5)
    clear_src = "int 1"

    approval_compiled, _ = compile_program(algod_client, approval_src)
    clear_compiled, _ = compile_program(algod_client, clear_src)

    global_schema = transaction.StateSchema(num_uints=2, num_byte_slices=1)
    local_schema = transaction.StateSchema(num_uints=0, num_byte_slices=0)

    app_id = create_app(algod_client, private_key, approval_compiled, clear_compiled, global_schema, local_schema)
    print(f"Deployed app with ID: {app_id}")

if __name__ == "__main__":
    main()
