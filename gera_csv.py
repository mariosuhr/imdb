import pandas as pd
import time

# Site com dados dos arquivos: https://developer.imdb.com/non-commercial-datasets/
# Marcar início da execução
inicio = time.time()

# Função para carregar arquivos
def carregar_tsv(caminho, colunas):
    df = pd.read_csv(caminho, sep='\t', usecols=colunas, dtype=str)
    return df

# Função para remover NaN e '\N' de múltiplas colunas
def remover_nulls(df, colunas):
    for coluna in colunas:
        df = df[df[coluna].notna() & (df[coluna] != '\\N')]
    return df

# 1. Carrega e filtra o básico
df_basics = carregar_tsv('title.basics.tsv', ['tconst','titleType', 'primaryTitle', 'originalTitle', 'startYear', 'runtimeMinutes', 'genres'])
df_ratings = carregar_tsv('title.ratings.tsv', ['tconst', 'averageRating', 'numVotes'])
df_basics = df_basics.merge(df_ratings, on='tconst', how='left')
df_basics = df_basics[df_basics['titleType'] == 'movie']
df_basics = df_basics[~df_basics['genres'].str.contains('short', na=False)]
df_basics = df_basics[df_basics['numVotes'].notna() & df_basics['numVotes'].str.isdigit()]
df_basics = df_basics[df_basics['numVotes'].astype(int) >= 5000]

#  Remove NaN e '\N' de startYear, runtimeMinutes, genres
df_basics = remover_nulls(df_basics, ['startYear', 'runtimeMinutes', 'genres'])

# 2. Carrega o crew (diretores e escritores)
df_crew = carregar_tsv('title.crew.tsv', ['tconst', 'directors', 'writers'])

# 3. Coleta os nconsts únicos usados
ids_diretores = df_crew['directors'].dropna().str.split(',').explode()
ids_writers = df_crew['writers'].dropna().str.split(',').explode()
ids_necessarios = pd.unique(pd.concat([ids_diretores, ids_writers]))

# 4. Carrega APENAS os nomes necessários
df_names = pd.read_csv('name.basics.tsv', sep='\t', usecols=['nconst', 'primaryName'], dtype=str)
df_names = df_names[df_names['nconst'].isin(ids_necessarios)]

# 5. Cria dicionário de lookup para substituição
dict_nomes = dict(zip(df_names['nconst'], df_names['primaryName']))

# 6. Função para converter IDs em nomes
def ids_para_nomes(campo):
    if pd.isna(campo) or campo == '\\N' or campo == '':
        return ''
    try:
        return ', '.join([dict_nomes.get(i, '') for i in str(campo).split(',') if i in dict_nomes])
    except Exception as e:
        return ''

# 7. Aplica as conversões
df_crew['directorsName'] = df_crew['directors'].apply(ids_para_nomes)
df_crew['writersName'] = df_crew['writers'].apply(ids_para_nomes)

# 8. Junta tudo
df_final = df_basics.merge(df_crew[['tconst', 'directorsName', 'writersName']], on='tconst', how='left')

# 9. Exporta
df_final.to_csv('imdb.csv', index=False)

print(f'Tempo de execução: {round(time.time() - inicio, 2)} segundos')
