inp = input("Tags: ")
untreated = inp.split("'")[2:]

arr = list(filter(lambda x: x!= '' and x!= ' ', untreated))
print(arr)