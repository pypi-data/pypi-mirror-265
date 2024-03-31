# Apyori for Pandas

Este pacote busca facilitar o uso da biblioteca apyori no pandas

veja um exemplo:

```python

from apyoripandas.apriori import Apriori
import pandas as pd

# Exemplo de teste
df_teste = pd.read_csv('teste.csv')

resultado = Apriori(df_test, min_support=0.1, min_confidence=0.9, min_length=18)

```

Neste caso resultado é um dataframe do pandas