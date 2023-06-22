from typing import Final

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
        with open('C:/Users/ayman/Documents/GitHub/ElectionTellerBot/progettoBot/Elezioni_Villafranca.CSV', 'r') as file:
            csv_reader = csv.reader(file)
            matrix = np.array(list(csv_reader))
    except FileNotFoundError:
        print("File CSV non trovato.")
        matrix = np.array([])


# Lets us use the /start command
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('"Ciao! Usa il comando /info per visualizzare le mie funzioni!"')


# Lets us use the /help command
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = "Benvenuto! Questo è un bot per le elezioni di Villafranca.\n\n" \
                "Ecco i comandi disponibili:\n" \
                "/start - Avvia il bot\n" \
                "/info - Mostra le informazioni sul bot e i comandi disponibili\n" \
                "/listaCandidati - Mostra i candidati sindaci\n" \
                "/mostraListe - Mostra le liste dei candidati\n" \
                "/mostraVincitore - Mostra il vincitore delle elezioni\n" \
                "/mostraDonne - Mostra solo i candidati donne\n" \
                "/mostraAstenuti - Mostra il numero di astenuti\n" \
                "/mostraDoveVotare - Mostra i luoghi di voto\n" \
                "/stop - Arresta il bot"
    await update.message.reply_text(info_text)


# Lets us use the /custom command
async def lista_candidati(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    
    lista_sindaci = matrix[0, 1] + matrix [0,3] + matrix[0,5]
    await update.message.reply_text(lista_sindaci)





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
    app.add_handler(CommandHandler('listacandidati', lista_candidati))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=5)
