import pandas as pd
import numpy as np
import csv
import time 

CSV_PLAYERS_SIZE = 22787
CSV_RATINGS_SIZE = 24188069

start_time = time.time()

def hashPolinomial(id, size):
    numerals = str(id).split()
    length = len(numerals)
    a = 31
    polinomio = 0
    for j in range(0, length):
        polinomio = polinomio + int(numerals[j]) * a ** j
    key = polinomio % size
    return key


class TrieNode:
    def __init__(self):
        self.children = [None] * 27  # a = 0 , b = 1 , ... z = 25, outros = 26
        self.player_id = 0


class Trie:
    def __init__(self):
        self.root = TrieNode()

    def getCharIndex(self, char):
        char = char.lower()
        if char == ' ' or char == '-' or char == "'" or char == '.' or char == '"':
            return 26
        else:
            return ord(char) - 97

    def makeNewNode(self):
        return TrieNode()

    def insert(self, string, id):
        current_node = self.root
        for char in string:
            index = self.getCharIndex(char)
            if not current_node.children[index]:
                current_node.children[index] = self.makeNewNode()
            current_node = current_node.children[index]
        current_node.player_id = id

    def searchNode(self, string):
        current_node = self.root
        for char in string:
            index = self.getCharIndex(char)
            if not current_node.children[index]:
                return False
            else:
                current_node = current_node.children[index]

        return current_node

    def findAllAncestors(self, node):
        if node is not None:
            current_node = node
            player_ids = []
            children_ids = []
            if current_node.player_id:
                player_ids.append(current_node.player_id)
            for child in current_node.children:
                if child is not None:
                    children_ids = children_ids + self.findAllAncestors(child)
            player_ids = player_ids + children_ids
            return player_ids

    def findAllPlayers(self, string):
        start_node = self.searchNode(string)
        return self.findAllAncestors(start_node)


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
        self.total_score = 0
        self.ratings_count = 0


class Rating:
    def __init__(self, id, player_id, rating):
        self.id = id
        self.player_id = player_id
        self.rating = rating


def read_players_csv(file, hash_table, trie):
    with file as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            id = line[0]
            name = line[1]
            positions = line[2].split(',')

            hash_table.insert(Player(id, name, positions))
            trie.insert(name, id)


def read_ratings_csv(file, hash_players):
    with file as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            id = line[0]
            player_id = line[1]
            rating = float(line[2])

            target_player = hash_players.search(player_id)
            target_player.ratings_count = target_player.ratings_count + 1
            target_player.total_score = target_player.total_score + rating


# Testes

# arquivos
players_f = open('INF01124_FIFA21_clean/players.csv', 'r')
ratings_f = open('INF01124_FIFA21_clean/rating.csv', 'r')

# Criacao das estruturas
players_hash = HashTable(CSV_PLAYERS_SIZE, hashPolinomial)
players_name_trie = Trie()


#leitura dos arquivos
read_players_csv(players_f, players_hash, players_name_trie)
read_ratings_csv(ratings_f, players_hash)
print("--- %s seconds ---" % (time.time() - start_time))

start_time = time.time()
search_result = players_name_trie.findAllPlayers('Art')
for id in search_result:
    player = players_hash.search(id)
    print(player.id, player.name, player.positions, player.total_score/player.ratings_count)
print("--- %s seconds ---" % (time.time() - start_time))


