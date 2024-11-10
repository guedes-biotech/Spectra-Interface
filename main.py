import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np

def open_file(file_name):
    df = pd.read_csv(file_name, low_memory=False) #Coleta os dados do csv
    #colunas_texto = ['y'] #Especifica quais são as colunas de texto dentro do csv
    #df = df.drop(columns=colunas_texto)# Retira as colunas de texto
    df = df.apply(pd.to_numeric, errors='coerce') #Aplica float para todos os dados restantes
    df = df.dropna()
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
    sns.lineplot(data=data_long, x='Comprimento de Onda', y='Absorbância', marker=None, color='b')  # Plota os valores como uma linha contínua, sem marcadores
    plt.xticks(ticks=data_long['Comprimento de Onda'][::50], rotation=90)  # Exibe o eixo x pulando de 50 em 50 colunas(apenas visual, os dados das colunas omitidas estão no gráfico) e com o texto rotacionado 90 graus
    plt.title(f'Espectro IR - Linha {linha_index}')  # Título do gráfico
    #plt.gca().axes.get_yaxis().set_visible(False)  # Oculte o eixo y
    plt.grid()  # Adiciona uma grade ao gráfico
    plt.tight_layout()  # Ajusta os elementos do gráfico para evitar colisão
    plt.show()  # Exibe o gráfico

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
    plt.figure(figsize=(8, 6))
    """
    plt.scatter(df_pca['PC1'], df_pca['PC2'])
    plt.title('PCA - Componentes Principais')
    plt.xlabel('Componente Principal 1')
    plt.ylabel('Componente Principal 2')
    plt.grid()
    plt.show()
    """
    explained_variance = pca.explained_variance_ratio_
    print("Variância explicada pelos componentes principais:", explained_variance)
     
#Fourrier
def fourrier(df):
    df_fft_real = pd.DataFrame(df.apply(lambda row: np.fft.fft(row).real, axis=1).tolist())
    return df_fft_real

def main():
    file_name = 'beer.csv'
    df = open_file(file_name, 0)
    #show_information(df)
    plot_IR(df, 1)
    #teste = fourrier(df)
    
    #get_PCA(df, 10)
    
#main()
    
