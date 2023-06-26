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

###########################################################################################################################################

# mostra in chat i bottoni - show in the chat the botton
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    keyboard = [
        [
            InlineKeyboardButton("informazioni", callback_data="1"),
            InlineKeyboardButton("Astenuti", callback_data="2"),
        ],
        [
            InlineKeyboardButton("Liste", callback_data="3"),
            InlineKeyboardButton("Candidati", callback_data="4"),
        ],
        [
            InlineKeyboardButton("Orrientamento", callback_data="5"),
            InlineKeyboardButton("Vincitori", callback_data="6"),
        ],
        [
            InlineKeyboardButton("Votazioni delle Sezioni", callback_data="7"),
            InlineKeyboardButton("Solo donne", callback_data="8"),
        ],
        [
            InlineKeyboardButton("Votanti", callback_data="9"),
            InlineKeyboardButton("Solo uomini", callback_data="10"),
        ],
        [
            InlineKeyboardButton("Votazioni attese", callback_data="11"),
            InlineKeyboardButton("Inscritti", callback_data="12"),
        ],
        [
            InlineKeyboardButton("Totale voti",callback_data="13"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Ciao, Sono ElectionTeller", reply_markup=reply_markup)

# settaggio dei bottoni - set of button
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
    elif opzione == 5:
        await orientamentoPolitico(update, context)
    elif opzione == 6:
        await Vincitore(update, context)
    elif opzione == 7:
        await datiElezioniSezioni(update, context)
    elif opzione == 8:
        await soloDonne(update, context)
    elif opzione == 9:
        await votanti(update, context)
    elif opzione == 10:
        await soloUomini(update, context)
    elif opzione == 11:
        await votazioniAttese(update, context)
    elif opzione == 12:
        await inscritti(update, context)
    elif opzione == 13:
        await totaliVotiCandidati(update, context)

# mostra il vicitore delle elezioni - show the winner of the election
async def Vincitore(update: Update, context: ContextTypes.DEFAULT_TYPE):
    popolazione =""     #popolazione più di destra o di sinista

    # per ogni riga controlla quale dei candidati ha vinto le elezioni
    if(matrix[55,1] < matrix[55,3] and matrix[55,1] < matrix[55,5]):
        popolazione = "Ha vinto "+matrix[0,1]+" con "+matrix[55,1]+" votazioni"
    elif(matrix[55,1] < matrix[55,3] and matrix[55,1] < matrix[55,5]):
        popolazione = "Ha vinto "+matrix[0,3]+" con "+matrix[55,3]+" votazioni"
    else:
        popolazione = "Ha vinto "+matrix[0,5]+" con "+matrix[55,5]+" votazioni"

    await update.callback_query.message.edit_text(popolazione)
async def orientamentoPolitico(update: Update, context: ContextTypes.DEFAULT_TYPE):
    i=0
    orientamento = ""
    while i< 55:
        if(i%2!=0):
            if(matrix[i,1] < matrix[i,3] and matrix[i,1] < matrix[i,5]):
                orientamento += "Nella sezione "+matrix[i,0]+" c'è una maggioranza per il candidato civico\n"
            elif(matrix[i,1] < matrix[i,3] and matrix[i,0] < matrix[i,5]):
                orientamento += "Nella sezione "+matrix[i,0]+" c'è una maggioranza di centrosinitra\n"
            else:
                orientamento += "Nella sezione "+matrix[i,0]+" c'è una maggioranza di centrodestra\n"
        i+=1
    await update.callback_query.message.edit_text(orientamento)




# mosta i risultati delle elezioni - show the result of the election 
async def datiElezioniSezioni(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.message.reply_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return

    i = 0

    orientamento = "l'orientamento politico verrà presentato in questa disposizione\nSezione; e il numero di voti che anno preso "+matrix[0, 1] +" "+ matrix [0,3]+" "+ matrix[0,5]+"\n"
    while i < 55:
        if(i%2 != 0):
            orientamento += "Sezione: "+matrix[i,0]+" | "+matrix[i,1]+" | "+matrix[i,3]+" | "+matrix[i,5]+"\n"
        i+=1

    await update.callback_query.message.edit_text(orientamento)

# mostra gli astenuti alle elezioni
async def astenuti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    # 56 e 9 totale astenuti
    if matrix is None or matrix.size == 0:
        await update.callback_query.message.edit_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    
    totaleAstenuti = matrix[55, 9]
    
    await update.callback_query.message.edit_text("Nelle elezioni di Villafranca i cittadini che hanno deciso di non andare al seggio sono stati: "
                                     + totaleAstenuti)

# mostra le liste dei candidati - show the list of candidate
async def liste(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.callback_query.message.edit_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    
    liste = f"{matrix[0, 2]}\n{matrix [0, 4]}\n{matrix[0,6]}"
    await update.callback_query.message.edit_text(liste)


async def soloDonne(update: Update, context: ContextTypes.DEFAULT_TYPE):
    donne = ""
    i = 0
    while i < 55:
        if(i % 2 != 0):
            donne += "Sezione: "+matrix[i,0]+" votazioni: "+matrix[i,13]+"\n"
        i+=1
    
    await update.callback_query.message.edit_text(donne)

async def soloUomini(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uomini = ""
    i = 0

    while i < 55:
        if(i%2 != 0):
            uomini += "Sezioni: "+matrix[i,0]+" votazioni: "+matrix[i,12]+"\n"
        i+=1
    await update.callback_query.message.edit_text(uomini)

async def votanti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    votanti = ""
    i = 0

    while i<55:
        if(i%2!=2):
            votanti+=matrix[i,14]
    i+=1
    await update.callback_query.message.edit_text(votanti)

async def inscritti(update: Update, context: ContextTypes.DEFAULT_TYPE):
    inscritti = ""
    i = 0

    while i<55:
        if(i%2!=0):
            inscritti+= "Sezioni: "+matrix[i,0]+" votanti:"+matrix[i,15]+"\n"
        i+=1
    await update.callback_query.message.edit_text(inscritti)

async def votazioniAttese(update: Update, context: ContextTypes.DEFAULT_TYPE):
    votazioni = "Erano attese "+(matrix[57,16]-matrix[56,15])+" votazioni.\nHanno votato il "+matrix[58,15]+" ovvero "+matrix[59,15]
    await update.callback_query.message.edit_text(votazioni)

async def totaliVotiCandidati(update: Update, context: ContextTypes.DEFAULT_TYPE):
    totale = matrix[0,1]+ "ha preso "+matrix[57,1]+" votazioni.\n"+matrix[0,3]+"ha avuto "+matrix[57,3]+" votazioni.\n"+matrix[0,5]+" ha avuto "+matrix[57,5]+" votazioni."
    await update.callback_query.message.edit_text(totale)

# mostra i candidati
async def candidati(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if matrix is None or matrix.size == 0:
        await update.callback_query.message.edit_text(chat_id=update.effective_chat.id, text="Dati non disponibili.")
        return
    lista_sindaci = f"{matrix[0, 1]}\n{matrix [0,3]}\n{matrix[0,5]}"
    await update.callback_query.message.edit_text(lista_sindaci)

# mostra le informazioni riguardanti i comandi eseguibili
async def info(update: Update, context: ContextTypes.DEFAULT_TYPE):
    info_text = "Benvenuto! Questo è un bot per le elezioni di Villafranca.\n\n" \
                "Ecco i comandi disponibili:\n" \
                "Astenuti: Mostra il numero di astenuti\n" \
                "/start: - Avvia il bot\n" \
                "info: Mostra le informazioni sul bot e i comandi disponibili\n" \
                "Candidati: Mostra i candidati sindaci\n" \
                "Astenuti: Mostra il numero di astenuti\n" \
                "Vincitore: Mostra il vincitore delle elezioni\n" \
                "liste: Mostra le liste\n" \
                "DatiSezioniElezione: mostra le votazioni che hanno preso ogni candidato in ogni sezione\n" \
                "orientamento politico: mostra per ogni sezione la maggioranza politica"
    await update.callback_query.message.edit_text(info_text)


############################################################################################################################################


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