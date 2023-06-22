import csv

matrice = []

with open(r'C:\Users\ayman\Documents\GitHub\ElectionTellerBot\Bot_bottoni\Elezioni_Villafranca.CSV', 'r') as file:
    reader = csv.reader(file, delimiter=';')
    for row in reader:
        matrice.append(row)

prova= matrice[0]
print(prova[0])