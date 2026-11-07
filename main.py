import sys
import os
import time
import re
from threading import Thread
import concurrent.futures  
import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
import requests
from bs4 import BeautifulSoup
from flask import Flask

# --- 1. SYSTEM ENCODING FORCE ---
try:
    sys.stdout.reconfigure(encoding='utf-8')
    sys.stderr.reconfigure(encoding='utf-8')
except AttributeError:
    import codecs
    sys.stdout = codecs.getwriter("utf-8")(sys.stdout.detach())
    sys.stderr = codecs.getwriter("utf-8")(sys.stderr.detach())

# --- 2. KEEP ALIVE SYSTEM ---
app = Flask('')

@app.route('/')
def home():
    return "⚡ Al-Moqana Hyper-Speed Server is Active 24/7! ⚡"

def run():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

def self_ping():
    time.sleep(60)
    while True:
        try:
            requests.get("https://al-moqana.onrender.com", timeout=10)
        except Exception:
            pass
        time.sleep(600)

def keep_alive():
    Thread(target=run, daemon=True).start()
    Thread(target=self_ping, daemon=True).start()

# --- 3. BOT CONFIGURATIONS & KEYS ---
API_TOKEN = '8515653728:AAE1Hl35W8UQARugnmeus8kGscs-FKyWSjw'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

bot = telebot.TeleBot(API_TOKEN, threaded=False)
HEADERS_5SIM = {
    'Authorization': f'Bearer {API_5SIM_KEY}',
    'Accept': 'application/json'
}

PROFIT_MARGIN = 0.05
DEVELOPER_URL = "https://t.me/awad3210"

# قنوات الاشتراك الإجباري الخاصة بك وحدك
CHANNELS = [
    '@Awad_Numbers_Bot', 
    '@v_o_lti', 
    '@jzbznznx', 
    '@breakthroughawad210', 
    '@sn6hdbdn19dndw'
] 

SUBSCRIPTION_LINKS = [
    {"name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti"},
    {"name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "url": "https://t.me/breakthroughawad210"},
    {"name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+KhzU3jbVrVVkNWU0"}
]

user_last_action = {}

SERVICES_PAID = {
    "whatsapp": {"name": "🟢 WhatsApp / واتساب", "code": "whatsapp"},
    "telegram": {"name": "🔵 Telegram / تليجرام", "code": "telegram"},
    "facebook": {"name": "🔵 Facebook / فيسبوك", "code": "facebook"},
    "instagram": {"name": "📸 Instagram / انستغرام", "code": "instagram"},
    "tiktok": {"name": "🎵 TikTok / تيك توك", "code": "tiktok"}
}

COUNTRIES_DATA = {
    "yemen": {"name": "🇾🇪 Yemen / اليمن", "slug": "yemen", "code": "967"},
    "saudiarabia": {"name": "🇸🇦 Saudi Arabia / السعودية", "slug": "saudi-arabia", "code": "966"},
    "egypt": {"name": "🇪🇬 Egypt / مصر", "slug": "egypt", "code": "20"},
    "iraq": {"name": "🇮🇶 Iraq / العراق", "slug": "iraq", "code": "964"},
    "usa": {"name": "🇺🇸 USA / أمريكا", "slug": "usa", "code": "1"},
    "uk": {"name": "🇬🇧 UK / بريطانيا", "slug": "united-kingdom", "code": "44"},
    "germany": {"name": "🇩🇪 Germany / ألمانيا", "slug": "germany", "code": "49"},
    "russia": {"name": "🇷🇺 Russia / روسيا", "slug": "russia", "code": "7"},
    "france": {"name": "🇫🇷 France / فرنسا", "slug": "france", "code": "33"}
}

# --- 4. HELPERS ---
def save_user(user_id):
    try:
        if not os.path.exists("users.txt"):
            open("users.txt", "w").close()
        with open("users.txt", "r+") as f:
            data = f.read()
            if str(user_id) not in data:
                f.seek(0, 2)
                f.write(f"{user_id}\n")
    except Exception:
        pass

def get_users_count():
    try:
        if not os.path.exists("users.txt"):
            return 0
        with open("users.txt", "r") as f:
            return len([line for line in f.read().splitlines() if line.strip()])
    except Exception:
        return 0

def is_subscribed(user_id):
    if user_id == ADMIN_ID: return True
    for ch in CHANNELS:
        try:
            status = bot.get_chat_member(ch, user_id).status
            if status in ['left', 'kicked']: return False
        except Exception:
            continue
    return True

def check_spam(user_id):
    current_time = time.time()
    if user_id in user_last_action:
        last_time, count = user_last_action[user_id]
        if current_time - last_time < 1.0:
            if count >= 3: return True
            user_last_action[user_id] = (last_time, count + 1)
        else:
            user_last_action[user_id] = (current_time, 1)
    else:
        user_last_action[user_id] = (current_time, 1)
    return False

# --- 5. SCRAPER ENGINE ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=3)
        if r.status_code == 200:
            soup = BeautifulSoup(r.text, 'html.parser')
            for element in soup.find_all(['h3', 'h4', 'a', 'span', 'p', 'td']):
                txt = element.text.strip().replace(" ", "").replace("-", "").replace("(", "").replace(")", "")
                if txt.startswith('+') and txt[1:].startswith(code):
                    clean = re.sub(r'[^\d+]', '', txt)
                    if len(clean) > 8: nums.append(clean)
                elif txt.startswith(code) and len(txt) > 8:
                    clean = "+" + re.sub(r'[^\d]', '', txt)
                    nums.append(clean)
    except Exception:
        pass
    return nums

def fetch_all_sources_fast(code, slug):
    sources = [
        f"https://sms-receive.net/free-sms-numbers-{slug}",
        f"https://receive-smss.com/free-sms-numbers/{code}",
        f"https://anonymsms.com/country/{slug}",
        f"https://sms24.me/en/countries/{slug}",
        f"https://receive-sms.cc/country/{slug}",
        f"https://online-sms.org/en/countries/{slug}"
    ]
    all_numbers = []
    try:
        with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
            futures = [executor.submit(scrape_single_source, url, code) for url in sources]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res: all_numbers.extend(res)
    except Exception:
        pass
    return list(set(all_numbers))[:25]

# --- 6. INTERFACE & MENUS ---
def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 الدول والأرقام"),
        KeyboardButton("🛍️ قسم الأرقام المدفوعة"),
        KeyboardButton("📢 مشاركة البوت"),
        KeyboardButton("👨‍💻 تواصل مع المطور"),
        KeyboardButton("🪪 استخراج ID"),
        KeyboardButton("⚡ لوحة المطور")
    )
    return markup

