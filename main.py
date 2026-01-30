import os
import yt_dlp
from telegram import Update
from telegram.ext import Application, MessageHandler, filters, ContextTypes

# إعدادات التحميل
def download_video(url):
    ydl_opts = {
        'format': 'best',
        'outtmpl': 'downloaded_video.%(ext)s',
        'max_filesize': 50 * 1024 * 1024,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info)

# وظيفة الرد على الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url.startswith("http"):
        await update.message.reply_text("من فضلك أرسل رابط فيديو صحيح 🔗")
        return

    msg = await update.message.reply_text("جاري التحميل والمعالجة... ⏳")

    try:
        file_path = download_video(url)
        with open(file_path, 'rb') as video:
            await update.message.reply_video(video=video, caption="تم التحميل بنجاح ✅")
        
        if os.path.exists(file_path):
            os.remove(file_path)
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"عذراً، حدث خطأ: {str(e)}")

# تشغيل البوت
if __name__ == '__main__':
    # استبدل النص أدناه بالتوكن الحقيقي من BotFather
    TOKEN = "8200389717:AAGTh9os6c0QouFzvPnt0B6lGTlcNVNPNfI"
    
    print("البوت يعمل الآن...")
    app = Application.builder().token(TOKEN).build()
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()


