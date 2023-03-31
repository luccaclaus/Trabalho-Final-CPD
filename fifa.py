import csv
import time

CSV_PLAYERS_SIZE = 22787
CSV_RATINGS_SIZE = 24188069
CSV_MINIRATINGS_SIZE = 10007

def hashPolinomial(id, size):
    numerals = str(id).split()
    length = len(numerals)
    a = 31
    polinomio = 0
    for j in range(0, length):
        polinomio = polinomio + int(numerals[j]) * a ** j
    key = polinomio % size
    return key

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

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


class TrieTagsNode:
    def __init__(self):
        self.children = [None] * 27  # a = 0 , b = 1 , ... z = 25, outros = 26
        self.players = []

class TrieTags:
    def __init__(self):
        self.root = TrieTagsNode()
        
    def getCharIndex(self, char):
        char = char.lower()
        if ord(char) > ord('a') and ord(char) < ord('z'):
            return ord(char) - 97
        else: 
            return 26
            

    def makeNewNode(self):
        return TrieTagsNode()

    def insert(self, string, id):
        current_node = self.root
        for char in string:
            index = self.getCharIndex(char)
            if not current_node.children[index]:
                current_node.children[index] = self.makeNewNode()
            current_node = current_node.children[index]
        if id not in current_node.players:
            current_node.players.append(id)
    
    def searchNode(self, string):
        current_node = self.root
        for char in string:
            index = self.getCharIndex(char)
            if not current_node.children[index]:
                return False
            else:
                current_node = current_node.children[index]

        return current_node

    def get_tags_players(self, tags):
        intersec = self.searchNode(tags[0]).players
        for tag in tags:
            intersec = intersection(intersec, self.searchNode(tag).players)
        return intersec

            
 
        
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
        if cell:
            for item in cell:
                if item.id == id:
                    return item
        return False

    def get_best(self, N, position):
        players_in_position = []
        for cell in self.table:
            if cell:
                for player in cell:
                    if player.ratings_count >= 1000 and position in player.positions:
                        players_in_position.append((player.id, player.get_global_rating()))

        players_in_position.sort(key=lambda t: t[1], reverse=True)

        top_players_id = []
        for tuple in players_in_position[0:N]:
            top_players_id.append(tuple[0])

        return top_players_id

    # def get_tags_intersec(self, tags_list):
    #     result = []
    #     for cell in self.table:
    #        if cell:
    #            for player in cell:
    #                 if tag1 in player.tags and tag2 in player.tags:
    #                     result.append(player.id)
                   


class Player:
    def __init__(self, id, name, positions):
        self.id = id
        self.name = name
        self.positions = positions
        self.total_score = 0
        self.ratings_count = 0
        self.tags = []

    def get_global_rating(self):
        if self.ratings_count != 0:
            return self.total_score / self.ratings_count
        else:
            return 0


class Review:
    def __init__(self,player_id, score):
        self.player_id = player_id
        self.score = score

class User:
    def __init__(self,id, ratings):
        self.id = id
        self.ratings = ratings
        
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


def read_ratings_csv(file, hash_players, hash_users):
    with file as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        # Leitura dos dados
        for line in csv_reader:
            user_id = line[0]
            player_id = line[1]
            score = float(line[2])
            rating = Review(player_id, score)

            # Salva user e rating
            target_user = hash_users.search(user_id)
            if target_user:
                target_user.ratings.append(rating)
            else:
                hash_users.insert(User(user_id, [rating]))
            # Salva Player
            target_player = hash_players.search(player_id)
            target_player.ratings_count = target_player.ratings_count + 1
            target_player.total_score = target_player.total_score + score

def read_tags_csv(file, tags_trie):
    with file as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        # Leitura dos dados
        for line in csv_reader:
            player_id = line[1]
            tag = line[2]

            tags_trie.insert(tag, player_id)






"""
# Códigos de questões
"""

def search_by_name(name, names_trie, hash_table):

    search_result = names_trie.findAllPlayers(name)
    for id in search_result:
        player = hash_table.search(id)

        print(
            player.id,
            player.name,
            player.positions,
            player.get_global_rating(),
            player.ratings_count)
"""
# Testes
"""
"""
# arquivos
"""
players_f = open('INF01124_FIFA21_clean/players.csv', 'r')
ratings_f = open('INF01124_FIFA21_clean/minirating.csv', 'r')
tags_f = open('INF01124_FIFA21_clean/tags.csv')

"""
# Criacao das estruturas
"""
start_time = time.time()

players_hash = HashTable(CSV_PLAYERS_SIZE, hashPolinomial)
players_name_trie = Trie()

users_hash = HashTable(CSV_RATINGS_SIZE, hashPolinomial)

trie_tags = TrieTags()
print("Criacao das estruturas:")
print("--- %s seconds ---" % (time.time() - start_time))

"""
# leitura dos arquivos
"""
start_time = time.time()
read_players_csv(players_f, players_hash, players_name_trie)
print("Trie jogadores:")
print("--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
read_ratings_csv(ratings_f, players_hash,users_hash)
print("Hash ratings:")
print("--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
read_tags_csv(tags_f,trie_tags)
print("Trie tags:")
print("--- %s seconds ---" % (time.time() - start_time))

"""
# questão 2.1
"""
print("QUESTÃO 2.1\n")
start_time = time.time()

search_by_name('Matt', players_name_trie,players_hash)

print("--- %s seconds ---" % (time.time() - start_time))


"""
#questao 2.2
"""
print("\n\nQUESTÃO 2.2\n")

def get_user_ratings(user_id, hash_players):
    user = users_hash.search('60040')

    for rating in user.ratings:
        rated_player = hash_players.search(rating.player_id)
        print(rated_player.id,
              rated_player.name,
              rated_player.get_global_rating(),
              rated_player.ratings_count,
              rating.score)

get_user_ratings('119743', players_hash)


"""
#questâo 2.3
"""
print("\n\nQUESTÃO 2.3\n")


start_time = time.time()

best_players_id = players_hash.get_best(10, 'RB')
for id in best_players_id:
    pl = players_hash.search(id)
    print(pl.id, pl.name, pl.positions ,pl.get_global_rating(), pl.ratings_count)

print("--- %s seconds ---" % (time.time() - start_time))

"""
#questâo 2.4
"""
print(("QUESTAO 2.4"))
players_with_tags = trie_tags.get_tags_players(['Brazil','Dribbler'])
for pl_id in players_with_tags:
    pl_data = players_hash.search(pl_id)
    if pl_data:
        print(
              pl_data.id,
              pl_data.name,
              pl_data.positions,
              pl_data.get_global_rating(),
              pl_data.ratings_count
              )




