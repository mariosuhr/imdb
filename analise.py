import pandas as pd
pd.options.display.float_format = '{:,.0f}'.format

colunas = ['tconst', 'titleType', 'primaryTitle', 'originalTitle', 'startYear','runtimeMinutes', 'genres', 'averageRating', 'numVotes','directorsName', 'writersName']

df = pd.read_csv('imdb.csv')


mediaVotosDiretores = df.groupby('directorsName')['numVotes'].mean().reset_index()
mediaVotosDiretores = mediaVotosDiretores.sort_values(by='numVotes', ascending=False)




print(mediaVotosDiretores.head(20))

