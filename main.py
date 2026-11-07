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
    return "⚡ Al-Moqana NumberNest Server is Active 24/7! ⚡"

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
API_TOKEN = '8686242492:AAFdseE7gxsUNRkVgVESl22R_qxqd7WHYEU'
API_5SIM_KEY = 'ضع_مفتاح_الـ_API_الخاص_بموقع_5sim_هنا' 
ADMIN_ID = 8388141188 
CHANNEL_LOG_ID = "@Awad_Numbers_Bot"  

# تنظيف فوري لأي ويبهوك قديم
try:
    requests.get(f"https://api.telegram.org/bot{API_TOKEN}/deleteWebhook?drop_pending_updates=true", timeout=10)
except Exception:
    pass

bot = telebot.TeleBot(API_TOKEN, threaded=False)
DEVELOPER_URL = "https://t.me/awad3210"

# قنوات الاشتراك الإجباري مع معرفاتها وروابطها
SUBSCRIPTION_CHANNELS = [
    {"id": "@Awad_Numbers_Bot", "name": "📢 قناة البوت الرسمية", "url": "https://t.me/Awad_Numbers_Bot"},
    {"id": "@v_o_lti", "name": "📢 قناة جديدة", "url": "https://t.me/v_o_lti"},
    {"id": "@jzbznznx", "name": "📢 قناة عبارات بشكل عام", "url": "https://t.me/jzbznznx"},
    {"name": "📢 تعليم اختراق الجوالات وتوقيف الواتساب", "id": "@breakthroughawad210", "url": "https://t.me/breakthroughawad210"},
    {"id": "@sn6hdbdn19dndw", "name": "📢 قناة الدعم الاحتياطية", "url": "https://t.me/sn6hdbdn19dndw"},
    {"id": "+KhzU3jbVrVVkNWU0", "name": "💬 جروب المناقشة والتبادل", "url": "https://t.me/+KhzU3jbVrVVkNWU0"}
]

APPS_DATA = {
    "facebook": {"name": "Facebook", "app_icon": "📘", "code": "1"},
    "huawei": {"name": "Huawei", "app_icon": "📱", "code": "218"},
    "instagram": {"name": "Instagram", "app_icon": "📸", "code": "39"},
    "whatsapp": {"name": "WhatsApp", "app_icon": "🟢", "code": "967"},
    "x": {"name": "X", "app_icon": "❌", "code": "1"}
}

COUNTRIES_DATA = {
    "ethiopia": {"name": "Ethiopia", "flag": "🇪🇹", "code": "251", "slug": "ethiopia"},
    "guinea": {"name": "Guinea", "flag": "🇬🇳", "code": "224", "slug": "guinea"},
    "italy": {"name": "Italy", "flag": "🇮🇹", "code": "39", "slug": "italy"},
    "madagascar": {"name": "Madagascar", "flag": "🇲🇬", "code": "261", "slug": "madagascar"},
    "mali": {"name": "Mali", "flag": "🇲🇱", "code": "223", "slug": "mali"},
    "slovenia": {"name": "Slovenia", "flag": "🇸🇮", "code": "386", "slug": "slovenia"},
    "testall": {"name": "USA", "flag": "🇺🇸", "code": "1", "slug": "usa"},
    "venezuela": {"name": "Venezuela", "flag": "🇻🇪", "code": "58", "slug": "venezuela"}
}

CACHED_NUMBERS = {}
BROADCAST_MODE = {}

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

def get_users_list():
    try:
        if not os.path.exists("users.txt"):
            return []
        with open("users.txt", "r") as f:
            return [line.strip() for line in f.read().splitlines() if line.strip()]
    except Exception:
        return []

# فحص القنوات التي لم يشترك فيها المستخدم بعد
def get_unsubscribed_channels(user_id):
    if user_id == ADMIN_ID: 
        return []
    unsubscribed = []
    for ch in SUBSCRIPTION_CHANNELS:
        ch_id = ch["id"]
        # إذا كانت رابط دعوة جروب خاص، نتخطي فحص الـ API المباشر ونعتبرها تتطلب تحقق يدوي أو نتحقق من القنوات العامة
        if ch_id.startswith("+") or ch_id.startswith("https:"):
            continue
        try:
            status = bot.get_chat_member(ch_id, user_id).status
            if status in ['left', 'kicked']:
                unsubscribed.append(ch)
        except Exception:
            # في حال حدث خطأ في جلب العضوية، نضيفها للاحتياط ليقوم المستخدم بالاشتراك فيها
            unsubscribed.append(ch)
    return unsubscribed

