
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes
import os

# Token dan ID admin
TOKEN = os.getenv("TOKEN", "YOUR_BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID", "123456789"))
USER_DB = "users.txt"

# Simpan ID user
def save_user_id(user_id):
    if not os.path.exists(USER_DB):
        open(USER_DB, "w").close()
    with open(USER_DB, "r+") as f:
        users = f.read().splitlines()
        if str(user_id) not in users:
            f.write(f"{user_id}\n")

# /start handler
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user_id(user.id)
    first_name = user.first_name

    text = (
        f"Hai {first_name}!

"
        "Punya group dan akun lama yang udah ga kepake??\n"
        "Daripada penuh-penuhin hp, mending jual aja di sini. Selain bisa ditukar jadi saldo e-wallet, "
        "kamu juga bisa tukar jadi diamond game, Stars Telegram, bahkan bisa tukar Telegram Premium!!!\n\n"
        "Klik tombol di bawah buat cek Price & Format, Tutor TFO, dan Testimoni 👇👇"
    )

    keyboard = [
        [InlineKeyboardButton("💰 Price & Format", url="https://t.me/opencvdanjualbeligc/375")],
        [InlineKeyboardButton("📘 Tutor TFO", url="https://t.me/opencvdanjualbeligc/381")],
        [InlineKeyboardButton("🗣 Testimoni", url="https://t.me/opencvdanjualbeligc/360")],
        [InlineKeyboardButton("📩 Kontak Admin", url="https://t.me/kingsdarkhole")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode='Markdown')

# Broadcast pesan ke semua user
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return await update.message.reply_text("Kamu bukan admin.")
    if not context.args:
        return await update.message.reply_text("Gunakan: /broadcast isi_pesan")

    message = " ".join(context.args)
    with open(USER_DB, "r") as f:
        user_ids = f.read().splitlines()

    success, fail = 0, 0
    for uid in user_ids:
        try:
            await context.bot.send_message(chat_id=int(uid), text=message)
            success += 1
        except:
            fail += 1
    await update.message.reply_text(f"Broadcast berhasil: {success}, Gagal: {fail}")

# Forward pesan user ke admin
async def forward_to_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    save_user_id(user.id)
    prefix = f"[From {user.first_name} | ID: {user.id}]"
    await context.bot.send_message(chat_id=ADMIN_ID, text=prefix)
    await update.message.forward(chat_id=ADMIN_ID)

# Admin membalas ke user
async def reply_from_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID:
        return
    if update.message.reply_to_message:
        try:
            if "ID:" in update.message.reply_to_message.text:
                uid = int(update.message.reply_to_message.text.split("ID:")[1].split("]")[0])
                await context.bot.send_message(chat_id=uid, text=update.message.text)
        except:
            pass

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(MessageHandler(filters.TEXT & (~filters.COMMAND), forward_to_admin))
    app.add_handler(MessageHandler(filters.TEXT & filters.REPLY, reply_from_admin))
    print("Bot sedang berjalan...")
    app.run_polling()
