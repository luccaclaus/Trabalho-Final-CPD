import csv
import time
from Classes import *

CSV_PLAYERS_SIZE = 22787
CSV_RATINGS_SIZE = 24188089
CSV_MINIRATINGS_SIZE = 10007



# Leitura de dados em CSV
def read_players_csv(file, hash_table, trie):
    with file as csv_file:
        csv_reader = csv.reader(csv_file)
        next(csv_reader)
        for line in csv_reader:
            id = line[0]
            name = line[1]
            positions = line[2].split(', ')

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

# Funções auxiliares
def get_string_arguments(user_inp):
    tags_untreated = user_inp.split("'")[1:]
    tags = list(filter(lambda x: x != '' and x != ' ', tags_untreated))
    return tags

"""
# Códigos de questões
"""
# QUESTÂO 2.1 #
def search_by_name(name, names_trie, hash_table):

    search_result = names_trie.findAllPlayers(name)
    if search_result == []:
        print("Nenhum jogador tem esse nome!")
    else:
        for id in search_result:
            player = hash_table.search(id)

            print(
                player.id,
                player.name,
                player.positions,
                player.get_global_rating(),
                player.ratings_count)

# QUESTÂO 2.2 #
def get_user_ratings(user_id, hash_players):
    user = users_hash.search(user_id)
    if user:
        for rating in user.ratings:
            rated_player = hash_players.search(rating.player_id)
            print(rated_player.id,
                rated_player.name,
                rated_player.get_global_rating(),
                rated_player.ratings_count,
                rating.score)
    else: 
        print("\nInsira um usuário existente!")

"""
# arquivos
"""
players_f = open('INF01124_FIFA21_clean/players.csv', 'r')
ratings_f = open('INF01124_FIFA21_clean/rating.csv', 'r')
tags_f = open('INF01124_FIFA21_clean/tags.csv')

"""
# Criacao das estruturas
"""
start_time = time.time()

players_hash = HashTable(CSV_PLAYERS_SIZE, hashIdentidade)

players_name_trie = Trie()

users_hash = HashTable(CSV_RATINGS_SIZE, hashIdentidade)

trie_tags = TrieTags()
print("Tempo para criacao das estruturas:")
print("--- %s seconds ---" % (time.time() - start_time))

"""
# leitura dos arquivos
"""
start_time = time.time()
read_players_csv(players_f, players_hash, players_name_trie)
print("\n\nÁrvore Trie e Hash de jogadores:")
print("--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
read_ratings_csv(ratings_f, players_hash,users_hash)
print("\n\nHash de usuários:")
print("--- %s seconds ---" % (time.time() - start_time))


start_time = time.time()
read_tags_csv(tags_f,trie_tags)
print("\n\nÁrvore Trie de tags (comentários):")
print("--- %s seconds ---" % (time.time() - start_time))


positions = ["ST", "GK", "LW", "RW", "CF", "CAM", "CM", "CDM", "LM", "RM", "CB", "LB", "RB", "RWB", "LWB"]
user_input = ""

while user_input != "off":
    user_input = input("\nDigite comando: ")
    command = user_input.split(" ")
    if user_input != "off":
        funct_name = command[0]
        args = command[1:] #argumentos: todas as palavras passadas depois do nome da funcao

        #match funct_name:
        # PLAYER: busca por nome
        if funct_name == "player":
            name_prefix = ' '.join(args)
            search_by_name(name_prefix, players_name_trie,players_hash)
        elif funct_name == "user":
            user_id = args[0]  # argumento unico
            get_user_ratings(user_id, players_hash)
        # TAGS: busca por tags
        elif funct_name == "tags":
            # tags_untreated = user_input.split("'")[1:]
            # tags = list(filter(lambda x: x!= '' and x!= ' ', tags_untreated))
            tags = get_string_arguments(user_input)

            players_with_tags = trie_tags.get_tags_players(tags)
            if not players_with_tags:
                print("Nenhum jogador possui essas tags!\n")
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
        #TOPN: busca top N por posição
        else:
            if funct_name[0:3] == "top":
                n_top = int(funct_name[3:])
                pos = args[0] #argumento unico (posicao)
                if n_top >= 1:
                    if pos in positions:
                        best_players_id = players_hash.get_best(n_top, pos)
                        for id in best_players_id:
                            pl = players_hash.search(id)
                            print(pl.id, pl.name, pl.positions ,pl.get_global_rating(), pl.ratings_count)
                    else:
                        print("\nInsira uma posiçâo válida!")
                else:
                    print("Insira um número positivo!")
            else: print("\nComando inválido!")

