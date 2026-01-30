import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# وظيفة التحميل
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'video.mp4',
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
        return 'video.mp4'

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    
    status_msg = await update.message.reply_text("⏳ جاري التحميل... يرجى الانتظار")
    try:
        file_path = download_video(url)
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ تم التحميل بنجاح")
        os.remove(file_path)
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ حدث خطأ: {str(e)}")

if __name__ == '__main__':
    # ضع توكن البوت الجديد هنا بدقة
    TOKEN = "8351715808:AAHYmi3NxfLYKI6m5kAdh_gO9eWu-tOQ5mQ"
    
    print("البوت بدأ العمل على Railway... ✅")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)
