import requests
import time

TOKEN = '537891055:oofPfHUKYmmJNhJ9UdhBDwsexghl2ovK9pcqHXAa'
URL = f"https://tapi.bale.ai/bot{TOKEN}/"

# فهرست آزمون‌ها با لینک و هزینه تحلیل
tests = {
    "آزمون NEO": ("https://shivapsy.ir/form-test/?form_id=22", "2,500,000 ریال"),
    "آزمون MMPI-2 فرم کوتاه": ("https://shivapsy.ir/form-test/?form_id=1", "2,500,000 ریال"),
    "آزمون گودیناف": ("https://shivapsy.ir/form-test/?form_id=21", "2,500,000 ریال"),
    "آزمون سلامت عمومی GHQ": ("https://shivapsy.ir/form-test/?form_id=7", "1,000,000 ریال"),
    "آزمون رغبت سنج هالند": ("https://shivapsy.ir/form-test/?form_id=3", "2,000,000 ریال"),
    "آزمون هوش هیجانی بار-ان": ("https://shivapsy.ir/form-test/?form_id=4", "1,500,000 ریال"),
    "آزمون SCL-90": ("https://shivapsy.ir/form-test/?form_id=6", "1,500,000 ریال"),
    "آزمون هوش چندگانه": ("https://shivapsy.ir/form-test/?form_id=11", "1,500,000 ریال"),
    "آزمون ریون رنگی کودکان": ("https://shivapsy.ir/form-test/?form_id=24", "2,500,000 ریال"),
    "پرسشنامه شغلی": ("https://shivapsy.ir/form-test/?form_id=25", "2,000,000 ریال"),
    "فرم بلند پرسشنامه استرانگ": ("https://shivapsy.ir/form-test/?form_id=2", "2,000,000 ریال"),
    "پرسشنامه رغبت‌سنج": ("https://shivapsy.ir/form-test/?form_id=10", "2,000,000 ریال")
}

# دکمه‌ها برای منوی اصلی
def send_welcome(chat_id):
    keyboard = {
        "keyboard": [
            [{"text": "📝 آزمون‌های روانشناسی"}],
            [{"text": "📊 مشاهده تحلیل آزمون"}],
            [{"text": "👩‍⚕️ درمانگران مرکز شیوا"}]
        ],
        "resize_keyboard": True
    }
    welcome_text = (
        "همراه گرامی سلام! به کلینیک روانشناسی و مشاوره شیوا خوش آمدید.\n"
        "برای بهره مندی از امکانات این بازو از گزینه‌های زیر استفاده کنید."
    )
    requests.post(URL + "sendMessage", json={
        "chat_id": chat_id,
        "text": welcome_text,
        "reply_markup": keyboard
    })

# دریافت پیام‌ها
def get_updates(offset=None):
    response = requests.get(URL + "getUpdates", params={"offset": offset})
    return response.json()

# ارسال پیام ساده
def send_message(chat_id, text):
    requests.post(URL + "sendMessage", data={"chat_id": chat_id, "text": text})

# پردازش پیام‌ها
def main():
    last_update_id = None
    while True:
        updates = get_updates(last_update_id)
        if "result" in updates:
            for update in updates["result"]:
                if "message" not in update:
                    continue

                chat_id = update["message"]["chat"]["id"]
                user_msg = update["message"].get("text", "").strip()
                print(f"📩 پیام کاربر: {user_msg}")

                if user_msg == "/start":
                    send_welcome(chat_id)

                elif user_msg == "📝 آزمون‌های روانشناسی":
                    message = "🧾 فهرست آزمون های روانشناسی و هزینه تحلیل آنها:\n"
                    for title, (link, cost) in tests.items():
                        cost_number = int(cost.replace(" ریال", "").replace(",", "").replace("٬", ""))
                        cost_formatted = "{:,}".format(cost_number).replace(",", "٬") + " ریال"
                        message += f"\n🔹 {title}\n{link}\n💰 هزینه تحلیل: {cost_formatted}\n"
                    message += "\n⬅️ بازگشت به صفحه اصلی"
                    send_message(chat_id, message)

                elif user_msg == "📊 مشاهده تحلیل آزمون":
                    send_message(chat_id, "برای مشاهده نتیجه تحلیل آزمون خود، لطفاً به آدرس زیر مراجعه  و کد سفارش خود را وارد نمایید:\n🔍 https://shivapsy.ir/test-analysis-explore/")

                elif user_msg == "👩‍⚕️ درمانگران مرکز شیوا":
                    send_message(chat_id, "برای آشنایی با درمانگران مرکز، لطفاً به لینک زیر مراجعه کنید:\n👩‍⚕️ https://shivapsy.ir/doctors/")

                else:
                    send_welcome(chat_id)

                last_update_id = update["update_id"] + 1
        time.sleep(1)

if __name__ == '__main__':
    main()
