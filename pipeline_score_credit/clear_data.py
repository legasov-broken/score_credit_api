from lib import *



def clear_data(path):
    # convert to datetime format
    loan = pd.read_csv(path)
    loan['OPNDT'] =  pd.to_datetime(loan['OPNDT'], format='%d/%m/%Y')
    loan['END_OF_TENOR'] =  pd.to_datetime(loan['END_OF_TENOR'], format='%d/%m/%Y')
    loan['LOAN_LENGTH'] = (loan['END_OF_TENOR'] - loan['OPNDT']).dt.days

    # correlation matrix between vars
    corrMatrix = loan.corr()

    # drop useless columns
    loan.drop(['CLSDT', 'PHONE', 'ADDRESS', 'CREDIT_ACNO', 'Debit ACNO', 'DEALER_NAME', 'OPNDT', 'END_OF_TENOR'], axis=1, inplace=True)
    loan_c = loan.drop(['LAST_REPAYMENT_DATE'], axis=1)
    loan_c['LAST_REPAYMENT_AMOUNT'].fillna(value=loan_c['LAST_REPAYMENT_AMOUNT'].mean(), inplace=True)
    loan_c.drop(['CUSTOMERID'], axis=1, inplace =True)

    # create a new column based on the NPL_STATUS column that will be our target variable
    loan_c['good_bad'] = np.where(loan_c.loc[:, 'NPL_STATUS'].isin(['Bad Debt', 'Doubtful']), 0, 1)
    # Drop the original 'NPL_STATUS' column
    loan_c.drop(columns = ['NPL_STATUS'], inplace = True)
    corrMatrix = loan_c.corr()

    # regularization
    numerical_features = loan_c.select_dtypes(include='number')
    object_features = loan_c.select_dtypes(include='object')
    datetime_features = loan_c.select_dtypes(include='datetime')
    loan_c.drop(datetime_features.columns, axis=1, inplace=True)

    enc = OrdinalEncoder()
    loan_c[['CUSTOMER_TYPE', 'CATNAME', 'CRD_PURPOSE']]= enc.fit_transform(loan_c[['CUSTOMER_TYPE', 'CATNAME', 'CRD_PURPOSE']])
    loan_c.drop(['BRNAME', 'ASDATE',	'NRC_NO',	'MIN_DUEDT', 'CRD_CLASSIFICATION'], axis=1, inplace=True)
    loan_c.drop(['FIRSTDATE_OF_PRINCIPAL_PAYMENT', 'FIRSTDATE_OF_INTEREST_PAYMENT'], axis=1, inplace = True)

    columns = np.full((corrMatrix.shape[0],), True, dtype=bool)
    for i in range(corrMatrix.shape[0]):
        for j in range(i+1, corrMatrix.shape[0]):
            if corrMatrix.iloc[i,j] >= 0.9:
                if columns[j]:
                    columns[j] = False
    selected_columns = numerical_features.columns[columns]
    unselect = numerical_features.columns.difference(selected_columns)

    #drop mutilcorr
    loan_c.drop(unselect, axis=1, inplace = True)

    return loan_c