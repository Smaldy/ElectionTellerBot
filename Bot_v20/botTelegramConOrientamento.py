from typing import Final
import os
import csv
import numpy as np
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

print('Starting up bot...')


TOKEN ='5963731424:AAFJR6VFiVqjaK8E0ieV8ayhkvIEr8h9R5k'


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



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('"Ciao! Usa il comando /info per visualizzare le mie funzioni!"')

async def astenuti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 9 e 56 totale astenuti
    if matrix is None or matrix.size == 0:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    totaleAstenuti = matrix[55, 9]
    print("ciao"+totaleAstenuti)
    await update.message.reply_text("Nelle elezioni di Villafranca i cittadini che hanno deciso di non andare al seggio sono stati: "
                                     + totaleAstenuti)

async def liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    
    liste = "Le liste candidate alle elezioni di villafranca sono: " + matrix[0, 2] + matrix [0, 4] + matrix[0,6]
    await update.message.reply_text(liste)

async def candidati(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    lista_sindaci = "La lista dei candidati sindaci di villafranca sono: " + matrix[0, 1] + matrix [0,3] + matrix[0,5]
    await update.message.reply_text(lista_sindaci)

"""
async def datiElezioniSezioni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    #questo nn serve
    #j = 0
    #for var in range(1,6,2):
    #    while j < 56:
    #        print("ciao")
    #        faccioli += str(matrix[j,0])+matrix[j,var]
    #        j+=1
    #
    i = 0
    orientamento = "l'orientamento politico verrà presentato in questa disposizione\nSezione; e il numero di voti che anno preso "+matrix[0, 1] +" "+ matrix [0,3]+" "+ matrix[0,5]+"\n"
    while i < 55:
        if(i%2 != 0):
            #sezioni = sezioni + str(matrix[i,0]+" ;")
            orientamento = orientamento +"; "+matrix[i,0]+"; "+matrix[i,1]+"; "+matrix[i,3]+"; "+matrix[i,5]+"\n"
        i+=1

    await update.message.reply_text(orientamento)
"""
async def orientamentiPoliticiSezioni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    popolazione #popolazione più di destra o di sinista

    if(matrix[55,1] < matrix[55,3] and matrix[55,1] < matrix[55,5]):
        popolazione = "Ha vinto "+matrix[55,1]
    elif(matrix[55,1] < matrix[55,3] and matrix[55,1] < matrix[55,5]):
        popolazione = "Ha vinto "+matrix[55,3]
    else:
        popolazione = "Ha vinto "+matrix[55,5]
    await update.message.reply_text(popolazione)


async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = "Benvenuto! Questo è un bot per le elezioni di Villafranca.\n\n" \
                "Ecco i comandi disponibili:\n" \
                "/start - Avvia il bot\n" \
                "/info - Mostra le informazioni sul bot e i comandi disponibili\n" \
                "/Candidati - Mostra i candidati sindaci\n" \
                "/astenuti - Mostra il numero di astenuti\n" \
                "/mostraVincitore - Mostra il vincitore delle elezioni\n" \
                "/liste - Mostra le liste\n" \
                "/orientamenti - Mostra gli orientamenti politici in ogni sezione\n" \
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
    app = Application.builder().token('5819210026:AAECJTbhz0RGHL-l2W4l29yqgmLNIlsWzys').build()

    # Commands
    app.add_handler(CommandHandler('start', start))
    app.add_handler(CommandHandler('info', info))
    app.add_handler(CommandHandler('candidati', candidati))
    app.add_handler(CommandHandler('astenuti', astenuti))
    app.add_handler(CommandHandler('Liste',liste))
    #app.add_handler(CommandHandler('datiElezioniSezioni',datiElezioniSezioni))
    app.add_handler(CommandHandler('orientamenti',orientamentiPoliticiSezioni))

    # Log all errors
    app.add_error_handler(error)

    print('Polling...')
    # Run the bot
    app.run_polling(poll_interval=2)
