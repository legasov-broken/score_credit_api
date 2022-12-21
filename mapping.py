from lib import *

source = open('./WOE_dict_sorted.json')
source = json.load(source)

def dict_mapping(value):
    '''
    Mapping input dictionay to the WOE dict
    
    Parameters: 
        source: dictionary
    Example: 
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

    Return:
        out_: dictionary
    '''
    out_ = {}

    for ele_in in source:
        out_[ele_in] = None
        for ele_out in value:
            if ele_in == ele_out:
                out_[ele_in] = value[ele_out] 
    return out_
