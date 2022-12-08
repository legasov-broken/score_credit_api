from lib import *
from credit_score import credit_score


def score_users(input):

    # sort user's data
    input["A"] = input.pop("id")
    input = collections.OrderedDict(sorted(input.items()))

    # extract each user data from .json
    ext = []
    for ele in input:
        ext_ = np.array(input[ele])
        ext.append(ext_)
    ext = np.array(ext)
    ext = np.transpose(ext)
    ext_ = ext[:,1:]

    # take id of users
    id = ext[:,0]

    # caculate each user's score from their data
    score = []
    for idx,val in enumerate(ext_):
        score_ = credit_score(ext_[idx,:])
        score.append(score_)

    # collab id and score

    result = {}
    result["id"] = id.tolist()
    result["score"] = score

    return result










