import pandas as pd

df = pd.read_csv('imdb.csv')

# Buscar todos os filmes do Batman
hp_movies = df[df['originalTitle'].str.contains("the hobbit", case=False, na=False)]

# Mostrar apenas as colunas relevantes
print(hp_movies)
