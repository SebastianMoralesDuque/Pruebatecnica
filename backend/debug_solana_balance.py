import os
import django
import sys
from solana.rpc.api import Client
from solders.keypair import Keypair

# Setup Django
sys.path.append('.')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from django.conf import settings

def check_balance():
    rpc_url = getattr(settings, 'SOLANA_RPC_URL', "https://api.devnet.solana.com")
    private_key_hex = getattr(settings, 'SOLANA_PRIVATE_KEY', None)
    
    if not private_key_hex:
        print("ERROR: No SOLANA_PRIVATE_KEY in settings.py")
        return

    client = Client(rpc_url)
    try:
        seed = bytes.fromhex(private_key_hex)
        keypair = Keypair.from_seed(seed)
        pubkey = keypair.pubkey()
        print(f"Public Key: {pubkey}")
        
        balance_resp = client.get_balance(pubkey)
        balance = balance_resp.value / 10**9 # Convert lamports to SOL
        print(f"Balance: {balance} SOL")
        
        if balance == 0:
            print("WARNING: Balance is still 0. Please fund this specific address on Devnet.")
        else:
            print("SUCCESS: Balance is > 0.")
            
    except Exception as e:
        print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    check_balance()
