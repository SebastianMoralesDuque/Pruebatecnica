import hashlib
import traceback
from django.conf import settings
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.message import Message
from solders.transaction import Transaction

class BlockchainService:
    @staticmethod
    def certify_data(data_to_hash):
        pdf_hash = hashlib.sha256(data_to_hash.encode()).hexdigest()
        
        rpc_url = getattr(settings, 'SOLANA_RPC_URL', "https://api.devnet.solana.com")
        private_key_hex = getattr(settings, 'SOLANA_PRIVATE_KEY', None)

        if not private_key_hex or "REEMPLAZAR" in private_key_hex:
            return {
                "status": "SIMULATED",
                "txHash": "SIMULATED_TX_HASH",
                "pdf_hash": pdf_hash
            }

        try:
            client = Client(rpc_url)
            seed = bytes.fromhex(private_key_hex)
            keypair = Keypair.from_seed(seed)
            
            memo_program_id = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")
            memo_instruction = Instruction(memo_program_id, pdf_hash.encode('utf-8'), [])
            
            blockhash = client.get_latest_blockhash().value.blockhash
            message = Message.new_with_blockhash([memo_instruction], keypair.pubkey(), blockhash)
            txn = Transaction([keypair], message, blockhash)
            
            response = client.send_transaction(txn)
            tx_hash = str(response.value)
            
            return {
                "status": "SUCCESS",
                "txHash": tx_hash,
                "pdf_hash": pdf_hash
            }
        except Exception as e:
            traceback.print_exc()
            raise Exception(f"Error Solana: {str(e)}")
