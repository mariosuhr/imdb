# main.py

import pandas as pd
from lista import Watchlist


df = pd.read_csv('imdb.csv')

def menu():
    watchlist = Watchlist()

    while True:
        print("\n--- Watchlist ---")
        print("1-Adicionar filme ao fim da lista")
        print("2-Adicionar filme ao início da lista")
        print("3-Marcar um filme como assistido")
        print("4-Exibir watchlist")
        print("5-Recomendação inteligente:")
        print("6-Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == '1' or opcao == '2':
            filme = input("Digite o nome do filme: ")
            watchlist.adicionar_filme_por_titulo(df, filme, opcao) 

        elif opcao == '3':
            watchlist.exibir_watchlist()
            filme = input("Digite o número do filme que foi assistido:")
            watchlist.remover_posicao(filme)
            if filme:
                print(f"Filme marcado como assistido e removido da watchlist: {filme}")
            else:
                print("Nenhuma filme para concluir.")

        elif opcao == '4':
            watchlist.exibir_watchlist()
        
        elif opcao == '5':
            watchlist.recomendacao_inteligente()

        elif opcao == '6':
            print("Saindo do programa")
            break
        else:
            print("Opção inválida. Tente novamente.")


menu()


