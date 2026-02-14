# File: backend/memory/qdrant_backup.py
# Purpose: Secondary Memory System (Backup).
# Free Tier Strategy: 1GB RAM Cluster (Enough for ~1M vectors).
# Logic: Same embedding model as Pinecone (all-MiniLM-L6-v2) for compatibility.

import uuid
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from sentence_transformers import SentenceTransformer

class QdrantBackupManager:
    def __init__(self, qdrant_url, qdrant_api_key):
        """
        Qdrant Cloud se connect karta hai aur 'Backup Collection' banata hai.
        """
        self.client = QdrantClient(url=qdrant_url, api_key=qdrant_api_key)
        self.collection_name = "a1_memory_backup"
        
        # Free Embedding Model (Same as Pinecone for consistency)
        self.model = SentenceTransformer('all-MiniLM-L6-v2')

        # Check: Agar collection nahi hai toh banao
        if not self.client.collection_exists(self.collection_name):
            print(f"🎯 [Qdrant]: Initializing Backup Vault '{self.collection_name}'...")
            self.client.create_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )
        else:
            print("✅ [Qdrant]: Backup Vault Connected.")

    def save_backup(self, text_chunk, source="backup"):
        """
        Pinecone fail hone par yahan data save karo.
        """
        print(f"💾 [Qdrant]: Backing up memory: '{text_chunk[:30]}...'")
        
        # 1. Text -> Vector
        vector = self.model.encode(text_chunk).tolist()
        
        # 2. Unique ID (UUID zaroori hai Qdrant ke liye)
        point_id = str(uuid.uuid4())
        
        # 3. Payload (Original Text) ke sath save karo
        operation_info = self.client.upsert(
            collection_name=self.collection_name,
            points=[
                PointStruct(
                    id=point_id, 
                    vector=vector, 
                    payload={"text": text_chunk, "source": source}
                )
            ]
        )
        return "Backup Secured"

    def search_backup(self, query, top_k=3):
        """
        Backup Vault mein search karo.
        """
        print(f"🕵️ [Qdrant]: Searching in Backup for: '{query}'...")
        
        query_vector = self.model.encode(query).tolist()
        
        hits = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        
        # Results extract karna
        results = [hit.payload['text'] for hit in hits]
        
        if not results:
            return "No backup memory found."
            
        return "\n".join(results)

# --- Usage Example (Failover Logic) ---
if __name__ == "__main__":
    # Qdrant Cloud Console se URL aur Key lein
    QDRANT_URL = "https://your-cluster-url.qdrant.io"
    QDRANT_KEY = "th_xxxxxxxxxxxxxxxxxxxxxxxx"
    
    vault = QdrantBackupManager(QDRANT_URL, QDRANT_KEY)
    
    # Scenario: Pinecone Full ho gaya -> Qdrant Activate
    vault.save_backup("Yeh data Pinecone mein fit nahi hua, isliye Qdrant mein rakha hai.")
    
    # Search check
    print(vault.search_backup("Pinecone full hone par kya karein?"))
  
