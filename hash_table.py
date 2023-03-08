import pandas as pd
import numpy as np
import csv

CSV_PLAYERS_SIZE = 22787
CSV_RATINGS_SIZE = 24188069

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
    def __init__(self, size, hash_funct):
        self.size = size
        self.hashFunction = hash_funct
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


class Rating:
    def __init__(self, id, player_id, rating):
        self.id = id
        self.player_id = player_id
        self.rating = rating


def read_players_csv(file, hash_table):
    with file as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            id = line[0]
            name = line[1]
            positions = line[2].split(',')

            # for position in line[2].split(','):
            #     positions.append(position)
            hash_table.insert(Player(id, name, positions))


def read_ratings_csv(file, hash_table):
    with file as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            id = line[0]
            player_id = line[1]
            rating = line[2]
            hash_table.insert(Rating(id, player_id, rating))


# Testes

# arquivos
players_f = open('INF01124_FIFA21_clean/players.csv', 'r')
ratings_f = open('INF01124_FIFA21_clean/rating.csv', 'r')

# Criacao dos Hashs
players_hash = HashTable(CSV_PLAYERS_SIZE, hashPolinomial)
read_players_csv(players_f, players_hash)

ratings_hash = HashTable(CSV_RATINGS_SIZE, hashPolinomial)
read_ratings_csv(ratings_f, ratings_hash)

#ratings_hash.print()
# players_hash.print()
