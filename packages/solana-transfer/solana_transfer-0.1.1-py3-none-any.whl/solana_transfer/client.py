from solana.rpc.api import Keypair, Pubkey, Client
from solders.system_program import TransferParams, transfer
from solana_transaction.transaction import Transaction
from spl_token.core import Token
from spl.token.constants import TOKEN_PROGRAM_ID as program_id
from solana.rpc.types import TokenAccountOpts


class TransferClient:

    def __init__(self, rpc_endpoint=None, private_key=None, seed=None):
        self.rpc_endpoint = rpc_endpoint
        self.private_key = private_key
        self.seed = seed

    def transfer_sol(self, receiver=None, sol_no=None):
        """
            转账sol
        :param private_key:
        :param receiver:
        :param lamport:
        :return:
        """
        if self.private_key:
            sender = Keypair.from_base58_string(self.private_key)
        elif self.seed:
            sender = Keypair.from_seed(self.seed)
        else:
            raise '请提供 private key 或者 seed'

        if not self.rpc_endpoint:
            client = Client('https://api.mainnet-beta.solana.com')
        else:
            client = Client(self.rpc_endpoint)

        if not receiver:
            raise '请提供接收者账户地址'

        receiver = Pubkey.from_string(receiver)

        if not sol_no:
            lamport = client.get_balance(sender.pubkey()).value
        else:
            lamport = sol_no * 1000000000

        try:
            txn = Transaction().add(
                transfer(TransferParams(from_pubkey=sender.pubkey(), to_pubkey=receiver, lamports=int(lamport))))
        except:
            raise '余额不足, 请减少转账数量'

        tx = client.send_transaction(txn, sender).value
        return tx

    def transfer_sol_token(self, receiver=None, token_address_string=None,
                           lamport: float = None):
        """
            转账token
        :param private_key:
        :param receiver:
        :param token_address_string:
        :param lamport:
        :return:
        """
        if self.private_key:
            sender = Keypair.from_base58_string(self.private_key)
        elif self.seed:
            sender = Keypair.from_seed(self.seed)
        else:
            raise '请提供 private key 或者 seed'

        if not self.rpc_endpoint:
            client = Client('https://api.mainnet-beta.solana.com')
        else:
            client = Client(self.rpc_endpoint)

        if not receiver:
            raise '请提供接收者账户地址'

        receiver_pk = Pubkey.from_string(receiver)

        if not token_address_string:
            raise "请提供token合约地址"

        token_address = Pubkey.from_string(token_address_string)

        try:
            source_token_account = \
                client.get_token_accounts_by_owner(sender.pubkey(), TokenAccountOpts(token_address)).value[0].pubkey
        except:
            raise 'token account error'
        token_balance = client.get_token_account_balance(source_token_account).value
        ui_amount = token_balance.ui_amount
        decimals = token_balance.decimals
        if not lamport:
            lamport = int(float(ui_amount) * (10 ** int(decimals)))
        spl_client = Token(client, pubkey=token_address, program_id=program_id, payer=sender)

        token_account = spl_client.get_accounts_by_owner(owner=receiver_pk).value
        if token_account:
            dest_token_account = token_account[0].pubkey
        else:
            dest_token_account = spl_client.create_associated_token_account(owner=receiver_pk, skip_confirmation=False,
                                                                            recent_blockhash=None)

        tx = spl_client.transfer(source=source_token_account, dest=dest_token_account, owner=sender,
                                 amount=lamport, multi_signers=None, opts=None, recent_blockhash=None).value

        return tx
