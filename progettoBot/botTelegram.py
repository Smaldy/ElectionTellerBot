import csv
from telegram.ext import Updater, CommandHandler

TOKEN = "6265945877:AAGeiaPR9mmYXT_6xCGo-gN5fGGyUqBuXAI"
èFunzionante = True

matrice = []

with open(r'C:\Users\ayman\Documents\GitHub\ElectionTellerBot\Bot_bottoni\Elezioni_Villafranca.CSV', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        matrice.append(row)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Ciao! Usa il comando /info per visualizzare le mie funzioni!.")

#funzione lista_candidati
def mostra_candidati(update, context):
    riga= matrice[0]
    lista_sindaci = []
    for i in range(1,7,2):
        lista_sindaci.append(riga[i])

    row_string = ', '.join(lista_sindaci)
    context.bot.send_message(chat_id=update.effective_chat.id, text=row_string)

#funzione che mostra la lista
def mostra_liste(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="funzione non ancora funzionante")

#funzione che mostra il vincitore
def mostra_vincitore(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="funzione non ancora funzionante")

#funziona che mostra solo_donne
def mostra_solo_donne(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="funzione non ancora funzionante")

#funziona che mostra gli astenuti
def astenuti(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="funzione non ancora funzionante")
 
#funzione che mostra dove votare
def dove_votare(update,context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="funzione non ancora funzionante")

def info(update, context):
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
    context.bot.send_message(chat_id=update.effective_chat.id, text=info_text)

#funzione per arrestare il bot
def stop(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Bot arrestato sul dispositivo corrente.")
    global èFunzionante
    èFunzionante = False

def main():
    global updater
    
    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    
    mostraCandidati = CommandHandler('listaCandidati', mostra_candidati)
    inizio = CommandHandler('start', start)
    fine = CommandHandler('stop', stop)
    informazioni = CommandHandler("info", info)
    mostraListe = CommandHandler('mostraListe', mostra_liste)
    mostraVincitore = CommandHandler('mostraVincitore', mostra_vincitore)
    mostraDonne = CommandHandler('mostraDonne', mostra_solo_donne)
    mostraAstenuti = CommandHandler('mostraAstenuti', astenuti)
    mostraDoveVotare = CommandHandler('mostraDoveVotare', dove_votare)

    dispatcher.add_handler(inizio)
    dispatcher.add_handler(mostraCandidati)
    dispatcher.add_handler(fine)
    dispatcher.add_handler(informazioni)
    dispatcher.add_handler(mostraListe)  
    dispatcher.add_handler(mostraVincitore)  
    dispatcher.add_handler(mostraDonne)  
    dispatcher.add_handler(mostraAstenuti)  
    dispatcher.add_handler(mostraDoveVotare)
    updater.start_polling()
    updater.idle()

    while èFunzionante:
        try:
            updater.idle()
        except KeyboardInterrupt:
            stop(None, None)

if __name__ == '__main__':
    main()