import pandas as pd

class Filme:
    def __init__(self, titulo, duracao, generos, notaMedia, diretor):
        self.titulo = titulo
        self.duracao = duracao
        self.generos = generos
        self.notaMedia = notaMedia
        self.diretor = diretor
        self.proximo = None

class Watchlist:
    def __init__(self):
        self.cabeca = None
        self.cauda = None
    
    def esta_vazia(self):
        return self.cabeca is None
    
    def adicionar(self, titulo, duracao, generos, notaMedia, diretor):
        novo_filme = Filme(titulo, duracao, generos, notaMedia, diretor)
        if self.esta_vazia():
            self.cabeca = novo_filme
            self.cauda = novo_filme  # Atualiza a cauda quando o primeiro nó é adicionado
        else:
            self.cauda.proximo = novo_filme  # Atualiza o próximo da cauda
            self.cauda = novo_filme  # Atualiza a cauda para o novo nó

    def adicionar_inicio(self, titulo, duracao, generos, notaMedia, diretor):
        novo_filme = Filme(titulo, duracao, generos, notaMedia, diretor)
        if self.esta_vazia():
            self.cabeca = novo_filme
            self.cauda = novo_filme
        else:
            novo_filme.proximo = self.cabeca
            self.cabeca = novo_filme            
    

    def remover_posicao(self, posicao):
        if self.esta_vazia():
            print('A lista está vazia.')
            return

        if posicao == 0:
            self.remover_primeiro()
            return

        atual = self.cabeca
        anterior = None
        contador = 0

        while atual is not None and contador < int(posicao):
            anterior = atual
            atual = atual.proximo
            contador += 1

        if atual is not None:
            anterior.proximo = atual.proximo
            if anterior.proximo is None:
                self.cauda = anterior  # Atualiza a cauda se o último nó foi removido
            print(f'Filme {atual.titulo} na posição {posicao} removido.')
        else:
            print(f'Posição {posicao} fora do intervalo.')

    #Ajustar a busca
    def buscar(self, titulo):
        atual = self.cabeca
        while atual is not None:
            if atual.titulo == titulo:
                return True
            atual = atual.proximo
        return False

    def tamanho(self):
        contador = 0
        atual = self.cabeca
        while atual is not None:
            contador += 1
            atual = atual.proximo
        return contador

    def buscar_posicao(self, posicao):
        atual = self.cabeca
        contador = 0

        while atual is not None and contador < posicao:
            atual = atual.proximo
            contador += 1

        if atual is not None:
            print(f'Filme na posição {posicao}: {atual.titulo}')
        else:
            print(f'Posição {posicao} fora do intervalo.')

    def exibir_watchlist(self):
        if self.esta_vazia():
            print('A lista está vazia.')
        else:
            atual = self.cabeca
            while atual:
                print(atual.titulo, end=', ')
                atual = atual.proximo
            

  
    def adicionar_filme_por_titulo(self, df, titulo, opcao):
        resultado = df[df['primaryTitle'].str.lower() == titulo.lower()]

        if resultado.empty:
            print(f"Filme '{titulo}' não encontrado no DataFrame.")
            return

        row = resultado.iloc[0]
        titulo, duracao, generos, notaMedia, diretor = extrair_dados_filme(row)
        if opcao == 1:
            self.adicionar(titulo, duracao, generos, notaMedia, diretor)
        else:
            self.adicionar_inicio(titulo, duracao, generos, notaMedia, diretor)

        print(f"Filme '{titulo}' adicionado à Watchlist com sucesso!")

def extrair_dados_filme(row):

    titulo = row['primaryTitle'] if pd.notnull(row.get('primaryTitle')) else 'Título Desconhecido'        
    duracao = int(row.get('runtimeMinutes'))
    generos = row.get('genres')
    generos = generos.split(',') if pd.notnull(generos) else []
    notaMedia = float(row.get('averageRating')) 
    diretor = row.get('directorsName')
    diretor = diretor if pd.notnull(diretor) else 'Desconhecido'

    return titulo, duracao, generos, notaMedia, diretor


        