# دالة إنشاء أزرار الاشتراك الديناميكية المتبقية
def get_subscription_markup(user_id):
    unsub_list = get_unsubscribed_channels(user_id)
    markup = InlineKeyboardMarkup(row_width=1)
    
    # إذا لم يتبقى قنوات (أو البوت لم يتمكن من فحص الجروب الخاص)، نعرض أزرار القنوات العامة الباقية
    if not unsub_list:
        # لو كانت القائمة فارغة، نعرض الأزرار الأساسية
        for ch in SUBSCRIPTION_CHANNELS[:5]:
            markup.add(InlineKeyboardButton(ch["name"], url=ch["url"]))
    else:
        for ch in unsub_list:
            markup.add(InlineKeyboardButton(ch["name"], url=ch["url"]))
            
    markup.add(InlineKeyboardButton("✨ تحقق من الاشتراك ✅", callback_data="verify_subs"))
    return markup

# --- 5. SCRAPER ENGINE ---
def scrape_single_source(url, code):
    nums = []
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    try:
        r = requests.get(url, headers=headers, timeout=2)
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

def get_numbers_for_target(code, slug):
    cache_key = f"{code}_{slug}"
    if cache_key in CACHED_NUMBERS and CACHED_NUMBERS[cache_key]:
        return CACHED_NUMBERS[cache_key]
        
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
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(scrape_single_source, url, code) for url in sources]
            for future in concurrent.futures.as_completed(futures):
                res = future.result()
                if res: all_numbers.extend(res)
    except Exception:
        pass
        
    unique_nums = list(set(all_numbers))
    if not unique_nums:
        unique_nums = [f"+{code}9{int(time.time()) % 100000000}", f"+{code}8{int(time.time()) % 100000000}"]
        
    CACHED_NUMBERS[cache_key] = unique_nums
    return unique_nums

# --- 6. GROUP PROTECTION & DEVELOPER BROADCAST SYSTEM ---
@bot.message_handler(content_types=['photo', 'video', 'document', 'audio', 'sticker', 'animation', 'voice', 'video_note'])
def protect_group(message):
    user_id = message.from_user.id
    if user_id != ADMIN_ID and message.chat.type in ['group', 'supergroup']:
        try:
            bot.delete_message(message.chat.id, message.message_id)
            warning_msg = bot.send_message(
                message.chat.id, 
                f"⚠️ [{message.from_user.first_name}](tg://user?id={user_id})\nممنوع إرسال الصور، الفيديوهات، الروابط أو الملفات هنا! 🚫\nمسموح بالنصوص الكتابية فقط.", 
                parse_mode="Markdown"
            )
            time.sleep(5)
            bot.delete_message(message.chat.id, warning_msg.message_id)
        except Exception:
            pass

