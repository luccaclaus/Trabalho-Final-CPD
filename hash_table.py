import pandas as pd
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
            print('-------')
            for item in cell:
                print(vars(item))
        print('\n\n')


class Player:
    def __init__(self, id, name, positions):
        self.id = id
        self.name = name
        self.positions = positions


def read_players_csv(file, hash_table):
    with file as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            id = line[0]
            name = line[1]
            positions = []

            for position in line[2].split(','):
                positions.append(position)
            hash_table.insert(Player(id, name, positions))


# Testes

players_f = open('INF01124_FIFA21_clean/players.csv', 'r')
players_hash = HashTable(CSV_PLAYERS_SIZE)

read_players_csv(players_f, players_hash)

players_hash.print()