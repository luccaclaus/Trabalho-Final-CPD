def hashPolinomial(input, M):
    numerals = str(input).split()
    length = len(numerals)
    a = 31
    polinomio = 0
    for j in range(0, length):
        polinomio = polinomio + int(numerals[j]) * a ** j
    key = polinomio % M
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

myTable = HashTable(10)

messi = Player(12345, 'Messi')
geromel = Player(97854, 'Geromel')
myTable.insert(messi)
myTable.insert(geromel)

print(vars(myTable.search(97854)))



