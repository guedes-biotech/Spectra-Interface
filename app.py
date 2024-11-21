import matplotlib
import matplotlib.pyplot as plt
matplotlib.use('Qt5Agg')  # Usando o backend Qt5 para o matplotlib
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QDialog, QDialogButtonBox, QScrollArea, QCheckBox, QSizePolicy, QStackedWidget, QLineEdit, QComboBox
import mplcursors
import pandas as pd
import numpy as np
import main
import sys
import os

class ColumnSelectionDialog(QDialog):  # Janela da caixa de seleção de colunas
    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Columns')  # Título
        layout = QVBoxLayout(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)

        # Criando um widget para conter as caixas de seleção
        container_widget = QWidget(scroll_area)
        container_layout = QVBoxLayout(container_widget)

        self.checkboxes = []  # Lista de colunas

        # Adiciona caixas de seleção para cada coluna do DataFrame
        for col in df.columns:
            checkbox = QCheckBox(col)
            checkbox.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
            container_layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        # Botão para confirmar a seleção
        buttons = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
        layout.addWidget(buttons)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)

        scroll_area.setWidget(container_widget)  # Define o widget da área de rolagem
        layout.addWidget(scroll_area)  # Adiciona a área de rolagem ao layout principal

    def get_selected_columns(self):  # Coleta as colunas marcadas
        selected_columns = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        return selected_columns

class InicialScreen(QWidget): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.layout = QVBoxLayout(self)  # Layout principal da tela

        # Botão de seleção do arquivo
        self.file_selector = QPushButton("Selecione o arquivo .csv")
        self.file_label = QLabel("No file selected")  # Texto de arquivo selecionado

        # Layout horizontal para o seletor de arquivo
        fisrt_line_layout = QHBoxLayout()
        fisrt_line_layout.addWidget(self.file_selector)
        fisrt_line_layout.addWidget(self.file_label)
        self.file_selector.clicked.connect(self.get_csv)  # Conecta o botão à função get_csv
        self.layout.addLayout(fisrt_line_layout)  # Adiciona o layout horizontal à tela
        self.layout.addStretch(1)

        second_line_layout = QHBoxLayout()
        
        # Label de colunas selecionadas
        self.column_label = QLabel('Colunas que não contêm dados de espectroscopia:')
        self.column_label.setWordWrap(True)
        second_line_layout.addWidget(self.column_label)

        # Botão para selecionar colunas
        self.get_columns_button = QPushButton('Selecionar colunas')
        second_line_layout.addWidget(self.get_columns_button)
        self.get_columns_button.clicked.connect(self.show_column_selection_dialog)
        
        self.layout.addLayout(second_line_layout)
        self.layout.addStretch(1)
        
        # Botão para iniciar a análise
        self.start_analysis_button = QPushButton('Iniciar Análise')
        self.start_analysis_button.setFixedHeight(50)
        self.layout.addWidget(self.start_analysis_button)
        self.start_analysis_button.clicked.connect(self.go_to_second_window)

    def get_csv(self):
        # Abre o diálogo para selecionar o arquivo CSV
        self.file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '/', '(*.csv)')
        if self.file_path:
            # Exibe o nome do arquivo no label
            self.file_label.setText(os.path.basename(self.file_path))
            self.df_original = main.open_file(self.file_path)  # Carrega o arquivo CSV como DataFrame

    def show_column_selection_dialog(self):
        # Cria o diálogo de seleção de colunas
        if hasattr(self, 'df_original'):  # Checa se o arquivo foi selecionado ou não
            dialog = ColumnSelectionDialog(self.df_original, self)

            if dialog.exec_() == QDialog.Accepted:  # Usuário clicou em OK
                self.selected_columns = dialog.get_selected_columns()
                self.column_label.setText(f'Colunas que não contêm dados de espectroscopia: {str(self.selected_columns)[1:-1]}')

    def go_to_second_window(self):
        # Prepara os dados para a próxima tela e troca a tela
        if hasattr(self, 'df_original') and hasattr(self, 'selected_columns'):
            self.df_cleaned = self.df_original.drop(columns=self.selected_columns)  # Retira as colunas de texto
            self.df_cleaned = self.df_cleaned.apply(pd.to_numeric, errors='coerce') #Aplica float para todos os dados restantes
            self.df_cleaned = self.df_cleaned.dropna(how='any')
            self.indices_mantidos = self.df_cleaned.index #Indices que passaram pela limpeza
            self.parentWidget().setCurrentIndex(1)  # Troca para a segunda tela
        elif hasattr(self, 'df_original'):
            self.selected_columns = []
            self.df_cleaned = self.df_original
            self.df_cleaned = self.df_cleaned.apply(pd.to_numeric, errors='coerce') #Aplica float para todos os dados restantes
            self.df_cleaned = self.df_cleaned.dropna(how='any')
            self.indices_mantidos = self.df_cleaned.index #Indices que passaram pela limpeza
            self.parentWidget().setCurrentIndex(1)  # Troca para a segunda tela

