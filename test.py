
import methods as met


text="hello word"

key = met.easGenKey()
cft = met.easEncWhithKey(text.encode('utf-8'), key)

encryted = met.easdecWhithKey(cft, key)

print(encryted.decode('utf-8'))