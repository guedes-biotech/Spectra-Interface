import matplotlib
matplotlib.use('Qt5Agg')  # Usando o backend Qt5 para o matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler, MinMaxScaler
import numpy as np

def open_file(file_name):
    df = pd.read_csv(file_name, low_memory=False) #Coleta os dados do csv
    return df
    
def show_information(df):
    print('-'*80)
    print("Informações gerais:")
    df.info() #Retorna a classe de variável do python, o numero de linhas, o número de colunas, a quantidade de colunas por tipo de variável(float, string, bool) e o tamanho da variável em memória do computador
    print('-'*80)

    #Print do total de valores NaN(not a number) dentro do dataframe
    total_nan = df.isna().sum().sum()
    print(f"Total de valores NaN após a conversão: {total_nan}")

def plot_IR(df, linha_index):
    #Plot do espectro
    valores = df.iloc[linha_index]  # Obtém os valores da linha
    data_long = pd.DataFrame({'Comprimento de Onda': valores.index, 'Absorbância': valores.values}) # Conversão das variáveis para facilitar a leitura pela biblioteca

    plt.figure(figsize=(12, 6))  # Tamanho da figura em polegadas
    sns.lineplot(data=data_long, x='Comprimento de Onda', y='Absorbância', legend=None, marker=None, color='b')  # Plota os valores como uma linha contínua, sem marcadores
    plt.xticks(ticks=data_long['Comprimento de Onda'][::50], rotation=90)  # Exibe o eixo x pulando de 50 em 50 colunas(apenas visual, os dados das colunas omitidas estão no gráfico) e com o texto rotacionado 90 graus
    plt.yticks(np.arange(0, df.max().max(), 0.2))
    plt.title(f'Espectro IR - Linha {linha_index + 1}')  # Título do gráfico
    #plt.gca().axes.get_yaxis().set_visible(False)  # Oculte o eixo y
    plt.grid()  # Adiciona uma grade ao gráfico
    plt.tight_layout()  # Ajusta os elementos do gráfico para evitar colisão
    plt.show(block=False)  # Exibe o gráfico
    
def plot_all_spectra(df, show_legend=False):
    # Plot do espectro
    plt.figure(figsize=(12, 6))  # Configuração do tamanho da figura
    for linha_index, valores in df.iterrows():  # Itera diretamente pelos índices e valores das linhas
        data_long = pd.DataFrame({
            'Comprimento de Onda': valores.index,
            'Absorbância': valores.values
        })  # Conversão para formato longo

        # Adiciona um gráfico para a linha atual
        label = f'Espectro {linha_index+1}'  # Definindo um label para cada linha
        sns.lineplot(data=data_long, x='Comprimento de Onda', y='Absorbância', marker=None, label=label if show_legend else None)

    plt.xticks(ticks=data_long['Comprimento de Onda'][::50], rotation=90)  # Ajusta o eixo x
    plt.yticks(np.arange(0, df.max().max(), 0.2))
    plt.title('Espectros IR - Todas as Linhas')  # Título geral do gráfico
    plt.grid()  # Adiciona grade
    
    # Se show_legend for True, exibe a legenda
    if show_legend:
        # Ajuste para que a legenda não seja cortada e fique fora do gráfico
        plt.legend(title="Linhas", bbox_to_anchor=(1.05, 1), loc='upper left', frameon=False)  # Legenda fora do gráfico e sem borda

    # Ajuste do layout para evitar corte de conteúdo
    plt.tight_layout()  # Ajuste do layout para que todos os elementos se ajustem corretamente
    
    plt.show(block=False)  # Exibe o gráfico

#PCA
def get_PCA(df, number_components):
    scaler = StandardScaler()
    df_scaled = scaler.fit_transform(df)  # Normaliza os dados
    pca = PCA(n_components=number_components) # Função que puxa a PCA dos dados
    components = pca.fit_transform(df_scaled) # 
    columns = [] #Nome das colunas 
    for k in range(1, number_components+1):
        columns.append(f'PC{k}') 
    df_pca = pd.DataFrame(data=components, columns=columns)
    return (pca, df_pca)

#Fourrier
def fourrier(df):
    df_fft_real = pd.DataFrame(df.apply(lambda row: np.fft.fft(row).real, axis=1).tolist())
    return df_fft_real

def normalize(df):
    # Cria o objeto MinMaxScaler
    scaler = MinMaxScaler()
    
    # Normaliza os dados numéricos do DataFrame
    df_normalizado = pd.DataFrame(scaler.fit_transform(df), columns=df.columns, index=df.index)
    
    return df_normalizado
