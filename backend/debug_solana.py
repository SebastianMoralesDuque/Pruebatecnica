import os
import django
import sys
from io import BytesIO
import hashlib
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
from solders.instruction import Instruction as SInstruction
from solders.message import Message
from solders.transaction import Transaction

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings
from management.models import Producto

def test_certify():
    print("Testing Certification Logic...")
    try:
        pdf_hash = hashlib.sha256(b"test_content").hexdigest()
        rpc_url = getattr(settings, 'SOLANA_RPC_URL', "https://api.devnet.solana.com")
        private_key_hex = "64f3c2622c69b547fb467335870182ddefa57b5f5abe910f49019c443f6559af"
        
        client = Client(rpc_url)
        seed = bytes.fromhex(private_key_hex)
        keypair = Keypair.from_seed(seed)
        print(f"Keypair pubkey: {keypair.pubkey()}")
        
        memo_program_id = Pubkey.from_string("MemoSq4gqABvAn9NoSKeyJv6Ysl7R8L34KxyTqQuX9A")
        memo_instruction = SInstruction(
            memo_program_id,
            pdf_hash.encode('utf-8'),
            []
        )
        
        blockhash_resp = client.get_latest_blockhash()
        recent_blockhash = blockhash_resp.value.blockhash
        print(f"Recent blockhash: {recent_blockhash}")
        
        message = Message.new_with_blockhash(
            [memo_instruction],
            keypair.pubkey(),
            recent_blockhash
        )
        
        txn = Transaction([keypair], message, recent_blockhash)
        print("Transaction constructed and signed.")
        
        response = client.send_transaction(txn)
        print(f"Transaction response: {response}")
        
    except Exception as e:
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_certify()
