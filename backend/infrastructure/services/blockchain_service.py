import hashlib
from django.conf import settings
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction
from solders.message import Message
from solders.transaction import Transaction
from shared_domain.exceptions import InfrastructureError

class BlockchainService:
    @staticmethod
    def certify_data(data_string):
        data_hash = hashlib.sha256(data_string.encode()).hexdigest()
        
        if not settings.SOLANA_PRIVATE_KEY:
            return {
                "txHash": f"dummy_{data_hash[:10]}",
                "pdf_hash": data_hash,
                "status": "DUMMY_SUCCESS"
            }

        try:
            client = Client(settings.SOLANA_RPC_URL)
            # Try to load as hex (seed)
            try:
                private_key_bytes = bytes.fromhex(settings.SOLANA_PRIVATE_KEY)
                if len(private_key_bytes) == 64:
                    keypair = Keypair.from_bytes(private_key_bytes)
                else:
                    keypair = Keypair.from_seed(private_key_bytes[:32])
            except ValueError:
                # If not hex, try base58 or other formats if needed, but hex is common in these tests
                raise InfrastructureError("La llave privada de Solana no tiene un formato hexadecimal válido.")
            
            # Standard Solana Memo Program (This one is valid Base58)
            memo_program_id = Pubkey.from_string("MemoSq4gqABAXKb96qnH8TysNcWxMyWCqXgDLGmfcHr")
            memo_instruction = Instruction(memo_program_id, data_hash.encode('utf-8'), [])
            
            print(f"Certifying hash: {data_hash} with pubkey: {keypair.pubkey()}")
            
            # Fetch blockhash
            try:
                blockhash_resp = client.get_latest_blockhash()
                blockhash = blockhash_resp.value.blockhash
            except Exception as e:
                raise InfrastructureError(f"No se pudo obtener el blockhash de Solana: {str(e)}")
            
            message = Message.new_with_blockhash([memo_instruction], keypair.pubkey(), blockhash)
            txn = Transaction([keypair], message, blockhash)
            
            try:
                response = client.send_transaction(txn)
                tx_hash = str(response.value)
            except Exception as e:
                raise InfrastructureError(f"Error al enviar la transacción a Solana: {str(e)}")
            
            return {
                "status": "SUCCESS",
                "txHash": tx_hash,
                "pdf_hash": data_hash
            }
        except Exception as e:
            import traceback
            print(f"Solana Error Traceback:")
            traceback.print_exc()
            if isinstance(e, InfrastructureError):
                raise e
            raise InfrastructureError(f"Fallo en la comunicación con Solana: {str(e)}")
