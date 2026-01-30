import os
import yt_dlp
import asyncio
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# --- دالة التحميل مع كود التمويه ---
def download_media(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'file.mp4',
        'quiet': True,
        'no_warnings': True,
        # هذه الأسطر هي "التمويه" لخداع يوتيوب ومنع الـ 403 Forbidden
        'user_agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36',
        'referer': 'https://www.google.com/',
        'headers': {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'en-us,en;q=0.5',
            'Sec-Fetch-Mode': 'navigate',
        }
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if "http" not in url: return
    
    status_msg = await update.message.reply_text("⏳ جاري المعالجة بنظام التمويه... يرجى الانتظار")
    try:
        path = download_media(url)
        with open(path, 'rb') as video:
            await update.message.reply_video(video=video, caption="✅ تم التحميل بنجاح (نظام التمويه)")
        os.remove(path)
        await status_msg.delete()
    except Exception as e:
        await status_msg.edit_text(f"❌ خطأ: يوتيوب يرفض الاتصال حالياً. جرب تيك توك أو فيسبوك.\n\nالتفاصيل: {str(e)}")

if __name__ == '__main__':
    # تأكد من وضع التوكن الجديد هنا بدقة
    TOKEN = "8351715808:AAHYmi3NxfLYKI6m5kAdh_gO9eWu-tOQ5mQ" # ضع توكنك بالكامل
    
    print("البوت يعمل الآن بنظام التمويه... ✅")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling(drop_pending_updates=True)
