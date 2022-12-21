from lib import *


MAX_VAL = 99999999999999
MIN_VAL = -MAX_VAL

# -----------------------------------------------------------------------------------------------------


def _bin_table(df, colname, n_bins=10, qcut=None):
    '''
    Phân chia các nhóm bins và thống kê số lượng các quan sát, số lượng good và bad ở mỗi nhóm.

    Parameters:
        df: dataframe
        colname: name of column needs to seperate
        n_bins: bins of the column

    Returns:
        df_summary: bins  of input dataframe
        thres: threshold of a bin
    '''
    X = df[[colname, 'good_bad']]
    X = X.sort_values(colname)
    coltype = X[colname].dtype

    if coltype in ['float', 'int']:
        if qcut is None:
            try:
                bins, thres = pd.qcut(X[colname], q=n_bins, retbins=True)
                # Thay thế threshold đầu và cuối của thres
                thres[0] = MIN_VAL
                thres[-1] = MAX_VAL
                bins, thres = pd.cut(X[colname], bins=thres, retbins=True)
                X['bins'] = bins
            except:
                print('n_bins must be lower to bin interval is valid!')
        else:
            bins, thres = pd.cut(X[colname], bins=qcut, retbins=True)
            X['bins'] = bins
    elif coltype == 'object':
        X['bins'] = X[colname]

    df_GB = pd.pivot_table(X,
                           index=['bins'],
                           values=['good_bad'],
                           columns=['good_bad'],
                           aggfunc={
                               'good_bad': np.size
                           })

    df_Count = pd.pivot_table(X,
                              index=['bins'],
                              values=['good_bad'],
                              aggfunc={
                                  'good_bad': np.size
                              })

    if coltype in ['float', 'int']:
        df_Thres = pd.DataFrame({'Thres': thres[1:]}, index=df_GB.index)
    elif coltype == 'object':
        df_Thres = pd.DataFrame(index=df_GB.index)
        thres = None
    df_Count.columns = ['No_Obs']
    df_GB.columns = ['#BAD', '#GOOD']
    df_summary = df_Thres.join(df_Count).join(df_GB)
    return df_summary, thres

# -----------------------------------------------------------------------------------------------------


def calc_vif(X):
    '''
    (Optional)
    Unknow function by Le Tien Dat.
    '''
    # Calculating VIF
    vif = pd.DataFrame()
    vif["variables"] = X.columns
    vif["VIF"] = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

    return (vif)

# -----------------------------------------------------------------------------------------------------


def woe_categorical(df, cat_feature, good_bad_df):
    '''
    (Optional)
    Calculate woe of categorical features.
    Unknow function by Le Tien Dat.
    '''
    df = pd.concat([df[cat_feature], good_bad_df], axis=1)
    df = pd.concat([df.groupby(df.columns.values[0], as_index=False)[df.columns.values[1]].count(),
                    df.groupby(df.columns.values[0], as_index=False)[df.columns.values[1]].mean()], axis=1)
    df = df.iloc[:, [0, 1, 3]]
    df.columns = [df.columns.values[0], 'n_obs', 'prop_good']
    df['prop_n_obs'] = df['n_obs'] / df['n_obs'].sum()
    df['n_good'] = df['prop_good'] * df['n_obs']
    df['n_bad'] = (1 - df['prop_good']) * df['n_obs']
    df['prop_n_good'] = df['n_good'] / df['n_good'].sum()
    df['prop_n_bad'] = df['n_bad'] / df['n_bad'].sum()
    df['WoE'] = np.log(df['prop_n_good'] / df['prop_n_bad'])
    df = df.sort_values(['WoE'])
    df = df.reset_index(drop=True)
    df['diff_prop_good'] = df['prop_good'].diff().abs()
    df['diff_WoE'] = df['WoE'].diff().abs()
    df['IV'] = (df['prop_n_good'] - df['prop_n_bad']) * df['WoE']
    df['IV'] = df['IV'].sum()
    return df

# -----------------------------------------------------------------------------------------------------


