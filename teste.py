import main
import sys
import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import numpy as np
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow, QVBoxLayout, QLabel, QDesktopWidget, QFrame, QShortcut, QPushButton, QFileDialog, QHBoxLayout, QDialog, QCheckBox, QDialogButtonBox, QScrollArea, QSizePolicy

class ColumnSelectionDialog(QDialog): #Janela da caixa de seleção de colunas
    def __init__(self, df, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Select Columns') #Título
        layout = QVBoxLayout(self)
        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        
        # Criando um widget para conter as caixas de seleção
        container_widget = QWidget(scroll_area)
        container_layout = QVBoxLayout(container_widget)
        
        self.checkboxes = [] #Lista de colunas

        #Adiciona caixas de seleção para cada coluna do DataFrame
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
        
        scroll_area.setWidget(container_widget)# Define o widget da área de rolagem
        layout.addWidget(scroll_area) # Adiciona a área de rolagem ao layout principal
    
    def get_selected_columns(self): #Coleta as colunas marcadas
        selected_columns = [checkbox.text() for checkbox in self.checkboxes if checkbox.isChecked()]
        return selected_columns
    
class TestWindow(QMainWindow): 
    def __init__(self):
        super().__init__()
        self.setGeometry(0, 0, 1200, 800)# Define a geometria da janela
        self.setWindowTitle('Análise IR')

        # Cria um widget central e um layout para ele
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)
        self.layout = QVBoxLayout(central_widget)

        self.file_selector = QPushButton("Selecione o arquivo .csv") #botão de seleção do arquivo
        self.file_label = QLabel("No file selected") #texto de arquivo selecionado
        
        fisrt_line_layout = QHBoxLayout() #Layout horizontal
        fisrt_line_layout.addWidget(self.file_selector)
        fisrt_line_layout.addWidget(self.file_label)
        self.file_selector.clicked.connect(self.get_csv) # Conecta o botão a função get_csv
        self.layout.addLayout(fisrt_line_layout) #Adiciona o layout horizontal a tela
        
        self.column_label = QLabel('Colunas que não contém dados de espectroscopia:')
        self.column_label.setWordWrap(True)
        self.layout.addWidget(self.column_label)
        
        self.get_columns_button = QPushButton('Selecionar colunas')
        self.layout.addWidget(self.get_columns_button)
        self.get_columns_button.clicked.connect(self.show_column_selection_dialog)
        
        self.star_analysis_button = QPushButton('Iniciar Análise')
        self.layout.addWidget(self.star_analysis_button)
        self.star_analysis_button.clicked.connect(self.go_to_second_window)
        
        ### Variáveis ###
        
        
        
        
    def get_csv(self):
        self.file_path, _ = QFileDialog.getOpenFileName(self, 'Open File', '/', '(*.csv)')
        if self.file_path:
            # Exibe o nome do arquivo no label
            self.file_label.setText(os.path.basename(self.file_path))
            self.df_original = main.open_file(self.file_path)
    
    def show_column_selection_dialog(self):
        # Cria o diálogo de seleção de colunas
        if hasattr(self, 'df_original'): #Checa se df foi selecionado ou não
            dialog = ColumnSelectionDialog(self.df_original, self)
            
            if dialog.exec_() == QDialog.Accepted:
                self.selected_columns = dialog.get_selected_columns()
                self.column_label.setText(f'Colunas que não contém dados de espectroscopia: {str(self.selected_columns)[1:-1]}')
        
    def go_to_second_window(self):
        df = self.df_original.drop(columns=self.selected_columns)# Retira as colunas de texto
        self.clear_layout(self.layout)
    
    def clear_layout(self, layout):
    # Itera sobre todos os itens do layout
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)  # Obtém o item no índice i
            if item is not None:
                widget = item.widget()
                if widget:
                    widget.deleteLater()  # Remove o widget do layout e destrói da memória
                else:
                    # Se o item não for um widget (pode ser um item de layout), remover o layout também
                    sub_layout = item.layout()
                    if sub_layout:
                        self.clear_layout(sub_layout)  # Chama recursivamente para limpar layouts internos

    
app = QApplication(sys.argv)
window = TestWindow()
window.show()
sys.exit(app.exec_())