class AnalysisWindow(QWidget): 
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Análise dos Dados')
        self.layout = QVBoxLayout(self)
        
        plot_spectra_layout = QHBoxLayout()
        
        # Label do plot do gráfico 
        self.plot_label = QLabel("Plot dos espectros:")
        plot_spectra_layout.addWidget(self.plot_label)
        
        self.input_plot_number = QLineEdit(self) #Caixa para inserir o número do plot desejado
        self.input_plot_number.setPlaceholderText('Digite um número ou uma lista de numéros espaçados por VÍRGULA(EX: 1, 32, 21, 10, 2, 40)')
        self.input_plot_number.setMinimumWidth(300)
        self.input_plot_number.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        plot_spectra_layout.addWidget(self.input_plot_number)
        
        self.plot_one_button = QPushButton('Plotar Espectro') #Botão para plotar 1 linha
        plot_spectra_layout.addWidget(self.plot_one_button)
        self.plot_one_button.clicked.connect(self.plot_one_spectrum)
        
        self.plot_all_button = QPushButton('Plotar Todos') #Botão para plotar todas as linhas
        plot_spectra_layout.addWidget(self.plot_all_button)
        self.plot_all_button.clicked.connect(self.plot_all_spectra)
        
        self.layout.addLayout(plot_spectra_layout)
        
        pca_layout = QHBoxLayout()
        
        # Label do plot do gráfico 
        self.label_PCA = QLabel("Análise de componente principal:")
        pca_layout.addWidget(self.label_PCA)
        
        self.input_pca_size = QLineEdit(self) #Caixa para inserir o número do componentes principais desejadas
        self.input_pca_size.setPlaceholderText(f"Digite o número de componentes principais")
        self.input_pca_size.setMinimumWidth(200)
        self.input_pca_size.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        pca_layout.addWidget(self.input_pca_size)
        
        self.generate_PCA = QPushButton('Calcular Componentes') #Botão para gerar as componentes
        self.generate_PCA.clicked.connect(self.PCA_generator)
        pca_layout.addWidget(self.generate_PCA)
        
        self.layout.addLayout(pca_layout)
        
        plot_pca_layout = QHBoxLayout()
        
        self.variancias = QLabel("Variância explicada pelos componentes principais:")
        plot_pca_layout.addWidget(self.variancias)
        
        self.pc_dropdown = QComboBox() #Caixa de seleção da componente principal
        plot_pca_layout.addWidget(self.pc_dropdown)
        
        self.second_dropdown = QComboBox()
        plot_pca_layout.addWidget(self.second_dropdown) #Segunda caixa para definir o segundo eixo do gráfico, caso tenha
        self.second_dropdown.addItem('Nenhum')
        
        self.plot_pca_button = QPushButton('Mostrar Perfil da Componente')
        plot_pca_layout.addWidget(self.plot_pca_button)
        self.plot_pca_button.clicked.connect(self.plot_pca)
        
        self.layout.addLayout(plot_pca_layout)
        
        final_line_layout = QHBoxLayout()
        
        self.final_label = QLabel('Opções para gerar os arquivos:')
        final_line_layout.addWidget(self.final_label)
        
        self.fourrier_box = QCheckBox('Transformada de Fourrier')
        final_line_layout.addWidget(self.fourrier_box)
        
        self.normalize_box = QCheckBox('Normalizar')
        final_line_layout.addWidget(self.normalize_box)
        
        self.end_button = QPushButton('Gerar arquivos e finalizar')
        final_line_layout.addWidget(self.end_button)
        self.end_button.clicked.connect(self.finish_app)
        
        self.layout.addLayout(final_line_layout)
        
    def showEvent(self, event):
        # Obtém os dados da primeira tela ao exibir a segunda tela
        parent_widget = self.parentWidget()  # Obtém o QStackedWidget
        inicial_screen = parent_widget.widget(0)  # Tela inicial é o índice 0
        
        self.df_cleaned = inicial_screen.df_cleaned  # Acessa o atributo df_cleaned
        self.indices_mantidos = inicial_screen.indices_mantidos #Acessa a lista de indices que permaneceram depois da limpeza
        self.df_original = inicial_screen.df_original
        self.selected_columns = inicial_screen.selected_columns #Pega as colunas selecionadas da primeria janela
        self.plot_label.setText(f"Plot dos espectros(1 a {self.df_cleaned.shape[0]}):")
        
    def plot_one_spectrum(self):
        if self.input_plot_number.text().isdigit():
            main.plot_IR(self.df_cleaned, int(self.input_plot_number.text()) - 1)
        elif ',' in self.input_plot_number.text():
            index_list = self.input_plot_number.text().split(', ')
            index_list = list(map(int, index_list)) # Convertendo os elementos da lista para inteiros
            index_list = [x - 1 for x in index_list]
            df_copy = self.df_cleaned.loc[index_list].copy()
            main.plot_all_spectra(df_copy, show_legend=True) 
        
    def plot_all_spectra(self):
        main.plot_all_spectra(self.df_cleaned)
        
    def PCA_generator(self):
        temp = main.get_PCA(self.df_cleaned, int(self.input_pca_size.text())) #Pega o df da PCA
        self.pca = temp[0]
        self.pca_df = temp[1]
        
        self.variancias.setText(f"Variância explicada pelos componentes principais: {self.pca.explained_variance_ratio_}") #Mostra na tela as variancias de cada PCA
        
        self.pc_dropdown.clear() #Limpa o primeiro dropdown
        self.pc_dropdown.addItems(self.pca_df.columns) # Adiciona as componentes principais como opção
        
        self.second_dropdown.clear()
        self.second_dropdown.addItems(self.pca_df.columns)
        
    def plot_pca(self):
        if self.second_dropdown.currentText() == 'Nenhum':
            cp_loadings = self.pca.components_[self.pc_dropdown.currentIndex()]  # A linha do loading de acordo com a coluna selecionada
            comprimentos_onda = self.df_cleaned.columns

            # Plotando o gráfico
            plt.figure(figsize=(12, 6))
            plt.plot(comprimentos_onda, cp_loadings, marker='o', color='b', markersize=3)
            plt.title(f'Perfil da Componente Principal - {self.pc_dropdown.currentText()}')
            plt.xlabel('Comprimento de Onda')  # Defina o nome do eixo X
            plt.ylabel('Contribuição (Loadings)')  # Defina o nome do eixo Y
            plt.xticks(ticks=comprimentos_onda[::50], rotation=90)
            plt.axhline(0, color='red', linestyle='--')  # Linha de referência
            plt.grid()
            plt.tight_layout()  # Ajusta o layout do gráfico
            plt.show(block=False)
        
        else: #Plota a correlação
            plt.figure(figsize=(12, 6))
            scatter_plot = plt.scatter(self.pca_df[self.pc_dropdown.currentText()], self.pca_df[self.second_dropdown.currentText()])
            plt.title(f'PCA - {self.pc_dropdown.currentText()} X {self.second_dropdown.currentText()}')
            plt.xlabel(f'{self.pc_dropdown.currentText()}')
            plt.ylabel(f'{self.pc_dropdown.currentText()}')
            plt.grid()

            # Criar o cursor para mostrar o índice dos pontos
            cursor = mplcursors.cursor(scatter_plot, hover=True)
            
            def on_add(sel):
                # Pega as coordenadas do ponto no gráfico
                x_val, y_val = sel.target
                
                # Compara os valores de x e y com o DataFrame para encontrar o índice correspondente
                idx = np.argmin(np.abs(self.pca_df[self.pc_dropdown.currentText()] - x_val) +
                                np.abs(self.pca_df[self.second_dropdown.currentText()] - y_val))
                
                # Atualiza o texto da anotação com o índice correto
                sel.annotation.set_text(f'Índice: {self.df_cleaned.index[idx] + 1}')
            
            cursor.connect("add", on_add)

            plt.show(block=False)
    
    def finish_app(self):
        self.df_cleaned.to_csv('train_raw.csv', index=False)
        
        if len(self.selected_columns) != 0:
            df_predict = self.df_original.loc[self.indices_mantidos, self.selected_columns].copy()
            df_predict.to_csv('train_predict.csv', index=False)
            
        if self.fourrier_box:
            df_fourrier = main.fourrier(self.df_cleaned)
            df_fourrier.to_csv('train_fourrier.csv', index=False)
            
        if self.normalize_box:
            df_normalized = main.normalize(self.df_cleaned)
            df_normalized.to_csv('train_normalized.csv', index=False)
            
        if hasattr(self, 'pca_df'):
            self.pca_df.to_csv('train_pca.csv', index=False)
            
        main_app.close()   
            
class MainApp(QStackedWidget):
    def __init__(self):
        super().__init__()
        self.inicial_screen = InicialScreen(self)
        self.second_screen = AnalysisWindow(self)

        self.addWidget(self.inicial_screen)  # Adiciona a tela inicial
        self.addWidget(self.second_screen)  # Adiciona a segunda tela

        self.setCurrentIndex(0)  # Define a tela inicial

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.resize(1200, 800)  # Define o tamanho da janela inicial
    main_app.show()  # Exibe a janela em modo normal
    sys.exit(app.exec_())