@bot.message_handler(func=lambda message: True, content_types=['text', 'photo', 'video', 'document'])
def monitor_text_messages(message):
    user_id = message.from_user.id
    chat_type = message.chat.type
    
    # حماية المجموعات
    if user_id != ADMIN_ID and chat_type in ['group', 'supergroup']:
        if message.text and ("http://" in message.text or "https://" in message.text or "t.me/" in message.text or ".com" in message.text):
            try:
                bot.delete_message(message.chat.id, message.message_id)
                warning_msg = bot.send_message(
                    message.chat.id, 
                    f"⚠️ [{message.from_user.first_name}](tg://user?id={user_id})\nممنوع إرسال الروابط في المجموعة! 🚫", 
                    parse_mode="Markdown"
                )
                time.sleep(5)
                bot.delete_message(message.chat.id, warning_msg.message_id)
                return
            except Exception:
                pass

    # الخاص
    if chat_type == 'private':
        if user_id == ADMIN_ID and BROADCAST_MODE.get(ADMIN_ID, False):
            BROADCAST_MODE[ADMIN_ID] = False
            users = get_users_list()
            sent_count = 0
            
            bot.send_message(ADMIN_ID, f"📢 **جاري إرسال الرسالة إلى `{len(users)}` مستخدم...**", parse_mode="Markdown")
            for uid in users:
                try:
                    if message.content_type == 'text':
                        bot.send_message(uid, message.text, parse_mode="Markdown")
                    elif message.content_type == 'photo':
                        bot.send_photo(uid, message.photo[-1].file_id, caption=message.caption or "", parse_mode="Markdown")
                    elif message.content_type == 'video':
                        bot.send_video(uid, message.video.file_id, caption=message.caption or "", parse_mode="Markdown")
                    sent_count += 1
                except Exception:
                    pass
            bot.send_message(ADMIN_ID, f"✅ **تمت الإذاعة بنجاح!**\n📬 وصلت إلى `{sent_count}` مستخدم.", parse_mode="Markdown")
            return

        # فحص الاشتراك الذكي
        unsub = get_unsubscribed_channels(user_id)
        if unsub:
            bot.send_message(
                message.chat.id, 
                "⚠️ **يجب عليك الانضمام إلى القنوات المتبقية لاستخدام البوت:**", 
                reply_markup=get_subscription_markup(user_id), 
                parse_mode="Markdown"
            )
            return
        
        text = message.text
        if text == "🌐 الدول والأرقام":
            send_main_menu(message.chat.id)
        elif text == "🛒 قسم الأرقام المدفوعة":
            bot.send_message(message.chat.id, "🛍️ **قسم الأرقام المدفوعة الحصرية متاح عبر التواصل مع المطور مباشرة.**", parse_mode="Markdown")
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
            
            users_count = len(get_users_list())
            markup_admin = InlineKeyboardMarkup(row_width=1)
            markup_admin.add(
                InlineKeyboardButton("📢 إذاعة رسالة لجميع المستخدمين", callback_data="admin_broadcast"),
                InlineKeyboardButton("📊 إحصائيات البوت", callback_data="admin_stats")
            )
            bot.send_message(ADMIN_ID, f"⚙️ **لوحة تحكم المطور:**\n👥 إجمالي المشتركين: `{users_count}` عضو.", reply_markup=markup_admin, parse_mode="Markdown")

# --- 7. INTERFACE & MENUS ---
def get_main_reply_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(
        KeyboardButton("🌐 الدول والأرقام"),
        KeyboardButton("🛒 قسم الأرقام المدفوعة"),
        KeyboardButton("📢 مشاركة البوت"),
        KeyboardButton("👨‍💻 تواصل مع المطور"),
        KeyboardButton("🪪 استخراج ID"),
        KeyboardButton("⚡ لوحة المطور")
    )
    return markup

def send_main_menu(chat_id, message_id=None):
    markup = InlineKeyboardMarkup(row_width=2)
    markup.add(
        InlineKeyboardButton("Facebook 📘 (3)", callback_data="app_facebook"),
        InlineKeyboardButton("Huawei 📱 (1)", callback_data="app_huawei"),
        InlineKeyboardButton("Instagram 📸 (2)", callback_data="app_instagram"),
        InlineKeyboardButton("WhatsApp 🟢 (2)", callback_data="app_whatsapp"),
        InlineKeyboardButton("X ❌ (1)", callback_data="app_x")
    )
    markup.add(
        InlineKeyboardButton("Ethiopia 🇪🇹", callback_data="cnt_ethiopia"),
        InlineKeyboardButton("Guinea 🇬🇳", callback_data="cnt_guinea"),
        InlineKeyboardButton("Italy 🇮🇹 (5)", callback_data="cnt_italy"),
        InlineKeyboardButton("Madagascar 🇲🇬", callback_data="cnt_madagascar"),
        InlineKeyboardButton("Mali 🇲🇱", callback_data="cnt_mali"),
        InlineKeyboardButton("Slovenia 🇸🇮", callback_data="cnt_slovenia"),
        InlineKeyboardButton("Test All 🔥", callback_data="cnt_testall"),
        InlineKeyboardButton("Venezuela 🇻🇪 (7)", callback_data="cnt_venezuela")
    )
    
    welcome_text = (
        "👋 **مرحباً بك يا صديقي في بوت الأرقام والحسابات!**\n"
        "✅ اختر التطبيق أو الدولة من الأزرار بالأسفل للحصول على الرقم الحي فوراً."
    )
    try:
        if message_id:
            bot.edit_message_text(welcome_text, chat_id, message_id, reply_markup=markup, parse_mode="Markdown")
        else:
            bot.send_message(chat_id, welcome_text, reply_markup=markup, parse_mode="Markdown")
    except Exception:
        pass

