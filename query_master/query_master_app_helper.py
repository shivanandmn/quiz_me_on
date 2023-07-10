from telegram import (
    Update
)
from query_master.query_master import load_query_db
qa_chain = None
async def pdf_handler(update: Update, context):
    file = context.bot.get_file(update.message.document.file_id)
    save_file = f'query_master/docs/{update.effective_chat.id}.pdf'
    file.download(save_file)  # Save the PDF file locally
    global qa_chain
    qa_chain = load_query_db(save_file, chain_type="stuff", k=4)
    # Respond back to the user
    await update.message.reply_text(chat_id=update.effective_chat.id, text="I understood your doc. You can /ask_me any questions")

async def ask_me(update: Update, context):
    pass