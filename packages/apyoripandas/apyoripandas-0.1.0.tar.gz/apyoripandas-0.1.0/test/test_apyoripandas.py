from apyoripandas.apriori import Apriori
import pandas as pd

# Exemplo de teste
data = {
    'Item1': [1, 1, 0, 1, 0],
    'Item2': [1, 0, 1, 1, 1],
    'Item3': [0, 1, 1, 0, 1]
}

r = Apriori((a := pd.DataFrame(data)), min_confidence=0.9)

a.to_clipboard()

print(r)