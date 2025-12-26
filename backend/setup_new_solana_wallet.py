import json
from solana.rpc.api import Client
from solders.keypair import Keypair
from solders.pubkey import Pubkey
import time

def setup():
    client = Client("https://api.devnet.solana.com")
    
    # 1. Generate new Keypair
    kp = Keypair()
    pubkey = kp.pubkey()
    # Private key as hex (32 bytes seed)
    private_key_hex = kp.secret().hex()
    
    print(f"NEW_ADDRESS:{pubkey}")
    print(f"NEW_PRIVATE_KEY_HEX:{private_key_hex}")
    
    # 2. Request Airdrop
    print("Requesting airdrop of 1 SOL...")
    try:
        resp = client.request_airdrop(pubkey, 1_000_000_000)
        signature = resp.value
        print(f"Airdrop signature: {signature}")
        
        # Wait for confirmation
        print("Waiting for confirmation...")
        time.sleep(10)
        
        balance = client.get_balance(pubkey).value
        print(f"Final Balance: {balance / 10**9} SOL")
        
        if balance > 0:
            print("SETUP_SUCCESS")
        else:
            print("SETUP_PENDING_CONFIRMATION")
            
    except Exception as e:
        print(f"SETUP_ERROR: {str(e)}")

if __name__ == "__main__":
    setup()
