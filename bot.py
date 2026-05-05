import sqlite3
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8776783368:AAEtA4NdbbL9QpZz6UQ1VBZE8qFDHavf2Eg"
ADMIN_ID = 7891796604

conn = sqlite3.connect("database.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS numbers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    number TEXT,
    status TEXT
)
""")
conn.commit()

# ---------------- CHECK ADMIN ----------------
def is_admin(user_id):
    return user_id == ADMIN_ID

# ---------------- START ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        await update.message.reply_text("Access denied.")
        return

    await update.message.reply_text(
        "Admin Panel Active\n\nCommands:\n/add <number>\n/list"
    )

# ---------------- ADD NUMBER ----------------
async def add(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    try:
        number = context.args[0]

        cursor.execute(
            "INSERT INTO numbers (number, status) VALUES (?, ?)",
            (number, "active")
        )
        conn.commit()

        await update.message.reply_text("Saved.")

    except:
        await update.message.reply_text("Usage: /add <number>")

# ---------------- LIST ----------------
async def list_data(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update.effective_user.id):
        return

    cursor.execute("SELECT number, status FROM numbers")
    rows = cursor.fetchall()

    text = "DATA:\n\n"
    for r in rows:
        text += f"{r[0]} - {r[1]}\n"

    await update.message.reply_text(text)

# ---------------- MAIN ----------------
def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("add", add))
    app.add_handler(CommandHandler("list", list_data))

    print("Bot running...")
    app.run_polling(
         drop_pending_updates=True
)

if __name__ == "__main__":
    main()
