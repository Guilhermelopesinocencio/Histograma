import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np
import math

# Função para desenhar o histograma e a tabela


def desenhar_histograma_tabela(dados, frequencias, intervalo_calculado, nome_intervalos, nome_frequencia, casas_decimais, tipo_numero, titulo_usuario):
    fi = frequencias
    fi_acumulada = np.cumsum(fi)
    total_respostas = sum(fi)

    # Se for "Inteiros", usar 0 casas decimais na frequência relativa e nas porcentagens
    if tipo_numero == "Inteiros":
        casas_decimais = 0

    # Frequência relativa com número de casas decimais escolhidas
    fr = [round(fi_acum / total_respostas, casas_decimais)
          for fi_acum in fi_acumulada]

    # Calcular FR em porcentagem
    fr_porcentagem = [round(f * 100, 2) for f in fr]

    # Calcular FR Acumulada
    fr_acumulada = np.cumsum(fr)

    # Arredondar FR Acumulada para cima
    fr_acumulada = np.ceil(fr_acumulada * 100) / 100

    # Calcular FR% Acumulada
    fr_porcentagem_acumulada = np.cumsum(fr_porcentagem)

    # Criar uma nova figura e adicionar subplots
    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))

    # Usar o intervalo calculado para determinar as bordas
    largura_barra = intervalo_calculado
    intervalos_bordas = np.arange(min([float(intervalo.split('-')[0]) for intervalo in dados]),
                                  max([float(intervalo.split('-')[1])
                                      for intervalo in dados]) + largura_barra,
                                  largura_barra)

    # Gráfico do histograma
    ax1.bar(intervalos_bordas[:-1], frequencias, width=largura_barra,
            align='edge', color='#4CAF50', edgecolor='black')
    ax1.set_xticks(intervalos_bordas)
    ax1.set_title("Gráfico de Histograma")
    ax1.set_xlabel(nome_intervalos)
    ax1.set_ylabel(nome_frequencia)

    # Adicionar frequências acima das barras
    for i, freq in enumerate(frequencias):
        ax1.text(intervalos_bordas[i] + largura_barra / 2,
                 freq, str(freq), ha='center', va='bottom')

    # Tabela de frequências
    coluna_titulos = [nome_intervalos, 'FI', 'FI Acumulada',
                      'FR', 'FR Acumulada', 'FR (%)', 'FR% Acumulada']
    tabela_dados = [dados, fi, fi_acumulada, fr, fr_acumulada,
                    fr_porcentagem, fr_porcentagem_acumulada]

    # Adiciona a tabela na segunda subplot
    ax2.axis('tight')
    ax2.axis('off')
    tabela = ax2.table(cellText=np.array(tabela_dados).T,
                       colLabels=coluna_titulos, cellLoc='center', loc='center')

    # Título acima da tabela
    ax2.text(0.5, 1.2, f"Título: {
             titulo_usuario}", transform=ax2.transAxes, ha='center', va='center', fontsize=12)

    tabela.auto_set_column_width([0, 1, 2, 3, 4, 5, 6])
    tabela.scale(1.0, 1.0)
    for (i, j), cell in tabela.get_celld().items():
        cell.set_edgecolor('black')
        cell.set_linewidth(0.5)
        if i == 0:
            cell.set_text_props(weight='bold', fontsize=11)
        cell.set_text_props(horizontalalignment='center',
                            verticalalignment='center')

    # Adicionando a fonte na parte inferior direita da tabela
    ax2.text(1.0, -0.15, "Fonte: Eng. ll/ 2024",
             transform=ax2.transAxes, ha='right', va='center', fontsize=10)

    # Ajustar layout para título não sobrepor a tabela
    # Ajuste o retângulo para deixar mais espaço para o título
    plt.tight_layout(rect=[0, 0, 1, 0.85])
    plt.show()

# Função para processar os dados do usuário


