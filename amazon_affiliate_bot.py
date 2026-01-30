import re
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

BOT_TOKEN = "8537791968:AAEBZ84GuYQ4x0r28ASb jQkbVOB7hFJBHrQ"

AFFILIATE_TAG = "flowback-21"
AMAZON_DOMAIN = "amazon.in"

DISCLOSURE = "\n\n⚠️ As an Amazon Associate, I earn from qualifying purchases."

# ---------- UTIL FUNCTIONS ----------

def resolve_url(url: str) -> str:
    try:
        r = requests.get(url, allow_redirects=True, timeout=10)
        return r.url
    except:
        return url


def extract_asin(url: str):
    patterns = [
        r"/dp/([A-Z0-9]{10})",
        r"/gp/product/([A-Z0-9]{10})",
        r"/product/([A-Z0-9]{10})",
    ]

    for p in patterns:
        m = re.search(p, url)
        if m:
            return m.group(1)

    return None


def build_affiliate_link(asin: str):
    return f"https://www.amazon.in/dp/{asin}?tag={AFFILIATE_TAG}"


# ---------- BOT HANDLERS ----------

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "👋 Send me any Amazon India product link and I’ll convert it to an affiliate link."
    )


async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip()

    if "amazon." not in text and "amzn." not in text:
        await update.message.reply_text("❌ Please send a valid Amazon link.")
        return

    final_url = resolve_url(text)

    if AMAZON_DOMAIN not in final_url:
        await update.message.reply_text("❌ Currently only Amazon India links are supported.")
        return

    asin = extract_asin(final_url)

    if not asin:
        await update.message.reply_text("⚠️ Could not detect product ASIN in that link.")
        return

    affiliate_url = build_affiliate_link(asin)

    reply = f"✅ Your Affiliate Link:\n\n{affiliate_url}{DISCLOSURE}"

    await update.message.reply_text(reply)


# ---------- MAIN ----------

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot running...")
    app.run_polling()


if __name__ == "__main__":
    main()