def _WOE(data, colname, n_bins=None, min_obs=100, qcut=None):
    '''
    Caculate WOE for each bins and IV for each vars.
    
    Parameters:
        data: dataframe input
        colname: name of column needs to caculate

    Returns:
        df_summary: WOE
        IV: information value
        new_thres: new threshold
    '''
    # Thống kê bins và lấy ra thres hold ban đầu
    df_summary, thres = _bin_table(data, colname, n_bins=n_bins, qcut=qcut)
    # Thay thế giá trị 0 của #BAD trong df_summary bằng 1 để không bị lỗi chia cho 0
    df_summary['#BAD'] = df_summary['#BAD'].replace({0: 1})

    if qcut is not None:
        # Lọc bỏ threshold để tạo thành threshold mới mà thỏa mãn số lượng quan sát >= min_obs
        exclude_ind = np.where(df_summary['No_Obs'] <= min_obs)[0]
        if exclude_ind.shape[0] > 0:
            new_thres = np.delete(thres, exclude_ind)
            print('Auto combine {} bins into {} bins'.format(
                n_bins, new_thres.shape[0]-1))
            # Tính toán lại bảng summary
            df_summary, thres = _bin_table(data, colname, qcut=new_thres)

    new_thres = thres
    df_summary['GOOD/BAD'] = df_summary['#GOOD']/df_summary['#BAD']
    df_summary['%BAD'] = df_summary['#BAD']/df_summary['#BAD'].sum()
    df_summary['%GOOD'] = df_summary['#GOOD']/df_summary['#GOOD'].sum()
    df_summary['WOE'] = np.log(df_summary['%GOOD']/df_summary['%BAD'])
    df_summary['IV'] = (df_summary['%GOOD'] -
                        df_summary['%BAD'])*df_summary['WOE']
    df_summary['COLUMN'] = colname
    IV = df_summary['IV'].sum()
    print('Information Value of {} column: {}'.format(colname, IV))
    return df_summary, IV, new_thres

# -----------------------------------------------------------------------------------------------------

def _KM(y_pred, n_bins):
    '''
    (Optional)
    Kolmogorov-Smirnov testing: caculate the differential between good and bad follow threshold.
    
    Parameters:
        y_preds: y predictions
        n_bins: numbers of bins

    '''
    _, thresholds = pd.qcut(y_pred, q=n_bins, retbins=True)
    cmd_BAD = []
    cmd_GOOD = []
    BAD_id = set(np.where(y_test == 0)[0])
    GOOD_id = set(np.where(y_test == 1)[0])
    total_BAD = len(BAD_id)
    total_GOOD = len(GOOD_id)
    for thres in thresholds:
        pred_id = set(np.where(y_pred <= thres)[0])
        # Đếm % số lượng hồ sơ BAD có xác suất dự báo nhỏ hơn hoặc bằng thres
        per_BAD = len(pred_id.intersection(BAD_id))/total_BAD
        cmd_BAD.append(per_BAD)
        # Đếm % số lượng hồ sơ GOOD có xác suất dự báo nhỏ hơn hoặc bằng thres
        per_GOOD = len(pred_id.intersection(GOOD_id))/total_GOOD
        cmd_GOOD.append(per_GOOD)
    cmd_BAD = np.array(cmd_BAD)
    cmd_GOOD = np.array(cmd_GOOD)
    return cmd_BAD, cmd_GOOD, thresholds

# -----------------------------------------------------------------------------------------------------

def _CreditScore(beta, alpha, woe, n=12, odds=1/4, pdo=-50, thres_score=600):
    '''
    Caculate Credit score for each features.

    Parameters:
        beta, alpha: const numbers from features - caculated by model
        WOE: weight of evidence - caculated by _WOE function

    Returns:
        score: score of features
    '''
    factor = pdo/np.log(2)
    offset = thres_score - factor*np.log(odds)
    score = (beta*woe+alpha/n)*factor+offset/n
    return score

# -----------------------------------------------------------------------------------------------------

def _search_score(obs, col):
    feature = [str(inter) for inter in list(WOE_dict[col]['table'].index) if obs[col].values[0] in inter][0]
    score = df_WOE[(df_WOE['Columns'] == col) & (
        df_WOE['Features'] == feature)]['Scores'].values[0]
    return score


