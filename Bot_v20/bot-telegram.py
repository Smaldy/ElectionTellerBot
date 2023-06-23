import logging

from telegram import __version__ as TG_VER

try:
    from telegram import __version_info__
except ImportError:
    __version_info__ = (0, 0, 0, 0, 0)  # type: ignore[assignment]

if __version_info__ < (20, 0, 0, "alpha", 1):
    raise RuntimeError(
        f"This example is not compatible with your current PTB version {TG_VER}. To view the "
        f"{TG_VER} version of this example, "
        f"visit https://docs.python-telegram-bot.org/en/v{TG_VER}/examples.html"
    )


from typing import Final
import os
import csv
import numpy as np
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes
# Enable logging
logging.basicConfig(
    format="%(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

print('Starting up bot...')

token_name = 'token.txt'
token_dir = os.path.dirname(os.path.abspath(__file__))
token_path = os.path.join(token_dir, token_name)

with open(token_path, "r") as f:
    TOKEN: Final = f.read().strip()

BOT_USERNAME: Final = '@GlustBot'
matrix = None
def load_data():
    global matrix
    try:
        file_name = 'Elezioni_Villafranca.CSV'
        current_dir = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(current_dir, file_name)
        with open(file_path, 'r') as file:
            csv_reader = csv.reader(file)
            matrix = np.array(list(csv_reader))
    except FileNotFoundError:
        print("File CSV non trovato.")
        matrix = np.array([])
################################################################################################





async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("informazioni", callback_data="1"),
            InlineKeyboardButton("Astenuti", callback_data="2"),
        ],
        [InlineKeyboardButton("Liste", callback_data="3"),
         InlineKeyboardButton("Candidati", callback_data="4")],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Ciao, Sono ElectionTeller", reply_markup=reply_markup)


async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
  
    query = update.callback_query

    await query.answer()
    print(query.data)
    opzione = int(query.data)
    if opzione == 1:
        await info(update, context)
    elif opzione == 2:
        await astenuti(update, context)
    elif opzione == 3:
        await liste(update, context)
    elif opzione == 4:
        await candidati(update, context)


async def astenuti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 9 e 56
    await update.callback_query.message.edit_text('il numero di astenuti è :')

async def liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.callback_query.message.edit_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    
    liste = matrix[0, 2] + matrix [0, 4] + matrix[0,6]
    await update.callback_query.message.edit_text(liste)
    

async def candidati(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.callback_query.message.edit_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    lista_sindaci = matrix[0, 1] + matrix [0,3] + matrix[0,5]
    await update.callback_query.message.edit_text(lista_sindaci)
    


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = "Benvenuto! Questo è un bot per le elezioni di Villafranca.\n\n" \
                "Ecco i comandi disponibili:\n" \
                "/Astenuti - Mostra il numero di astenuti\n" \
                "/start - Avvia il bot\n" \
                "/info - Mostra le informazioni sul bot e i comandi disponibili\n" \
                "/Candidati - Mostra i candidati sindaci\n" \
                "/astenuti - Mostra il numero di astenuti\n" \
                "/mostraVincitore - Mostra il vincitore delle elezioni\n" \
                "/liste - Mostra le liste\n" \
                "/DoveVotare - Mostra i luoghi di voto\n" \
                "/stop - Arresta il bot"
    await update.callback_query.message.edit_text(info_text)


#####################################################################################################################


# Log errors
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused error {context.error}')


# Run the program
if __name__ == '__main__':
    load_data()
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CallbackQueryHandler(button))
    # Log all errors
    app.add_error_handler(error)
    

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
