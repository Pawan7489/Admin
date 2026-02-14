# File: backend/admin_panel/algolia_search_engine.py
# Purpose: Provides "Lightning Fast" search for the Admin Panel.
# Free Tier: 10k Records & 100k Searches/month.
# Logic: Syncs metadata from MongoDB to Algolia for instant retrieval.

from algoliasearch.search_client import SearchClient

class AlgoliaSearchEngine:
    def __init__(self, app_id, api_key):
        """
        Algolia Client initialize karta hai.
        app_id & api_key: Algolia Dashboard se milega.
        """
        self.client = SearchClient.create(app_id, api_key)
        
        # Hum do alag indices banayenge: Users aur Files ke liye
        self.user_index = self.client.init_index('a1_users')
        self.file_index = self.client.init_index('a1_files')
        
        # Search settings optimize karna (Typos allow karna, etc.)
        self.file_index.set_settings({
            'searchableAttributes': ['filename', 'type', 'tags'],
            'customRanking': ['desc(upload_date)']
        })
        print("⚡ [Algolia]: Instant Search Engine Ready.")

    def index_new_file(self, file_id, filename, file_type, tags=[]):
        """
        Jab koi nayi file upload ho (MongoDB mein), toh yahan bhi register karo.
        """
        record = {
            'objectID': str(file_id), # MongoDB ID hi objectID banega
            'filename': filename,
            'type': file_type,
            'tags': tags,
            'upload_date': 20260214 # Example timestamp
        }
        
        try:
            self.file_index.save_object(record).wait()
            print(f"🔍 [Algolia]: Indexed File: {filename}")
            return True
        except Exception as e:
            print(f"❌ [Error]: Indexing failed. {e}")
            return False

    def instant_search(self, query, category="files"):
        """
        Admin Panel ke Search Bar mein type karte hi result layega.
        """
        print(f"🚀 [Algolia]: Searching for '{query}' in {category}...")
        
        target_index = self.user_index if category == "users" else self.file_index
        
        # Millisecond search execution
        results = target_index.search(query)
        
        hits = results['hits']
        print(f"✅ [Algolia]: Found {len(hits)} matches in {results['processingTimeMS']}ms.")
        
        # Sirf zaroori data return karo
        return hits

    def delete_record(self, object_id, category="files"):
        """
        Agar file delete ho gayi, toh search result se bhi hatao.
        """
        target_index = self.user_index if category == "users" else self.file_index
        target_index.delete_object(object_id)
        print(f"🗑️ [Algolia]: Removed record {object_id} from search.")

# --- Usage Example (Admin Panel Logic) ---
if __name__ == "__main__":
    # Algolia Keys (Dashboard se lein)
    APP_ID = "YourAppID"
    API_KEY = "YourAdminAPIKey"
    
    search_engine = AlgoliaSearchEngine(APP_ID, API_KEY)
    
    # Scenario 1: Nayi File Upload hui
    search_engine.index_new_file(
        file_id="mongo_id_12345",
        filename="Project_A1_Blueprint.pdf",
        file_type="document",
        tags=["important", "blueprint"]
    )
    
    # Scenario 2: Admin ne search kiya "Blue"
    # Result turant aayega bina DB query ke
    results = search_engine.instant_search("Blue")
    
    for hit in results:
        print(f"📄 Found: {hit['filename']} (Type: {hit['type']})")
      
