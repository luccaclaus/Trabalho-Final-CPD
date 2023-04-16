# Funções Auxiliares
def hashPolinomial(id, size):
    numerals = str(id).split()
    #numerals = id
    length = len(numerals)
    #a = 31
    a = 73
    polinomio = 0
    for j in range(0, length):
        polinomio = polinomio + int(numerals[j]) * a ** j
    key = polinomio % size
    return key

def hashIdentidade(id, size):
    return int(id)%size

def intersection(lst1, lst2):
    lst3 = [value for value in lst1 if value in lst2]
    return lst3

# Classes
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
            if current_node and current_node.player_id:
                player_ids.append(current_node.player_id)
            for child in current_node.children:
                if child is not None:
                    children_ids = children_ids + self.findAllAncestors(child)
            player_ids = player_ids + children_ids
            return player_ids

    def findAllPlayers(self, string):
        start_node = self.searchNode(string)
        if start_node:
            return self.findAllAncestors(start_node)
        else:
            return []
            # print("Nenhum jogador tem esse nome")


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
        if not tags: return []
        node = self.searchNode(tags[0])
        if node:
            intersec = node.players
        else:
            intersec = []
        for tag in tags:
            node = self.searchNode(tag)
            if node:
                intersec = intersection(intersec, node.players)
            else:
                intersec = []
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
        for tuple in players_in_position[:N]:
            top_players_id.append(tuple[0])

        return top_players_id


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
    def __init__(self, player_id, score):
        self.player_id = player_id
        self.score = score


class User:
    def __init__(self, id, ratings):
        self.id = id
        self.ratings = ratings
