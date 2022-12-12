from lib import *
from credit_score import credit_score

from mapping import dict_mapping

def score_users(input):

    # sort user's data

    id_ = input['id']
    input = dict_mapping(input)
    input['id'] = id_


    # extract each user data from .json
    ext = []
    for ele in input:
        ext_ = np.array(input[ele])
        ext.append(ext_)
    ext = np.array(ext)
    ext = np.transpose(ext)
    ext_ = ext[:,1:]

    # take id of users
    id = np.array(id_)

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










