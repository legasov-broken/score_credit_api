from lib import *




source = open('./WOE_dict_sorted.json')
data = json.load(source)

# od = collections.OrderedDict(sorted(data.items()))
# with open("WOE_dict_sorted.json", "w") as outfile:
#     json.dump(od, outfile)

def credit_score(cs):
    score = 0
    for i,ele in enumerate(data):
        for j in data[ele]:
            a = np.array(data[ele][j])
            if a[0] < cs[i] < a[1]:
                score = score+float(j)
                break
    return score

    