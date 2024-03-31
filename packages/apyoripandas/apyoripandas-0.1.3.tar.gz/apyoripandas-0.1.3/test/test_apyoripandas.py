from apyoripandas.apriori import Apriori
import pandas as pd

# Exemplo de teste
df_test = pd.read_csv('test\iris.csv')

r = Apriori(df_test, min_support=0.1, min_confidence=0.9, min_length=18)

values_expected = ["frozenset({'variety = Setosa', 'petal.width = 0.2'})",
"frozenset({'petal.width = 0.2'})",
"frozenset({'variety = Setosa'})",
"0.19333333333333333",
"1.0",
"3.0",]

test = dict(zip([repr(a) for a in r.values[0]], values_expected))

for k in test:
    print(k == test[k])

