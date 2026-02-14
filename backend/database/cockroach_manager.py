# File: backend/database/cockroach_manager.py
# Purpose: The "Unkillable" Database for Critical Data (Finance/Auth).
# Free Tier: 5GB Storage & 250M Request Units (Serverless).
# Logic: Uses PostgreSQL syntax but runs on distributed CockroachDB nodes.

import psycopg2
from psycopg2 import errorcodes
import time
import uuid

class CockroachDBManager:
    def __init__(self, connection_string):
        """
        Secure connection string CockroachDB Console se milega.
        Format: postgresql://<user>:<password>@<host>:<port>/<cluster>?sslmode=verify-full
        """
        self.conn_str = connection_string
        self.conn = self._connect()

    def _connect(self):
        """Secure connection banata hai."""
        try:
            conn = psycopg2.connect(self.conn_str)
            print("🪳 [CockroachDB]: The Iron Vault is Open & Connected.")
            return conn
        except Exception as e:
            print(f"❌ [Error]: Connection failed. {e}")
            return None

    def initialize_tables(self):
        """
        Critical tables banata hai agar wo exist nahi karte.
        """
        commands = [
            """
            CREATE TABLE IF NOT EXISTS users (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                username STRING NOT NULL,
                email STRING UNIQUE NOT NULL,
                balance DECIMAL(10, 2) DEFAULT 0.00
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS transactions (
                id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
                sender_id UUID REFERENCES users(id),
                receiver_id UUID REFERENCES users(id),
                amount DECIMAL(10, 2),
                timestamp TIMESTAMP DEFAULT now()
            )
            """
        ]
        try:
            with self.conn.cursor() as cur:
                for cmd in commands:
                    cur.execute(cmd)
            self.conn.commit()
            print("✅ [Vault]: Tables Verified.")
        except Exception as e:
            print(f"❌ [Error]: Table creation failed. {e}")

    def execute_transaction(self, sender_id, receiver_id, amount):
        """
        MASTER FUNCTION: Financial Transaction (Atomic).
        Agar beech mein light gayi ya internet kta, toh pura transaction cancel hoga.
        Paisa hawa mein gayab nahi hoga.
        """
        print(f"💸 [Finance]: Moving ${amount} from {sender_id} to {receiver_id}...")
        
        try:
            with self.conn.cursor() as cur:
                # 1. Check Sender Balance
                cur.execute("SELECT balance FROM users WHERE id = %s", (sender_id,))
                sender_balance = cur.fetchone()[0]

                if sender_balance < amount:
                    print("⚠️ [Finance]: Insufficient Funds.")
                    self.conn.rollback()
                    return False

                # 2. Deduct from Sender
                cur.execute("UPDATE users SET balance = balance - %s WHERE id = %s", (amount, sender_id))
                
                # 3. Add to Receiver
                cur.execute("UPDATE users SET balance = balance + %s WHERE id = %s", (amount, receiver_id))
                
                # 4. Record Log
                cur.execute("INSERT INTO transactions (sender_id, receiver_id, amount) VALUES (%s, %s, %s)", 
                            (sender_id, receiver_id, amount))

            # 5. Commit (Final Mohar)
            self.conn.commit()
            print("✅ [Finance]: Transaction Successful.")
            return True

        except Exception as e:
            print(f"❌ [Error]: Transaction Failed. Rolling back... {e}")
            self.conn.rollback() # Sab kuch wapas pehle jaisa ho jayega
            return False

# --- Usage Example (Master Logic) ---
if __name__ == "__main__":
    # CockroachDB se mila hua URL
    CONN_STRING = "postgresql://user:pass@free-tier.cockroachlabs.cloud:26257/defaultdb?sslmode=verify-full"
    
    vault = CockroachDBManager(CONN_STRING)
    vault.initialize_tables()
    
    # Test Transaction
    # vault.execute_transaction(sender_uuid, receiver_uuid, 50.00)
  
