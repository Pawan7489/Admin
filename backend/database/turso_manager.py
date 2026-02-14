# File: backend/database/turso_manager.py
# Purpose: The "Global Library" for Read-Heavy Data (Blogs/Docs).
# Free Tier: 9 Billion Reads/Month (Virtually Unlimited).
# Technology: LibSQL (Fork of SQLite optimized for Edge).

import libsql_client

class TursoEdgeDatabase:
    def __init__(self, db_url, auth_token):
        """
        Turso Dashboard se Database URL aur Token lein.
        URL format: libsql://dbname-username.turso.io
        """
        self.url = db_url
        self.token = auth_token
        self.client = libsql_client.create_client(self.url, authToken=self.token)
        print("🌍 [Turso]: Edge Database Connected. Ready for 9 Billion Reads.")

    async def initialize_library(self):
        """
        Knowledge Base Table banata hai.
        """
        await self.client.execute("""
            CREATE TABLE IF NOT EXISTS articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                slug TEXT UNIQUE NOT NULL,
                title TEXT NOT NULL,
                content TEXT NOT NULL,
                views INTEGER DEFAULT 0
            )
        """)
        print("📚 [Library]: Shelf is ready.")

    async def publish_article(self, slug, title, content):
        """
        WRITE Operation: Sirf Admin (Aap) karenge.
        Yeh data turant puri duniya ke Edge locations par fail jayega.
        """
        try:
            await self.client.execute(
                "INSERT INTO articles (slug, title, content) VALUES (?, ?, ?)", 
                [slug, title, content]
            )
            print(f"✍️ [Turso]: Article '{title}' published to Edge.")
            return True
        except Exception as e:
            print(f"❌ [Error]: Publish failed. {e}")
            return False

    async def read_article(self, slug):
        """
        READ Operation: Yeh wo function hai jo 9 Billion baar free hai.
        User jab blog kholega, toh yahan se data aayega (Milliseconds mein).
        """
        result = await self.client.execute(
            "SELECT title, content FROM articles WHERE slug = ?", 
            [slug]
        )
        
        if len(result.rows) > 0:
            article = result.rows[0]
            print(f"📖 [Turso]: Serving '{article[0]}' from Edge.")
            
            # (Optional) View Counter update karna - Async background mein
            # await self.client.execute("UPDATE articles SET views = views + 1 WHERE slug = ?", [slug])
            
            return {"title": article[0], "content": article[1]}
        
        return None

# --- Usage Strategy (Async) ---
# import asyncio
# async def main():
#     db = TursoEdgeDatabase("libsql://...", "token")
#     await db.initialize_library()
#     
#     # Admin: Write
#     await db.publish_article("intro-to-a1", "What is A1 OS?", "It is a zero-cost AI...")
#     
#     # User: Read (Super Fast)
#     data = await db.read_article("intro-to-a1")
#     print(data)
#
# asyncio.run(main())
