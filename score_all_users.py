from lib import *
from credit_score import credit_score

from mapping import dict_mapping



def score_users(source):
    
    '''
    Caculate all users' credit score and merge them into a single array.

    Parameters:
        source: array [{data_user_1},{data_user_2},{data_user_3},...]
    Example: 
    [
        {
            "_id": 23,
            "CUSTOMER_TYPE": 0,
            "CRLIMIT": 19530000,
            "PRINCIPAL_AMT": 12835511.27,
            "PRINCIPAL_PAY_DAY": 11,
            "INTEREST_PREPAID": 0,
            "NPL_DAYS": 1,
            "LAST_REPAYMENT_AMOUNT": 578829.23,
            "FEE_OUTSTANDING": 0,
            "VEXPRIREDATE": 0,
            "Down_payment": 30,
            "Down_payment_amount": 8370000,
            "LOAN_LENGTH": 1090
        }
        ,
        {
            "_id": 24,
            "CUSTOMER_TYPE": 2,
            "CRLIMIT": 15960000,
            "PRINCIPAL_AMT": 8162897.28,
            "PRINCIPAL_PAY_DAY": 11,
            "INTEREST_PREPAID": 0,
            "NPL_DAYS": 135,
            "LAST_REPAYMENT_AMOUNT": 453795.8,
            "FEE_OUTSTANDING": 138824.06,
            "VEXPRIREDATE": 0,
            "Down_payment": 30,
            "Down_payment_amount": 6840000,
            "LOAN_LENGTH": 1096
        }
    ]

    Return: 
        out: array [{id&score_user_1},{id&score_user_2},{id&score_user_2},...]
    Expected output:
    [
        {
            "_id": 23,
            "score": 367.66767998037136
        },
        {
            "_id": 24,
            "score": 647.4611431534739
        }
    ]
    '''
    
    out = []

    for ele in source:

        # take id of users
        users_out = {}
        id = ele['_id']
        users_out['_id'] = id
        ele = dict_mapping(ele)

        # caculate users' score
        score = []
        for ele_ in ele:
            score.append(ele[ele_])
            
        score = np.array(score)
        score[score == None] = 0
        score = credit_score(score)
        users_out["score"] = score
        # merge to an array
        out.append(users_out)
    return out
    

# previous version

# def score_users(input):

#     # sort user's data
#     id_ = input['_id']
#     input = dict_mapping(input)
#     input['_id'] = id_

#     # extract each user data from .json
#     ext = []
#     for ele in input:
#         ext_ = np.array(input[ele])
#         ext.append(ext_)
#     ext = np.array(ext)
#     ext = np.transpose(ext)
#     ext_ = ext[:,1:]

#     # take id of users
#     id = np.array(id_)

#     # caculate each user's score from their data
#     score = []
#     for idx,val in enumerate(ext_):
#         score_ = credit_score(ext_[idx,:])
#         score.append(score_)

#     # collab id and score

#     result = {}
#     result["id"] = id.tolist()
#     result["score"] = score

#     return result