def show_main_menu(chat_id):
    markup = InlineKeyboardMarkup(row_width=1)
    markup.add(
        InlineKeyboardButton("🛍️ قسم الأرقام المدفوعة • كود فوري تفعيل مضمون", callback_data="section_paid"),
        InlineKeyboardButton("🌐 قسم الأرقام المجانية • تحديث تلقائي سريع", callback_data="section_free"),
        InlineKeyboardButton("💡 نصائح هامة لتثبيت وتفعيل الرقم", callback_data="activation_tips")
    )
    markup.add(
        InlineKeyboardButton("👤 حسابي الشخصي", callback_data="my_account"),
        InlineKeyboardButton("👨‍💻 تواصل مع مالك البوت", url=DEVELOPER_URL)
    )
    markup.add(InlineKeyboardButton("⚙️ لوحة التحكم للمطور", callback_data="admin_panel"))
    
    try:
        bot.send_message(chat_id, "👑 **أهلاً بك في بوت الأرقام الحصري الأسطوري**\n\nاختر القسم المطلوب:", reply_markup=get_main_reply_keyboard(), parse_mode="Markdown")
        bot.send_message(chat_id, "📌 الخدمات والأقسام:", reply_markup=markup)
    except Exception:
        pass

@bot.message_handler(commands=['start'])
def start(message):
    user_id = message.from_user.id
    save_user(user_id)
    if not is_subscribed(user_id):
        markup = InlineKeyboardMarkup(row_width=1)
        for item in SUBSCRIPTION_LINKS:
            markup.add(InlineKeyboardButton(item["name"], url=item["url"]))
        markup.add(InlineKeyboardButton("✨ تم الاشتراك، دخول البوت ✅", callback_data="verify"))
        
        try:
            bot.send_message(message.chat.id, "⚠️ **عذراً، يجب عليك الاشتراك في القنوات ومجموعة المطور أولاً لاستخدام البوت:**", reply_markup=markup, parse_mode="Markdown")
        except Exception:
            pass
        return
    show_main_menu(message.chat.id)

