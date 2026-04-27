from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8634042111:AAFF0uOMuXK1UW_tDheN7O6u4vzaD_PprsA"

questions = [
    {"q": "ما عاصمة المملكة العربية السعودية؟", "options": ["جدة", "الرياض", "مكة", "الدمام"], "answer": 1, "prize": "100 ريال"},
    {"q": "كم عدد أيام السنة؟", "options": ["360", "364", "365", "366"], "answer": 2, "prize": "200 ريال"},
    {"q": "ما أكبر كوكب في المجموعة الشمسية؟", "options": ["زحل", "المريخ", "المشتري", "أورانوس"], "answer": 2, "prize": "300 ريال"},
    {"q": "من اخترع الهاتف؟", "options": ["إديسون", "غراهام بيل", "نيوتن", "أينشتاين"], "answer": 1, "prize": "500 ريال"},
    {"q": "ما أطول نهر في العالم؟", "options": ["الأمازون", "النيل", "الدانوب", "الفولغا"], "answer": 1, "prize": "1,000 ريال"},
    {"q": "كم عدد سور القرآن الكريم؟", "options": ["112", "113", "114", "115"], "answer": 2, "prize": "2,000 ريال"},
    {"q": "ما عاصمة فرنسا؟", "options": ["برلين", "روما", "مدريد", "باريس"], "answer": 3, "prize": "4,000 ريال"},
    {"q": "كم عدد لاعبي كرة القدم في الملعب لكل فريق؟", "options": ["9", "10", "11", "12"], "answer": 2, "prize": "8,000 ريال"},
    {"q": "ما أصغر دولة في العالم؟", "options": ["موناكو", "سان مارينو", "الفاتيكان", "ليختنشتاين"], "answer": 2, "prize": "16,000 ريال"},
    {"q": "من كتب رواية روميو وجولييت؟", "options": ["ديكنز", "شكسبير", "هوميروس", "دانتي"], "answer": 1, "prize": "32,000 ريال"},
    {"q": "ما أسرع حيوان بري في العالم؟", "options": ["الأسد", "النمر", "الفهد", "الحصان"], "answer": 2, "prize": "64,000 ريال"},
    {"q": "كم عدد ألوان الطيف؟", "options": ["5", "6", "7", "8"], "answer": 2, "prize": "125,000 ريال"},
    {"q": "ما أعمق بحيرة في العالم؟", "options": ["بحيرة فيكتوريا", "بحيرة بايكال", "بحيرة سوبيريور", "بحيرة تيتيكاكا"], "answer": 1, "prize": "250,000 ريال"},
    {"q": "من هو مؤسس شركة آبل؟", "options": ["بيل غيتس", "ستيف جوبز", "إيلون ماسك", "مارك زوكربيرغ"], "answer": 1, "prize": "500,000 ريال"},
    {"q": "ما أكبر محيط في العالم؟", "options": ["المحيط الهندي", "المحيط الأطلسي", "المحيط المتجمد", "المحيط الهادئ"], "answer": 3, "prize": "1,000,000 ريال"},
]

games = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🎰 أهلاً بك في *من سيربح المليون؟*\n\nاكتب /play لتبدأ اللعبة!", parse_mode="Markdown")

async def play(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.message.from_user.id
    games[user_id] = {"level": 0}
    await send_question(update, context, user_id)

async def send_question(update, context, user_id):
    level = games[user_id]["level"]
    q = questions[level]
    keyboard = [
        [InlineKeyboardButton(f"أ) {q['options'][0]}", callback_data="0"), InlineKeyboardButton(f"ب) {q['options'][1]}", callback_data="1")],
        [InlineKeyboardButton(f"ج) {q['options'][2]}", callback_data="2"), InlineKeyboardButton(f"د) {q['options'][3]}", callback_data="3")],
    ]
    text = f"💰 *الجائزة:* {q['prize']}\n❓ السؤال {level + 1} من {len(questions)}:\n\n*{q['q']}*"
    if hasattr(update, 'message') and update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.callback_query.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def answer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    user_id = query.from_user.id
    if user_id not in games:
        await query.message.reply_text("اكتب /play لتبدأ اللعبة!")
        return
    level = games[user_id]["level"]
    q = questions[level]
    chosen = int(query.data)
    if chosen == q["answer"]:
        if level + 1 == len(questions):
            await query.message.reply_text(f"🏆 *مبروك! ربحت المليون!* 🎉\n💰 جائزتك: {q['prize']}", parse_mode="Markdown")
            del games[user_id]
        else:
            games[user_id]["level"] += 1
            await query.message.reply_text(f"✅ *إجابة صحيحة!* ربحت {q['prize']} 🎉", parse_mode="Markdown")
            await send_question(update, context, user_id)
    else:
        await query.message.reply_text(f"❌ *إجابة خاطئة!*\nالإجابة الصحيحة: *{q['options'][q['answer']]}*\n\nاكتب /play للعب مجدداً", parse_mode="Markdown")
        del games[user_id]

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("play", play))
app.add_handler(CallbackQueryHandler(answer))
app.run_polling()
