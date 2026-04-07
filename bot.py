import os
from http.server import HTTPServer, BaseHTTPRequestHandler
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
def run_web_server():
    port = int(os.environ.get("PORT", 8080))
    server = HTTPServer(('0.0.0.0', port), SimpleHandler)
    print(f"Web server started on port {port}")
import yt_dlp
import os
import uuid
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

TOKEN = "8467075810:AAFn-tDbHMAZ8GhhmdpIK64D3SpawEXT9Ho"

async def download_instagram(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text

    if "instagram.com" not in url:
        await update.message.reply_text("❌ Bu Instagram link emas!")
        return

    await update.message.reply_text("📥 Yuklanmoqda...")

    filename = f"{uuid.uuid4()}.mp4"

    try:
        # Eski fayllarni o‘chirish (MUHIM 🔥)
        for f in os.listdir():
            if f.endswith(".mp4"):
                os.remove(f)

        ydl_opts = {
            'format': 'best',
            'outtmpl': filename,
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'noplaylist': True,
            'quiet': True,
            'no_warnings': True
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        await update.message.reply_video(open(filename, "rb"))

        os.remove(filename)

    except Exception as e:
        print(e)
        await update.message.reply_text("❌ Yuklab bo‘lmadi!")

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), download_instagram))

print("Bot 100% ishlayapti 🚀")
app.run_polling()
import asyncio
import aiohttp
import ffmpeg
import os

# --- 1. Video compress ---
def compress_video(input_path, output_path):
    (
        ffmpeg
        .input(input_path)
        .output(output_path, vcodec='libx264', crf=23, preset='fast', acodec='aac')
        .run(overwrite_output=True)
    )

# --- 2. Async video upload ---
async def async_upload_video(session, video_path):
    url = "https://api.instagram.com/v1/media/upload"  # misol uchun
    files = {'file': open(video_path, 'rb')}
    
    async with session.post(url, data=files) as resp:
        response = await resp.text()
        print(f"{video_path} yuklandi: {response}")

# --- 3. Async boshqaruvchi ---
async def upload_multiple_videos(videos):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for video in videos:
            compressed_path = f"compressed_{os.path.basename(video)}"
            compress_video(video, compressed_path)
            tasks.append(async_upload_video(session, compressed_path))
        await asyncio.gather(*tasks)
        import asyncio
import aiohttp
import ffmpeg
import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

# Instagram API token
INSTAGRAM_TOKEN = os.getenv("INSTAGRAM_TOKEN")
openai_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# --- 1. Video compress ---
def compress_video(input_path, output_path):
    ffmpeg.input(input_path).output(
        output_path, vcodec='libx264', crf=23, preset='fast', acodec='aac'
    ).run(overwrite_output=True)

# --- 2. Thumbnail generator ---
def generate_thumbnail(input_path, thumbnail_path):
    ffmpeg.input(input_path, ss=1).output(thumbnail_path, vframes=1).run(overwrite_output=True)

# --- 3. AI caption generator ---
def generate_caption(video_path):
    prompt = f"Write an engaging Instagram caption and hashtags for the video file {video_path}"
    response = openai_client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content

# --- 4. Async video upload ---
async def async_upload_video(session, video_path, caption):
    url = "https://graph.instagram.com/me/media"  # misol uchun
    files = {'file': open(video_path, 'rb')}
    data = {'caption': caption, 'access_token': INSTAGRAM_TOKEN}
    async with session.post(url, data=data, files=files) as resp:
        result = await resp.text()
        print(f"{video_path} yuklandi: {result}")

# --- 5. Async boshqaruvchi ---
async def upload_multiple_videos(videos):
    async with aiohttp.ClientSession() as session:
        tasks = []
        for video in videos:
            compressed_path = f"compressed_{os.path.basename(video)}"
            thumbnail_path = f"thumb_{os.path.basename(video)}.jpg"
            
            # Video optimizatsiya
            compress_video(video, compressed_path)
            generate_thumbnail(compressed_path, thumbnail_path)
            
            # AI caption
            caption = generate_caption(video)
            
            # Upload task
            tasks.append(async_upload_video(session, compressed_path, caption))
        await asyncio.gather(*tasks)

# --- 6. Video fayllari ro'yxati ---
videos_list = ["video1.mp4", "video2.mp4", "video3.mp4"]

# --- 7. Async ishga tushirish ---
asyncio.run(upload_multiple_videos(videos_list))


