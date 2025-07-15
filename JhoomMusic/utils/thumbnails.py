import os
import re
import textwrap
import aiofiles
import aiohttp
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont
from youtubesearchpython.__future__ import VideosSearch
from config import MUSIC_BOT_NAME, YOUTUBE_IMG_URL
from JhoomMusic import app

def changeImageSize(maxWidth, maxHeight, image):
    widthRatio = maxWidth / image.size[0]
    heightRatio = maxHeight / image.size[1]
    newWidth = int(widthRatio * image.size[0])
    newHeight = int(heightRatio * image.size[1])
    newImage = image.resize((newWidth, newHeight))
    return newImage

async def gen_thumb(videoid):
    if os.path.isfile(f"cache/{videoid}.png"):
        return f"cache/{videoid}.png"
    
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(f"cache/thumb{videoid}.png", mode="wb")
                        await f.write(await resp.read())
                        await f.close()
            
            try:
                wxyz = await app.get_profile_photos(app.id)
                wxy = await app.download_media(wxyz[0]['file_id'], file_name=f'{app.id}.jpg')
            except:
                wxy = f"assets/global.png"
            
            xy = Image.open(wxy)
            y = Image.open(f"cache/thumb{videoid}.png")
            y = y.resize((1280, 720))
            
            # Create gradient background
            background = Image.new('RGB', (1280, 720), (0, 0, 0))
            draw = ImageDraw.Draw(background)
            
            # Add gradient effect
            for i in range(720):
                alpha = int(255 * (i / 720))
                draw.line([(0, i), (1280, i)], fill=(alpha//4, alpha//8, alpha//6))
            
            # Paste thumbnail with transparency
            background.paste(y, (0, 0))
            
            # Add overlay
            overlay = Image.new('RGBA', (1280, 720), (0, 0, 0, 100))
            background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
            
            # Add profile picture
            xy = xy.resize((150, 150))
            mask = Image.new('L', (150, 150), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 150, 150), fill=255)
            background.paste(xy, (50, 500), mask)
            
            # Add text
            draw = ImageDraw.Draw(background)
            
            try:
                font = ImageFont.truetype("assets/font2.ttf", 70)
                font2 = ImageFont.truetype("assets/font2.ttf", 50)
                arial = ImageFont.truetype("assets/font2.ttf", 30)
                name_font = ImageFont.truetype("assets/font.ttf", 40)
            except:
                font = ImageFont.load_default()
                font2 = ImageFont.load_default()
                arial = ImageFont.load_default()
                name_font = ImageFont.load_default()
            
            # Draw title
            para = textwrap.wrap(title, width=32)
            j = 0
            for line in para:
                if j == 1:
                    j += 1
                    draw.text((2, 2), line, fill="black", font=font)
                    draw.text((0, 0), line, fill="white", font=font)
                    break
                draw.text((2, 2), line, fill="black", font=font)
                draw.text((0, 0), line, fill="white", font=font)
                j += 1
            
            # Draw channel name
            draw.text((52, 670), f"Channel: {channel}", fill="white", font=arial)
            
            # Draw duration and views
            draw.text((52, 620), f"Duration: {duration} Mins", fill="white", font=arial)
            draw.text((52, 645), f"Views: {views}", fill="white", font=arial)
            
            # Draw bot name
            draw.text((220, 530), f"Playing on {MUSIC_BOT_NAME}", fill="white", font=name_font)
            
            try:
                os.remove(f"cache/thumb{videoid}.png")
            except:
                pass
            
            background.save(f"cache/{videoid}.png")
            return f"cache/{videoid}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL

async def gen_qthumb(videoid):
    if os.path.isfile(f"cache/que_{videoid}.png"):
        return f"cache/que_{videoid}.png"
    
    url = f"https://www.youtube.com/watch?v={videoid}"
    try:
        results = VideosSearch(url, limit=1)
        for result in (await results.next())["result"]:
            try:
                title = result["title"]
                title = re.sub("\W+", " ", title)
                title = title.title()
            except:
                title = "Unsupported Title"
            
            try:
                duration = result["duration"]
            except:
                duration = "Unknown Mins"
            
            thumbnail = result["thumbnails"][0]["url"].split("?")[0]
            
            try:
                views = result["viewCount"]["short"]
            except:
                views = "Unknown Views"
            
            try:
                channel = result["channel"]["name"]
            except:
                channel = "Unknown Channel"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(thumbnail) as resp:
                    if resp.status == 200:
                        f = await aiofiles.open(f"cache/qthumb{videoid}.png", mode="wb")
                        await f.write(await resp.read())
                        await f.close()
            
            try:
                wxyz = await app.get_profile_photos(app.id)
                wxy = await app.download_media(wxyz[0]['file_id'], file_name=f'{app.id}_queue.jpg')
            except:
                wxy = f"assets/global.png"
            
            xy = Image.open(wxy)
            y = Image.open(f"cache/qthumb{videoid}.png")
            y = y.resize((1280, 720))
            
            # Create queue-specific design
            background = Image.new('RGB', (1280, 720), (20, 20, 30))
            draw = ImageDraw.Draw(background)
            
            # Add gradient
            for i in range(720):
                alpha = int(100 * (i / 720))
                draw.line([(0, i), (1280, i)], fill=(alpha//2, alpha//3, alpha//2))
            
            # Paste thumbnail
            background.paste(y, (0, 0))
            
            # Add "QUEUED" overlay
            overlay = Image.new('RGBA', (1280, 720), (255, 0, 0, 80))
            background = Image.alpha_composite(background.convert('RGBA'), overlay).convert('RGB')
            
            # Add profile picture
            xy = xy.resize((120, 120))
            mask = Image.new('L', (120, 120), 0)
            draw_mask = ImageDraw.Draw(mask)
            draw_mask.ellipse((0, 0, 120, 120), fill=255)
            background.paste(xy, (1100, 550), mask)
            
            # Add text
            draw = ImageDraw.Draw(background)
            
            try:
                font = ImageFont.truetype("assets/font2.ttf", 60)
                font2 = ImageFont.truetype("assets/font2.ttf", 40)
                arial = ImageFont.truetype("assets/font2.ttf", 25)
            except:
                font = ImageFont.load_default()
                font2 = ImageFont.load_default()
                arial = ImageFont.load_default()
            
            # Draw "QUEUED" text
            draw.text((52, 52), "QUEUED", fill="red", font=font)
            draw.text((50, 50), "QUEUED", fill="white", font=font)
            
            # Draw title
            para = textwrap.wrap(title, width=35)
            j = 0
            for line in para:
                if j == 2:
                    break
                draw.text((52, 150 + (j * 40)), line, fill="white", font=font2)
                j += 1
            
            # Draw details
            draw.text((52, 600), f"Channel: {channel}", fill="white", font=arial)
            draw.text((52, 625), f"Duration: {duration}", fill="white", font=arial)
            draw.text((52, 650), f"Views: {views}", fill="white", font=arial)
            
            try:
                os.remove(f"cache/qthumb{videoid}.png")
            except:
                pass
            
            background.save(f"cache/que_{videoid}.png")
            return f"cache/que_{videoid}.png"
    except Exception as e:
        print(e)
        return YOUTUBE_IMG_URL