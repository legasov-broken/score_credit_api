def _search_score(obs, col):

    score = df_WOE[(df_WOE['Columns'] == col) & (
        df_WOE['Features'] == feature)]['Scores'].values[0]
    return score
