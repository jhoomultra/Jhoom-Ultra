@@ .. @@
 # Database
 MONGO_DB_URI = config.MONGO_DB_URI
 temp_client = AsyncIOMotorClient(MONGO_DB_URI)
-db = temp_client.YukkiMusic
+db = temp_client.JhoomMusic
 
 StartTime = time.time()
 
 # Clients
 app = Client(
-    "YukkiBot",
+    "JhoomBot",
     api_id=config.API_ID,
     api_hash=config.API_HASH,
     bot_token=config.BOT_TOKEN,
 )
 
 userbot = Client(
-    "YukkiUserBot",
+    "JhoomUserBot",
     api_id=config.API_ID,
     api_hash=config.API_HASH,
     session_string=str(config.STRING1),