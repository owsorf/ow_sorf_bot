import telebot
from flask import Flask
from threading import Thread

# هذا هو توكنك بدون فراغات
TOKEN = "7717905111:AAHJwEsDLpjAfE3oSVc6g6cc3rdF13W9U9g"

bot = telebot.TeleBot(TOKEN)

# سيرفر صغير عشان يبقي البوت شغال
app = Flask('')

@app.route('/')
def home():
    return "I'm alive"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# البوت نفسه
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    try:
        # يقسم النص بناءً على السطر (Enter)
        lines = message.text.strip().split('\n')

        if len(lines) != 2:
            bot.reply_to(message, "❌ أرسل السعر فوق والسعر تحت.\nمثال:\n300\n175")
            return

        sell_price = float(lines[0].strip())
        cost_price = float(lines[1].strip())

        profit = sell_price - cost_price
        products_share = profit * 0.8
        ads_share = profit * 0.15
        bonus_share = profit * 0.05

        reply = f"""✅ صافي الربح: {profit:.2f} ريال
➡️ مخصص للمنتجات (80%): {products_share:.2f} ريال
➡️ مخصص للإعلانات (15%): {ads_share:.2f} ريال
➡️ مكافأة شخصية (5%): {bonus_share:.2f} ريال"""

        bot.reply_to(message, reply)

    except Exception as e:
        print("Error:", e)
        bot.reply_to(message, "❌ تأكد أنك أرسلت رقمين صحيحين فوق بعض.\nمثال:\n300\n175")

# تشغيل السيرفر + تشغيل البوت
keep_alive()
bot.infinity_polling()
