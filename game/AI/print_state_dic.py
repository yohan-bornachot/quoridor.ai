dic = {}
l = ["u", "d", "l", "r", "uu", "dd", "ll", "rr", "ur", "ul", "dr", "dl"]
i=0
for x in l:
    dic[x] = i
    i += 1

for k in range(8):
    for l in range(8):
        dic["h{}.{}".format(k,l)]=i
        i += 1
        dic["v{}.{}".format(k,l)]=i
        i += 1

print("state_dic = {", end="")       
for k,x in enumerate(dic):
    print("'{}' : {}".format(x,dic[x]), end="")
    if k != len(dic)-1: print(", ", end = "")
    if (k+1)%12 == 0: print("")
print("}")