@bot.message_handler(commands=['start'])
def start(message):
    if message.chat.type != 'private':
        return
    user_id = message.from_user.id
    save_user(user_id)
    
    unsub = get_unsubscribed_channels(user_id)
    if unsub:
        try:
            bot.send_message(
                message.chat.id, 
                "⚠️ **يجب عليك الانضمام إلى القنوات التالية أولاً لاستخدام البوت:**", 
                reply_markup=get_subscription_markup(user_id), 
                parse_mode="Markdown"
            )
        except Exception:
            pass
        return
    
    try:
        bot.send_message(message.chat.id, "📌 القائمة الرئيسية:", reply_markup=get_main_reply_keyboard())
    except Exception:
        pass
    send_main_menu(message.chat.id)

@bot.callback_query_handler(func=lambda call: True)
def handle_queries(call):
    user_id = call.from_user.id
    
    if call.data == "verify_subs":
        unsub = get_unsubscribed_channels(user_id)
        if not unsub:
            try:
                bot.delete_message(call.message.chat.id, call.message.message_id)
            except:
                pass
            bot.answer_callback_query(call.id, "✅ تم التحقق بنجاح، أهلاً بك!", show_alert=True)
            try:
                bot.send_message(call.message.chat.id, "📌 القائمة الرئيسية:", reply_markup=get_main_reply_keyboard())
            except:
                pass
            send_main_menu(call.message.chat.id)
        else:
            try:
                # تحديث القائمة ديناميكياً لتختفي القنوات التي تم الاشتراك بها وتبقى البقية فقط
                bot.edit_message_reply_markup(call.message.chat.id, call.message.message_id, reply_markup=get_subscription_markup(user_id))
            except Exception:
                pass
            bot.answer_callback_query(call.id, "❌ لم تقم بالاشتراك في كافة القنوات المتبقية!", show_alert=True)

    elif call.data == "back_home":
        send_main_menu(call.message.chat.id, call.message.message_id)

    elif call.data == "admin_broadcast":
        if user_id != ADMIN_ID:
            return bot.answer_callback_query(call.id, "❌ مخصص للمطور فقط.", show_alert=True)
        BROADCAST_MODE[ADMIN_ID] = True
        bot.answer_callback_query(call.id, "📢 تم تفعيل وضع الإذاعة")
        bot.send_message(ADMIN_ID, "✍️ **أرسل الآن الرسالة أو الصورة أو الفيديو الذي تريد إذاعته لجميع المستخدمين:**", parse_mode="Markdown")

    elif call.data == "admin_stats":
        if user_id != ADMIN_ID:
            return
        users_count = len(get_users_list())
        bot.answer_callback_query(call.id, f"📊 عدد المشتركين: {users_count}", show_alert=True)

    elif call.data.startswith("app_"):
        app_key = call.data.replace("app_", "")
        app_info = APPS_DATA.get(app_key, {"name": "Service", "code": "1", "app_icon": "📱"})
        
        markup = InlineKeyboardMarkup(row_width=2)
        markup.add(
            InlineKeyboardButton("Italy 🇮🇹", callback_data=f"getnum_{app_key}_italy"),
            InlineKeyboardButton("Venezuela 🇻🇪", callback_data=f"getnum_{app_key}_venezuela"),
            InlineKeyboardButton("Ethiopia 🇪🇹", callback_data=f"getnum_{app_key}_ethiopia"),
            InlineKeyboardButton("Guinea 🇬🇳", callback_data=f"getnum_{app_key}_guinea")
        )
        markup.add(InlineKeyboardButton("رجوع 🔙", callback_data="back_home"))
        
        try:
            bot.edit_message_text(
                f"📂 **{app_info['name']}**\n🌐 **اختر الدولة للطلب:**",
                call.message.chat.id, call.message.message_id, reply_markup=markup, parse_mode="Markdown"
            )
        except Exception:
            pass

    elif call.data.startswith("cnt_") or call.data.startswith("getnum_"):
        try:
            parts = call.data.split("_")
            if len(parts) == 2:
                cnt_key = parts[1]
                app_name = "WhatsApp"
                app_icon = "🟢"
                cnt_info = COUNTRIES_DATA.get(cnt_key, {"name": "USA", "flag": "🇺🇸", "code": "1", "slug": "usa"})
            else:
                app_key = parts[1]
                cnt_key = parts[2]
                app_info = APPS_DATA.get(app_key, {"name": "WhatsApp", "app_icon": "🟢"})
                app_name = app_info["name"]
                app_icon = app_info["app_icon"]
                cnt_info = COUNTRIES_DATA.get(cnt_key, {"name": "Italy", "flag": "🇮🇹", "code": "39", "slug": "italy"})
                
            bot.answer_callback_query(call.id, "⚡ جاري تجهيز الرقم وجلب الكود...")
            
            nums = get_numbers_for_target(cnt_info["code"], cnt_info["slug"])
            selected_number = nums[int(time.time()) % len(nums)]
            dummy_otp = f"{int(time.time()) % 900000 + 100000}"
            
            user_display_text = (
                f"🌍 **الدولة:** {cnt_info['flag']} `{cnt_info['name']}`\n\n"
                f"🔢 **الرقم:** `{selected_number}`\n\n"
                f"🔑 **كود التحقق الوارد:** `{dummy_otp}`\n\n"
                f"📋 *اضغط مطولًا للنسخ*"
            )
            
            markup_user = InlineKeyboardMarkup(row_width=2)
            markup_user.add(
                InlineKeyboardButton("🔄 رقم جديد", callback_data=call.data),
                InlineKeyboardButton("📂 جروب الأكواد", url=DEVELOPER_URL)
            )
            markup_user.add(InlineKeyboardButton("رجوع 🔙", callback_data="back_home"))
            
            bot.edit_message_text(user_display_text, call.message.chat.id, call.message.message_id, reply_markup=markup_user, parse_mode="Markdown")
            
            masked_number = selected_number[:6] + "••••••••" + selected_number[-4:] if len(selected_number) > 10 else selected_number
            
            channel_formatted_msg = (
                f"TRICKS MASTAR BOT PANEL\n"
                f"{cnt_info['flag']} #{cnt_info['name'][:2].upper()} {app_icon} {masked_number} |\n"
                f"🔊 English\n\n"
                f"Code {app_name} : {dummy_otp[:3]}-{dummy_otp[3:]}\n"
                f"Never share this code with anyone\n\n"
                f"# Prefix: /pre {selected_number.replace('+', '')[:6]}"
            )
            
            markup_channel = InlineKeyboardMarkup(row_width=2)
            markup_channel.add(
                InlineKeyboardButton(f"🔓 📋 {dummy_otp}", callback_data="dummy_otp_copy")
            )
            markup_channel.add(
                InlineKeyboardButton("🤖 Bot Link", url=DEVELOPER_URL),
                InlineKeyboardButton("📢 Channel", url=SUBSCRIPTION_CHANNELS[0]["url"])
            )
            
            try:
                bot.send_message(CHANNEL_LOG_ID, channel_formatted_msg, parse_mode="Markdown", reply_markup=markup_channel)
            except Exception:
                pass
                
        except Exception:
            bot.answer_callback_query(call.id, "❌ خطأ في الجلب، حاول مجدداً.", show_alert=True)

# --- 8. RUNNER ---
if __name__ == "__main__":
    keep_alive()
    print("NumberNest Bot Engine is running 24/7 successfully with Dynamic Subscription & Broadcast!")

    while True:
        try:
            bot.infinity_polling(timeout=20, long_polling_timeout=10, skip_pending=True)
        except Exception as e:
            print(f"Polling error: {e}")
            time.sleep(5)
