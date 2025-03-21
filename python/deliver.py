import pandas as pd
import matplotlib.pyplot as plt
from pandas.plotting import table
import time
import pyautogui
from aggregate import Aggregate

class Deliver:

    def deliver_dataframe():
        
        tabela_df = Aggregate.aggregate_dataframe()

        

        # Cria a figura para o gráfico
        fig, ax = plt.subplots(figsize=(8, 4))  # Ajuste o tamanho conforme necessário

        # Remove os eixos
        ax.axis('off')

        # Cria a tabela no gráfico
        tbl = table(ax, tabela_df, loc='center', colWidths=[0.2]*len(tabela_df.columns))

        # Ajusta a fonte e o estilo da tabela
        tbl.auto_set_font_size(False)
        tbl.set_fontsize(12)
        tbl.scale(1.2, 1.5)  # Aumenta ligeiramente o espaçamento vertical

        # Formatação de células (estilo CSS implementado no Python)
        for key, cell in tbl.get_celld().items():
            cell.set_text_props(horizontalalignment='center', verticalalignment='center')  # Centraliza tudo
            
            if key[0] == 0:  # Cabeçalhos (primeira linha da tabela)
                cell.set_text_props(fontweight='bold', color='black')  # Ajusta o peso da fonte e cor
                cell.set_facecolor('#d9d9d9')  # Cor de fundo cinza para cabeçalho
            elif key[1] == len(tabela_df.columns) - 1:  # Última coluna
                cell.set_text_props(fontweight='bold', color='black')  # Ajusta o peso da fonte e cor
                cell.set_facecolor('#d9d9d9')  # Cor de fundo cinza para última coluna
            elif key[0] == 5:  # Última linha (índice 5, contando com cabeçalho)
                cell.set_text_props(fontweight='bold', color='black')  # Negrito para a sexta linha
                cell.set_facecolor('#d9d9d9')  # Cor de fundo cinza para a sexta linha
            if key == (5, len(tabela_df.columns) - 1):  # Última célula específica
                cell.set_text_props(fontweight='bold', color='white')  # Texto branco em negrito
                cell.set_facecolor('#4d4d4d')  # Fundo cinza escuro

        # Salva a imagem PNG
        output_path = "tabela_placas_ativas.png"
        plt.savefig(output_path, format='png', bbox_inches='tight', dpi=300)

        # Fecha o gráfico
        plt.close()

        print(f"Tabela salva como {output_path}")
    
        pyautogui.hotkey('win', 'e')

        pyautogui.hotkey('shift', 'tab')


        for _ in range(3):  
            pyautogui.press('down')
            

        pyautogui.press('enter')
        time.sleep(1)

        # Pasta documents
        pyautogui.hotkey('ctrl', 'e')

        pyautogui.hotkey('shift', 'tab')

        pyautogui.press('right')

        pyautogui.hotkey('shift', 'down')


        for _ in range(6):
            pyautogui.press('down')
            

        pyautogui.press('enter')
        time.sleep(1)

        # Pasta processos
        pyautogui.hotkey('ctrl', 'e')

        pyautogui.hotkey('shift', 'tab')

        for _ in range(2):
            pyautogui.press('right')
            
        pyautogui.hotkey('shift', 'down')

        pyautogui.press('enter')
        time.sleep(1)

        # Pasta ativacoes_placas
        pyautogui.hotkey('ctrl', 'e')

        pyautogui.hotkey('shift', 'tab')

        for _ in range(3):
            pyautogui.press('right')
            
        pyautogui.hotkey('shift', 'down')

        pyautogui.press('enter')
        time.sleep(1)

        # Pasta python
        pyautogui.hotkey('ctrl', 'e')
        time.sleep(1)
        pyautogui.write('tabela_placas_ativas.png')
        time.sleep(2)
        for _ in range(4):
            pyautogui.press('tab')
            

        time.sleep(1)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'c')
        time.sleep(1)


        #whatsapp
        pyautogui.press('win')
        time.sleep(1)
        pyautogui.write('whatsapp')
        time.sleep(1)
        pyautogui.press('enter')  
        time.sleep(4)
        pyautogui.write('raphael')  
        time.sleep(1)
        pyautogui.press('down')
        time.sleep(1)
        pyautogui.press('enter')
        time.sleep(1)
        pyautogui.hotkey('ctrl', 'v')
        time.sleep(1)
        for _ in range(4):
            pyautogui.press('tab')
        time.sleep(1)
        pyautogui.press('enter')

if __name__ == '__main__':
    Deliver.deliver_dataframe()