from get_parms import mongo_collection
from data import Quiz
import datetime
from get_parms import bot_token
import re
from quizzes.fetch_quizzes import questions
from telegram import (
    KeyboardButton,
    KeyboardButtonPollType,
    Poll,
    InlineKeyboardMarkup,
    ReplyKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardRemove,
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes,
    MessageHandler,
    PollAnswerHandler,
    ConversationHandler,
    PollHandler,
    filters
)

from quizzes.generate import QuizGenerator
config = {
    "model_name": "gpt-3.5-turbo",
    "temperature": 0.6,
    "minumum_prompt_words": 3

}
quiz_generator = QuizGenerator(config)


def quiz_iterator():
    for qz in questions:
        yield


global data_quiz
data_quiz = [Quiz(**x) for x in questions]

# Stages
START_ROUTES, MIDDLE_ROUTES, END_ROUTES = range(3)
# Callback data
ONE, TWO, THREE, FOUR = range(4)


def is_correct_option_selected(option_idx, options):
    if options[option_idx].voter_count == 1:
        return True
    else:
        return False


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Inform user about what this bot can do"""
    await update.message.reply_text(
        "Please select /poll to get a Poll, /quiz to get a Quiz or /preview"
        " to generate a preview for your poll"
    )


async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if not context.bot_data.get('question_index', 0):
        context.bot_data["question_index"] = 0
    question_index = context.bot_data["question_index"]
    if question_index == len(data_quiz):
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Quizzes are Over!")
        return
    # print("question_text :", len(data_quiz[question_index].question_text))
    # print("options       :", [len(x)
    #       for x in data_quiz[question_index].options])
    # print("explanation   :", len(data_quiz[question_index].explanation))

    message = await update.effective_message.reply_poll(
        data_quiz[question_index].question_text, data_quiz[question_index].options, type=Poll.QUIZ,
        correct_option_id=data_quiz[question_index].correct_option_idx
    )
    # Save some info about the poll the bot_data for later use in receive_quiz_answer
    payload = {
        message.poll.id: {"chat_id": update.effective_chat.id,
                          "message_id": message.message_id,
                          "question_index": question_index,
                          "explanation": data_quiz[question_index].explanation}
    }
    context.bot_data.update(payload)


async def explanation(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Ask the user for a description of a custom category."""
    await update.message.reply_text(
        'Alright, please send me the category first, for example "Most impressive skill"'
    )


async def receive_quiz_answer(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    if update.poll.is_closed:
        return
    try:
        quiz_data = context.bot_data[update.poll.id]
    # this means this poll answer update is from an old poll, we can't stop it then
    except KeyError:
        return
    if quiz_data["explanation"]:
        await context.bot.send_message(
            quiz_data["chat_id"],
            quiz_data["explanation"]
        )
    await context.bot.stop_poll(quiz_data["chat_id"], quiz_data["message_id"])
    context.bot_data['question_index'] += 1
    # print("context.bot_data['question_index']",
    #       context.bot_data['question_index'])

    keyboard = [
        [InlineKeyboardButton('Next', callback_data='next')],
    ]
    keyboard = InlineKeyboardMarkup(keyboard)
    await context.bot.send_message(chat_id=quiz_data["chat_id"], text="Please choose:", reply_markup=keyboard)


def clean_prompt(data):
    k = re.compile(r"^prompt\s*:*\s*", re.IGNORECASE)
    return k.sub("", data, 1)


def word_count(x): return len(x.split())


async def handle_message(update, context):
    context.bot_data["question_index"] = 0
    message = update.message
    prompt = clean_prompt(message.text)
    if word_count(prompt) >= config["minumum_prompt_words"]:
        await context.bot.send_message(chat_id=update.effective_chat.id, text="Please wait getting data ready")
        quizzes = quiz_generator.generate_quizzes(
            topic_prompt=prompt)
        if quizzes:
            document = {"questions": quizzes, "prompt": prompt,
                        "datetime": datetime.datetime.now(tz=datetime.timezone.utc)}
            mongo_collection().insert_one(document)
            global data_quiz
            data_quiz = [Quiz(**x) for x in quizzes]
            await context.bot.send_message(chat_id=update.effective_chat.id, text="Ready!, you can start /quiz")
        else:
            await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Didn't get quizzes for the topic :{prompt}")
    else:
        await context.bot.send_message(chat_id=update.effective_chat.id, text=f"Incorrect prompt! minimum three words, but {word_count(prompt)} given")


async def help_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Display a help message"""
    await update.message.reply_text("Use /quiz, /poll or /preview to test this bot.")


def telegram_polling():
    """Run bot."""
    # Create the Application and pass it your bot's token.
    application = Application.builder().token(bot_token()).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("quiz", quiz))
    application.add_handler(MessageHandler(
        filters.Regex(re.compile(r"^prompt", re.IGNORECASE)), callback=handle_message))
    application.add_handler(CallbackQueryHandler(
        quiz))  # , pattern="^" + "next" + "$"
    application.add_handler(CommandHandler("help", help_handler))
    application.add_handler(PollHandler(receive_quiz_answer))

    # Run the bot until the user presses Ctrl-C
    print("application is running ...")
    application.run_polling()


if __name__ == "__main__":
    telegram_polling()
