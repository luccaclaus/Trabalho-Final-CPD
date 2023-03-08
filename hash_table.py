# import pandas as pd
import numpy as np
import csv

CSV_PLAYERS_SIZE = 22787

def hashPolinomial(id, size):
    numerals = str(id).split()
    length = len(numerals)
    a = 31
    polinomio = 0
    for j in range(0, length):
        polinomio = polinomio + int(numerals[j]) * a ** j
    key = polinomio % size
    return key

class HashTable:
    def __init__(self, size):
        self.size = size
        self.hashFunction = hashPolinomial
        self.table = []
        for i in range(0, size):
            self.table.append([])

    def insert(self, data):
        key = self.hashFunction(data.id, self.size)
        self.table[key].append(data)

    def search(self, id):
        key = self.hashFunction(id, self.size)
        cell = self.table[key]
        if not cell:
            return False
        else:
            for item in cell:
                if item.id == id:
                    return item

    def print(self):
        for cell in self.table:
            for item in cell:
                print(vars(item))
        print('\n\n')


class Player:
    def __init__(self, id, name):
        self.id = id
        self.name = name
        #self.position = position

# Testes

#players_df = pd.read_csv('http://www.inf.ufrgs.br/~comba/inf1047-files/fifa/players.csv')
#print(players_df)
#print(type(players_df))

f = open('INF01124_FIFA21_clean/players.csv')
csv_f = csv.reader(f)

#for row in csv_f:
#    print(row)

teste1 = HashTable(CSV_PLAYERS_SIZE)

for row in csv_f:
    value = int(row[0])
    # p_position  = teste1.hashFunction(value ,CSV_PLAYERS_SIZE)
    # teste1.table[p_position].append(Player(int(row[0]), row[1]))
    teste1.insert(Player(int(row[0]), row[1]))
