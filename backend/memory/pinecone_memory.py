# File: backend/memory/pinecone_memory.py
# Purpose: Gives the AI "Long-Term Memory" using Pinecone Vector DB.
# Free Tier Strategy: Uses 'all-MiniLM-L6-v2' (Free local embedding) + Pinecone Starter Index.

import os
import time
from pinecone import Pinecone, ServerlessSpec
from sentence_transformers import SentenceTransformer

class PineconeMemoryManager:
    def __init__(self, api_key, index_name="a1-os-memory"):
        """
        Pinecone aur Embedding Model ko initialize karta hai.
        Model: 'all-MiniLM-L6-v2' (Bahut fast aur lightweight hai, CPU par bhi chalta hai).
        """
        self.pc = Pinecone(api_key=api_key)
        self.index_name = index_name
        
        # Free Embedding Model load karna (No OpenAI Cost)
        print("🧠 [Memory]: Loading embedding model (all-MiniLM-L6-v2)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2') 
        
        # Index Check: Agar index nahi hai toh naya banao
        existing_indexes = [i.name for i in self.pc.list_indexes()]
        
        if index_name not in existing_indexes:
            print(f"🌲 [Pinecone]: Creating new Index '{index_name}'...")
            self.pc.create_index(
                name=index_name,
                dimension=384, # MiniLM model ka output size 384 hota hai
                metric='cosine', # Similarity napne ka tarika
                spec=ServerlessSpec(cloud='aws', region='us-east-1') # Free Tier region
            )
            time.sleep(10) # Index ready hone ka wait

        self.index = self.pc.Index(index_name)
        print("✅ [Pinecone]: Memory System Connected.")

    def store_memory(self, text_chunk, source_id="unknown"):
        """
        Text -> Vector -> Pinecone Storage.
        Jab AI kuch padhta hai, toh yahan save karta hai.
        """
        print(f"📥 [Memory]: Memorizing: '{text_chunk[:30]}...'")
        
        # 1. Text ko Numbers (Vector) mein badlo
        vector = self.model.encode(text_chunk).tolist()
        
        # 2. Unique ID banao (Simple hash for now)
        vector_id = str(hash(text_chunk))
        
        # 3. Pinecone mein daalo (Metadata ke sath)
        self.index.upsert(
            vectors=[{
                "id": vector_id, 
                "values": vector, 
                "metadata": {"text": text_chunk, "source": source_id}
            }]
        )
        return "Memorized"

    def recall_memory(self, user_query, top_k=3):
        """
        User ke sawal se related purani yaadein wapas lata hai.
        """
        print(f"🔍 [Memory]: Thinking about: '{user_query}'...")
        
        # 1. Sawal ko bhi vector mein badlo
        query_vector = self.model.encode(user_query).tolist()
        
        # 2. Pinecone mein search karo (Sabse milta-julta vector dhundo)
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )
        
        # 3. Result mein se text nikalo
        contexts = [match['metadata']['text'] for match in results['matches']]
        
        if not contexts:
            return "No relevant memory found."
            
        print(f"💡 [Memory]: Found {len(contexts)} relevant memories.")
        return "\n".join(contexts)

# --- Usage Example (Master Terminal se call hoga) ---
if __name__ == "__main__":
    # Pinecone Console se free API Key lein
    MY_API_KEY = "pc_sk_xxxxxxxxxxxxxxxxxxxxxxxx" 
    
    brain = PineconeMemoryManager(MY_API_KEY)
    
    # Scene 1: AI ko sikhana (Storing)
    brain.store_memory("Project A1 ek Zero-Investment AI Operating System hai.", source_id="project_doc")
    brain.store_memory("Admin Panel ka naam 'God Mode' hai.", source_id="project_doc")
    
    # Scene 2: AI se puchna (Retrieving)
    answer = brain.recall_memory("A1 OS kya hai?")
    print(f"\n🤖 Context Retrieved:\n{answer}")
  
