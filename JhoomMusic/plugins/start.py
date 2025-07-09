@@ .. @@
 from pyrogram import filters
 from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message
 
-from YukkiMusic import app
-from YukkiMusic.utils.database import add_served_chat, add_served_user
+from JhoomMusic import app
+from JhoomMusic.utils.database import add_served_chat, add_served_user
 from config import BANNED_USERS
 
@@ .. @@
     await message.reply_text(
-        f"🎵 **Welcome to Yukki Music Bot!**\n\n"
+        f"🎵 **Welcome to Jhoom Music Bot!**\n\n"
         f"I can play music in your group's voice chat.\n\n"
         f"**Commands:**\n"
@@ .. @@
                 ],
                 [
                     InlineKeyboardButton(
-                        "📨 Support Group", url="https://t.me/YukkiSupport"
+                        "📨 Support Group", url="https://t.me/JhoomSupport"
                     ),
                     InlineKeyboardButton(
-                        "📢 Updates Channel", url="https://t.me/TeamYukki"
+                        "📢 Updates Channel", url="https://t.me/TeamJhoom"
                     ),
                 ],
             ]
@@ .. @@
 async def help_command(client, message: Message):
     await message.reply_text(
-        "🎵 **Yukki Music Bot Help**\n\n"
+        "🎵 **Jhoom Music Bot Help**\n\n"
         "**Basic Commands:**\n"