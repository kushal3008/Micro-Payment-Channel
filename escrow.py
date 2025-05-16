from pyteal import *

def escrow_contract():
    sender = Txn.sender()
    receiver = Txn.receiver()
    amount = Txn.amount()
    close_remainder_to = Txn.close_remainder_to()
    first_valid = Global.first_valid()
    last_valid = Global.last_valid()
    current_round = Global.round()
    fee = Int(1000)

    valid_payment = And(
        Txn.group_index() == Int(0),
        Txn.rekey_to() == Global.zero_address(),
        Txn.close_remainder_to() == Global.zero_address(),
    )

    settle = And(
        Txn.on_completion() == OnComplete.NoOp,
        Txn.sender() == App.globalGet(Bytes("sender")),
        Txn.application_args.length() == Int(2),
        Btoi(Txn.application_args[1]) <= App.globalGet(Bytes("max_amount")),
    )

    return Cond(
        [Txn.application_id() == Int(0), Seq([
            App.globalPut(Bytes("sender"), Txn.sender()),
            App.globalPut(Bytes("receiver"), Txn.accounts[1]),
            App.globalPut(Bytes("max_amount"), Int(0)),
            Approve()
        ])],
        [Txn.on_completion() == OnComplete.NoOp, Seq([
            Assert(settle),
            App.globalPut(Bytes("max_amount"), Btoi(Txn.application_args[1])),
            Approve()
        ])],
        [Txn.on_completion() == OnComplete.DeleteApplication, Return(Txn.sender() == App.globalGet(Bytes("sender")))]
    )

if __name__ == "__main__":
    print(compileTeal(escrow_contract(), Mode.Application, version=5))