def processar_dados():
    entrada = entry.get()
    nome_intervalos = entry_nome_intervalos.get()
    nome_frequencia = entry_nome_frequencia.get()
    titulo_usuario = entry_titulo.get()  # Receber o título inserido pelo usuário
    casas_decimais = int(casas_decimais_var.get())
    tipo_numero = tipo_numero_var.get()

    # Verificar se todos os campos foram preenchidos
    if not entrada or not nome_intervalos or not nome_frequencia or not titulo_usuario:
        messagebox.showerror("Erro", "Por favor, preencha todos os campos.")
        return

    try:
        # Converter valores para inteiros ou decimais dependendo da escolha do usuário
        if tipo_numero == "Inteiros":
            valores = list(
                map(lambda x: int(float(x.replace(",", "."))), entrada.split(';')))
        else:
            valores = list(
                map(lambda x: float(x.replace(",", ".")), entrada.split(';')))

        min_valor = min(valores)
        max_valor = max(valores)
        total_respostas = len(valores)

        # Calcular o intervalo (Maior número - Menor número) / sqrt(total FI)
        intervalo_calculado = (max_valor - min_valor) / \
            math.sqrt(total_respostas)

        # Arredondar o intervalo para o próximo número inteiro se for "Inteiros"
        if tipo_numero == "Inteiros":
            intervalo_calculado = math.ceil(intervalo_calculado)
        else:
            intervalo_calculado = round(intervalo_calculado, casas_decimais)

        # Definir os intervalos de acordo com o intervalo calculado
        intervalos = []
        frequencias = []

        intervalo_inicial = min_valor
        while intervalo_inicial < max_valor:
            intervalo_final = intervalo_inicial + intervalo_calculado
            if tipo_numero == "Inteiros":
                intervalo = f"{int(intervalo_inicial)}-{int(intervalo_final)}"
            else:
                intervalo = f"{intervalo_inicial:.{
                    casas_decimais}f}-{intervalo_final:.{casas_decimais}f}"
            count = sum(1 for v in valores if intervalo_inicial <=
                        v < intervalo_final)
            intervalos.append(intervalo)
            frequencias.append(count)
            intervalo_inicial = intervalo_final

        desenhar_histograma_tabela(intervalos, frequencias, intervalo_calculado,
                                   nome_intervalos, nome_frequencia, casas_decimais, tipo_numero, titulo_usuario)

    except ValueError:
        messagebox.showerror("Erro", "Por favor, insira números válidos.")

# Função para habilitar ou desabilitar as opções de casas decimais


def atualizar_casas_decimais():
    if tipo_numero_var.get() == "Inteiros":
        casas_decimais_1.config(state="disabled")
        casas_decimais_2.config(state="disabled")
        casas_decimais_3.config(state="disabled")
        casas_decimais_4.config(state="disabled")
    else:
        casas_decimais_1.config(state="normal")
        casas_decimais_2.config(state="normal")
        casas_decimais_3.config(state="normal")
        casas_decimais_4.config(state="normal")


# Criar a janela principal
janela = tk.Tk()
janela.title("Histograma de Números")

# Campo para "Nome para Frequência"
nome_frequencia_label = tk.Label(janela, text="Nome para Frequência:")
nome_frequencia_label.pack(pady=5)
entry_nome_frequencia = tk.Entry(janela, width=30)
entry_nome_frequencia.pack(pady=5)

# Campo para "Nome para Intervalos"
nome_intervalos_label = tk.Label(janela, text="Nome para Intervalos:")
nome_intervalos_label.pack(pady=5)
entry_nome_intervalos = tk.Entry(janela, width=30)
entry_nome_intervalos.pack(pady=5)

# Campo para "Título do Gráfico"
titulo_label = tk.Label(janela, text="Título:")
titulo_label.pack(pady=5)
entry_titulo = tk.Entry(janela, width=30)
entry_titulo.pack(pady=5)

# Campo para a entrada de dados
entrada_label = tk.Label(
    janela, text="Insira os dados separados por ponto e vírgula (Exemplo: 0,24; 0,48 ou 20; 45):")
entrada_label.pack(pady=5)
entry = tk.Entry(janela, width=30)
entry.pack(pady=5)

# Opções para o tipo de número
tipo_numero_var = tk.StringVar(value="Inteiros")
tipo_inteiros_radio = tk.Radiobutton(
    janela, text="Inteiros", variable=tipo_numero_var, value="Inteiros", command=atualizar_casas_decimais)
tipo_inteiros_radio.pack(pady=5)
tipo_decimais_radio = tk.Radiobutton(
    janela, text="Decimais", variable=tipo_numero_var, value="Decimais", command=atualizar_casas_decimais)
tipo_decimais_radio.pack(pady=5)

# Opções para casas decimais
casas_decimais_var = tk.StringVar(value="0")
casas_decimais_label = tk.Label(janela, text="Quantidade de Casas decimais:")
casas_decimais_label.pack(pady=5)

casas_decimais_1 = tk.Radiobutton(
    janela, text="1 casa decimal", variable=casas_decimais_var, value="1")
casas_decimais_1.pack(pady=5)
casas_decimais_2 = tk.Radiobutton(
    janela, text="2 casa decimal", variable=casas_decimais_var, value="2")
casas_decimais_2.pack(pady=5)
casas_decimais_3 = tk.Radiobutton(
    janela, text="3 casa decimal", variable=casas_decimais_var, value="3")
casas_decimais_3.pack(pady=5)
casas_decimais_4 = tk.Radiobutton(
    janela, text="4 casa decimal", variable=casas_decimais_var, value="4")
casas_decimais_4.pack(pady=5)

# Botão para processar os dados
botao_processar = tk.Button(
    janela, text="Processar Dados", command=processar_dados)
botao_processar.pack(pady=10)

# Iniciar o loop da interface
janela.mainloop()