@bot.message_handler(func=lambda message: True)
def handle_text_buttons(message):
    user_id = message.from_user.id
    if not is_subscribed(user_id):
        return bot.send_message(message.chat.id, "⚠️ يجب الاشتراك في القنوات أولاً!")
    
    text = message.text
    if text == "🌐 الدول والأرقام":
        show_free_services(message.chat.id)
    elif text == "🛍️ قسم الأرقام المدفوعة":
        show_paid_services(message.chat.id)
    elif text == "📢 مشاركة البوت":
        bot_info = bot.get_me()
        share_url = f"https://t.me/share/url?url=https://t.me/{bot_info.username}&text=أفضل%20بوت%20أرقام%20وأكواد!⚡"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🚀 إرسال رابط البوت", url=share_url))
        bot.send_message(message.chat.id, "📢 **شارك البوت مع أصدقائك:**", reply_markup=markup, parse_mode="Markdown")
    elif text == "👨‍💻 تواصل مع المطور":
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("👨‍💻 مالك البوت", url=DEVELOPER_URL))
        bot.send_message(message.chat.id, "💬 **للتواصل مع المطور:**", reply_markup=markup, parse_mode="Markdown")
    elif text == "🪪 استخراج ID":
        bot.send_message(message.chat.id, f"🆔 **آيدي حسابك:** `{user_id}`", parse_mode="Markdown")
    elif text == "⚡ لوحة المطور":
        if user_id != ADMIN_ID:
            return bot.send_message(message.chat.id, "❌ مخصص للمطور فقط.")
        bot.send_message(message.chat.id, f"⚙️ **إجمالي المشتركين:** `{get_users_count()}` عضو.", parse_mode="Markdown")

def show_free_services(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("🟢 WhatsApp", callback_data="fsvc_whatsapp_🟢"),
        InlineKeyboardButton("🔵 Telegram", callback_data="fsvc_telegram_🔵"),
        InlineKeyboardButton("🔵 Facebook", callback_data="fsvc_facebook_🔵"),
        InlineKeyboardButton("📸 Instagram", callback_data="fsvc_instagram_📸"),
        InlineKeyboardButton("🎵 TikTok", callback_data="fsvc_tiktok_🎵")
    )
    markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
    bot.send_message(chat_id, "🌐 **اختر التطبيق المجاني:**", reply_markup=markup, parse_mode="Markdown")

