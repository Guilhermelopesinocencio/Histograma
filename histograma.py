import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Função para desenhar o histograma e a tabela
def desenhar_histograma_tabela(dados, frequencias):
    fi = frequencias
    fi_acumulada = np.cumsum(fi)

    total_respostas = sum(fi)
    # Frequência relativa com 2 casas decimais
    fr = [round(fi_acum / total_respostas, 2) for fi_acum in fi_acumulada]
    # Calcular FR em porcentagem
    fr_porcentagem = [round(f * 100, 2) for f in fr]
    # Calcular FR Acumulada
    fr_acumulada = np.cumsum(fr)
    # Arredondar FR Acumulada para cima, 1 casa decimal
    fr_acumulada = np.ceil(fr_acumulada * 100) / 100  # Arredondar para cima

    # Criar uma nova figura e adicionar subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

    largura_barra = 1.0
    intervalos_bordas = [int(intervalo.split('-')[0]) for intervalo in dados]
    intervalos_bordas.append(intervalos_bordas[-1] + 10)

    # Gráfico do histograma
    ax1.bar(intervalos_bordas[:-1], frequencias, width=10,
            align='edge', color='#4CAF50', edgecolor='black')

    ax1.set_xticks(intervalos_bordas)
    ax1.set_title("Histograma")
    ax1.set_xlabel("Intervalos")
    ax1.set_ylabel("Frequência")

    # Adicionar frequências acima das barras
    for i, freq in enumerate(frequencias):
        ax1.text(intervalos_bordas[i] + 5, freq,
                 str(freq), ha='center', va='bottom')

    # Tabela de frequências
    coluna_titulos = ['Intervalo', 'FI',
                      'FI Acumulada', 'FR', 'FR Acumulada', 'FR (%)']
    tabela_dados = [dados, fi, fi_acumulada, fr, fr_acumulada, fr_porcentagem]

    # Adiciona a tabela na segunda subplot
    ax2.axis('tight')
    ax2.axis('off')
    tabela = ax2.table(cellText=np.array(tabela_dados).T,
                       colLabels=coluna_titulos, cellLoc='center', loc='center')

    tabela.auto_set_column_width([0, 1, 2, 3, 4, 5])
    tabela.scale(1.0, 1.0)
    for (i, j), cell in tabela.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
        if i == 0:
            cell.set_text_props(weight='bold', fontsize=11)
        cell.set_text_props(horizontalalignment='center',
                            verticalalignment='center')

    pad = 20 + (len(dados) * 2)
    ax2.set_title("Tabela de Frequências", pad=pad)

    plt.tight_layout()
    plt.show()

# Função para processar os dados do usuário


def processar_dados():
    entrada = entry.get()
    if not entrada:
        messagebox.showerror("Erro", "Por favor, insira os números.")
        return

    try:
        valores = list(map(float, entrada.split(';')))
        min_valor = int(min(valores))
        max_valor = int(max(valores))

        if min_valor < 10:
            inicio_intervalo = 0
        else:
            inicio_intervalo = (min_valor // 10) * 10

        intervalos = []
        frequencias = []

        for i in range(inicio_intervalo, max_valor + 10, 10):
            intervalo = f"{i}-{i + 10}"
            if i == 10:
                count = sum(1 for v in valores if 10 <= v <
                            20)  # Contar apenas de 10 a 19
            else:
                count = sum(1 for v in valores if i <= v < i + 10)
            intervalos.append(intervalo)
            frequencias.append(count)

        desenhar_histograma_tabela(intervalos, frequencias)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira números válidos.")


# Criar a janela principal
janela = tk.Tk()
janela.title("Histograma de Números")

instrucoes = tk.Label(
    janela, text="Digite os números, separados por ponto e vírgula (exemplo: 1;2;2;3;4):")
instrucoes.pack(pady=10)

entry = tk.Entry(janela, width=50)
entry.pack(pady=10)

botao = tk.Button(janela, text="Gerar Histograma", command=processar_dados)
botao.pack(pady=20)

janela.mainloop()
