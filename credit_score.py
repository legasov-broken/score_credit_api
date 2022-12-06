from lib import *


source = open('./WOE_dict.json')
data = json.load(source)

def credit_score(cs):

    score = 0

# CUSTOMER_TYPE
    for i in data['CUSTOMER_TYPE']:
        a = np.array(data["CUSTOMER_TYPE"][i])
        if a[0] < cs[0] < a[1]:
            score = score+float(i)
            break

# CRLIMIT
    for i in data['CRLIMIT']:
        a = np.array(data["CRLIMIT"][i])
        if a[0] < cs[1] < a[1]:
            score = score+float(i)
            break

# PRINCIPAL_AMT
    for i in data['PRINCIPAL_AMT']:
        a = np.array(data["PRINCIPAL_AMT"][i])
        if a[0] < cs[2] < a[1]:
            score = score+float(i)
            break

# PRINCIPAL_PAY_DAY
    for i in data['PRINCIPAL_PAY_DAY']:
        a = np.array(data["PRINCIPAL_PAY_DAY"][i])
        if a[0] < cs[3] < a[1]:
            score = score+float(i)
            break

# INTEREST_PREPAID
    for i in data['INTEREST_PREPAID']:
        
        a = np.array(data["INTEREST_PREPAID"][i])
        if a[0] < cs[4] < a[1]:
            score = score+float(i)
            break

# NPL_DAYS
    for i in data['NPL_DAYS']:
        a = np.array(data["NPL_DAYS"][i])
        if a[0] < cs[5] < a[1]:
            score = score+float(i)
            break

# LAST_REPAYMENT_AMOUNT
    for i in data['LAST_REPAYMENT_AMOUNT']:
        a = np.array(data["LAST_REPAYMENT_AMOUNT"][i])
        if a[0] < cs[6] < a[1]:
            score = score+float(i)
            break

# FEE_OUTSTANDING
    for i in data['FEE_OUTSTANDING']:
        a = np.array(data["FEE_OUTSTANDING"][i])
        if a[0] < cs[7] < a[1]:
            score = score+float(i)
            break

# VEXPRIREDATE
    for i in data['VEXPRIREDATE']:
        a = np.array(data["VEXPRIREDATE"][i])
        if a[0] < cs[8] < a[1]:
            score = score+float(i)
            break

# Down_payment%
    for i in data['Down_payment%']:
        a = np.array(data["Down_payment%"][i])
        if a[0] < cs[9] < a[1]:
            score = score+float(i)
            break

# Down payment amount
    for i in data['Down payment amount']:
        a = np.array(data["Down payment amount"][i])
        if a[0] < cs[10] < a[1]:
            score = score+float(i)
            break

# LOAN_LENGTH
    for i in data['LOAN_LENGTH']:
        a = np.array(data["LOAN_LENGTH"][i])
        if a[0] < cs[11] < a[1]:
            score = score+float(i)
            break

    return score


