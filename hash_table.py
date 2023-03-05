def hashPolinomial(input, M):
    length = len(input)
    a = 31
    polinomio = 0
    for j in range(0, length):
        polinomio = polinomio + ord(input[j]) * a ** j
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
        key = self.hashFunction(data, self.size)
        print(key)
        self.table[key].append(data)

    def search(self, data):
        key = self.hashFunction(data, self.size)
        cell = self.table[key]
        if not cell:
            return False
        else:
            for item in cell:
                if item == data:
                    return item

    def print(self):
        for cell in self.table:
            print(cell)


class player:
    def __int__(self):
        self.id

myTable = HashTable(10)

myTable.insert('Rafael')
myTable.insert('Leafar')
myTable.insert('Ana')
myTable.insert('Lucca')
print(myTable.size)

myTable.print()
print(myTable.search('Leafar'))