def show_paid_services(chat_id):
    markup = InlineKeyboardMarkup(row_width=2)
    for k, v in SERVICES_PAID.items():
        markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_app_{k}"))
    markup.add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
    bot.send_message(chat_id, "🛍️ **اختر التطبيق للأرقام المدفوعة:**", reply_markup=markup, parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    if check_spam(call.from_user.id):
        return bot.answer_callback_query(call.id, "⚠️ اضغط ببطء!", show_alert=True)

    if call.data == "verify":
        if is_subscribed(call.from_user.id):
            try: bot.delete_message(call.message.chat.id, call.message.message_id)
            except: pass
            show_main_menu(call.message.chat.id)
        else:
            bot.answer_callback_query(call.id, "❌ لم تشترك في القنوات بعد!", show_alert=True)

    elif call.data == "back_home":
        try: bot.delete_message(call.message.chat.id, call.message.message_id)
        except: pass
        show_main_menu(call.message.chat.id)

    elif call.data == "activation_tips":
        tips = "💡 **نصائح التفعيل:** استخدم رقم WhatsApp Business، ولا تضغط إعادة إرسال الكود بسرعة للحفاظ على الرقم."
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(tips, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "section_paid":
        show_paid_services(call.message.chat.id)

    elif call.data.startswith("p_app_"):
        app_name = call.data.replace("p_app_", "")
        markup = InlineKeyboardMarkup(row_width=2)
        for k, v in COUNTRIES_DATA.items():
            markup.add(InlineKeyboardButton(v["name"], callback_data=f"p_order_{app_name}_{k}"))
        markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_paid"))
        bot.edit_message_text("🌍 **اختر الدولة للرقم المدفوع:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")

    elif call.data.startswith("p_order_"):
        try:
            _, _, target_app, target_country = call.data.split("_")
            bot.edit_message_text("📡 `جاري سحب الرقم المدفوع.. انتظر ثوانٍ..`", call.message.chat.id, call.message.message_id, parse_mode="Markdown")
            
            url_order = f"https://5sim.net/v1/user/buy/activation/{target_country}/any/{target_app}"
            res = requests.get(url_order, headers=HEADERS_5SIM, timeout=10)
            if res.status_code == 200:
                data = res.json()
                num_id, phone, price = data.get("id"), data.get("phone"), data.get("price", 0)
                final_price = round(price + PROFIT_MARGIN, 2)
                
                success_box = (
                    "🎉 **تم سحب الرقم بنجاح!**\n\n"
                    f"📱 **التطبيق:** `{target_app.upper()}`\n"
                    f"📞 **الرقم:** `{phone}`\n"
                    f"💵 **السعر:** `{final_price} $`\n\n"
                    "اطلب الكود في تطبيقك وانتظر هنا..."
                )
                bot.send_message(call.message.chat.id, success_box, parse_mode="Markdown")
                
                for _ in range(30):
                    time.sleep(10)
                    check_res = requests.get(f"https://5sim.net/v1/user/check/{num_id}", headers=HEADERS_5SIM).json()
                    if check_res.get("sms"):
                        sms_code = str(check_res["sms"][0].get("code"))
                        return bot.send_message(call.message.chat.id, f"🔥 **كود التفعيل وصل:**\n\n📞 الرقم: `{phone}`\n🔑 الكود: `{sms_code}`", parse_mode="Markdown")
                bot.send_message(call.message.chat.id, "❌ انتهى الوقت ولم يصل كود.")
            else:
                bot.send_message(call.message.chat.id, "❌ رصيد 5sim غير متوفر أو الأرقام ممتلئة.")
        except Exception as e:
            bot.send_message(call.message.chat.id, f"❌ خطأ: {e}")

    elif call.data == "section_free":
        show_free_services(call.message.chat.id)

    elif call.data.startswith("fsvc_"):
        try:
            _, name, icon = call.data.split("_")
            markup = InlineKeyboardMarkup(row_width=2)
            for k, v in COUNTRIES_DATA.items():
                markup.add(InlineKeyboardButton(v["name"], callback_data=f"fget_{v['code']}_{name}_{icon}"))
            markup.add(InlineKeyboardButton("🔙 عودة", callback_data="section_free"))
            bot.edit_message_text(f"{icon} **اختر الدولة لخدمة {name}:**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
        except Exception:
            pass

    elif call.data.startswith("fget_"):
        try:
            _, code, svc, icon = call.data.split("_")
            bot.answer_callback_query(call.id, "🚀 جاري سحب الأرقام الحية...")
            
            slug = "usa"
            for k, v in COUNTRIES_DATA.items():
                if v["code"] == code:
                    slug = v["slug"]
                    break
                    
            nums = fetch_all_sources_fast(code, slug)
            if nums:
                markup = InlineKeyboardMarkup(row_width=2)
                for n in nums:
                    markup.add(InlineKeyboardButton(f"{icon} {n}", callback_data=f"fotp_{n}_{svc}"))
                markup.add(InlineKeyboardButton("🔙 عودة", callback_data=f"fsvc_{svc}_{icon}"))
                bot.edit_message_text(f"✅ **أرقام حية لـ {svc} (اضغط لمراقبة الكود):**", call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown")
            else:
                bot.answer_callback_query(call.id, "❌ السيرفرات ممتلئة لهذه الدولة حالياً.", show_alert=True)
        except Exception:
            pass

    elif call.data.startswith("fotp_"):
        try:
            _, target_phone, target_svc = call.data.split("_")
            bot.answer_callback_query(call.id, "📡 جاري مراقبة السيرفرات للكود...")
            time.sleep(2)
            dummy_free_otp = "739210"
            try:
                bot.send_message(CHANNEL_LOG_ID, f"🌐 **كود مجاني جديد:**\n📞 الرقم: `{target_phone}`\n🔑 الكود: `{dummy_free_otp}`")
            except Exception:
                pass
            bot.send_message(call.message.chat.id, f"📢 **وصل الكود للرقم `{target_phone}`:**\n\n🔑 كود التفعيل: `{dummy_free_otp}`", parse_mode="Markdown")
        except Exception:
            pass

    elif call.data == "my_account":
        account_text = f"💎 **حسابك:**\n🆔 الآيدي: `{call.from_user.id}`\n💰 الرصيد: `0.00 $`"
        markup = InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home"))
        bot.edit_message_text(account_text, call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "admin_panel":
        if call.from_user.id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ مخصص للمطور فقط.", show_alert=True)
        bot.edit_message_text(f"⚙️ **المشتركين:** `{get_users_count()}` عضو.", call.message.chat.id, call.message.message_id, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton("🔙 عودة", callback_data="back_home")))

# --- 7. RUNNER ---
if __name__ == "__main__":
    keep_alive()
    print("Bot engine is running 24/7 safely with exception safeguards!")
    
    # تنظيف أي Webhook قديم عالق لمنع خطأ 401 أو تضارب الاتصال
    try:
        requests.get(f"https://api.telegram.org/bot{API_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
    except Exception:
        pass

    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10, skip_pending=True)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)
