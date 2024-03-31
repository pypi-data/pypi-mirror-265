from apyori import apriori as ap
import pandas as pd

def Apriori(dataframe, min_support=0.1, min_confidence=0.9, min_lift=1, min_length=18):
    df = dataframe.copy()
    df = df.astype(str)
    for i in df.columns:
        df[i] = f'{i} = ' + df[i]
    data = df.values
    results = list(ap(data, 
                      min_support=min_support,
                      min_confidence=min_confidence, 
                      min_lift=min_lift, 
                      min_length=min_length))
    
    if not(results): return None
    
    df2 = pd.DataFrame(results)

    df2['items_base'] = df2.ordered_statistics.str[0].str[0]
    df2['items_add'] = df2.ordered_statistics.str[0].str[1]
    df2['confidence'] = df2.ordered_statistics.str[0].str[2]
    df2['lift'] = df2.ordered_statistics.str[0].str[3]

    df2.drop(columns=['ordered_statistics'], inplace=True)

    return df2[['items', 'items_base', 'items_add', 'support', 'confidence', 'lift']]