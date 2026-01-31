import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- دالة التحميل للمواقع المدعومة ---
def download_media(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'file.mp4',
        'quiet': True,
        'no_warnings': True,
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return

    # --- فحص إذا كان الرابط من يوتيوب ---
    if "youtube.com" in url or "youtu.be" in url:
        await update.message.reply_text(
            "⚠️ نعتذر منك.. التحميل من يوتيوب متوقف حالياً للصيانة.\n\n"
            "✅ يمكنك التحميل من: تيك توك، إنستغرام، فيسبوك، وتويتر."
        )
        return

    status_msg = await update.message.reply_text("⏳ جاري التحميل من العراق... يرجى الانتظار")
    try:
        path = download_media(url)
        with open(path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ تم التحميل بواسطة بوتك")
        os.remove(path)
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ عذراً، هذا الرابط غير مدعوم حالياً أو أنه فيديو خاص.")

if __name__ == '__main__':
    # تأكد من وضع التوكن الخاص بك هنا
    TOKEN = "8351715808:AAHYmi3NxfLYKI6m5kAdh_gO9eWu-tOQ5mQ" 
    
    print("البوت يعمل الآن باحترافية... 🚀")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)
