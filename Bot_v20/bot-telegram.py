from typing import Final
import os
import csv
import numpy as np
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')

TOKEN: Final = '6265945877:AAGeiaPR9mmYXT_6xCGo-gN5fGGyUqBuXAI'
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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('"Ciao! Usa il comando /info per visualizzare le mie funzioni!"')

async def astenuti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('il numero di astenuti è :')

async def liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    
    liste = matrix[0, 2] + matrix [0, 4] + matrix[0,6]
    await update.message.reply_text(liste)

async def candidati(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    lista_sindaci = matrix[0, 1] + matrix [0,3] + matrix[0,5]
    await update.message.reply_text(lista_sindaci)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = "Benvenuto! Questo è un bot per le elezioni di Villafranca.\n\n" \
                "Ecco i comandi disponibili:\n" \
                "/start - Avvia il bot\n" \
                "/info - Mostra le informazioni sul bot e i comandi disponibili\n" \
                "/Candidati - Mostra i candidati sindaci\n" \
                "/astenuti - Mostra il numero di astenuti\n" \
                "/mostraVincitore - Mostra il vincitore delle elezioni\n" \
                "/liste - Mostra le liste\n" \
                "/Astenuti - Mostra il numero di astenuti\n" \
                "/DoveVotare - Mostra i luoghi di voto\n" \
                "/stop - Arresta il bot"
    await update.message.reply_text(info_text)


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
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('candidati', candidati))
    app.add_handler(CommandHandler('astenuti', astenuti))
    app.add_handler(CommandHandler('Liste',liste))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=2)
