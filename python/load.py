import logging
import openpyxl
import shutil
import pandas as pd
import os
import traceback
from transform import Transform
from extract import Extract
import pyautogui
import time
import matplotlib.pyplot as plt
from pandas.plotting import table
import win32com.client as win32
import pythoncom

logging.basicConfig(
    level=logging.INFO,  # Exibe mensagens a partir de INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Garante logs no console
    ]
)

df_movimentacao = Transform.transforming_df_movimentacao() #vai rodar ativ e renov e df_all_placas
df_placas_atual= Transform.transforming_df_all_placas() #vai rodar df_all_placas
df_canceladas = Extract.extract_cancelamentos() # vai rodar cancel


class Load_relat_ativ_pend:

    def to_sharepoint():

        try:
            #criando os paths 1 e 2
            path1 = r"C:\Users\raphael.almeida\Documents\Processos\ativacoes_placas"
            path2 = r"C:\Users\raphael.almeida\Grupo Unus\analise de dados - Arquivos em excel"

            #criando os pathfiles
            file_path1 = os.path.join(path1, 'acompanhamento_placas.xlsx')
            file_path2 = os.path.join(path2, 'acompanhamento_placas.xlsx')

            #criando os wb
            with pd.ExcelWriter(file_path1, engine='openpyxl') as wb1:
                df_movimentacao.to_excel(wb1, index=False, sheet_name='Movimentações')
                df_placas_atual.to_excel(wb1, index=False, sheet_name='Ativadas')
                df_canceladas.to_excel(wb1, index=False, sheet_name='Canceladas')
            
            with pd.ExcelWriter(file_path2, engine='openpyxl') as wb2:
                df_movimentacao.to_excel(wb2, index=False, sheet_name='Movimentações')
                df_placas_atual.to_excel(wb2, index=False, sheet_name='Ativadas')
                df_canceladas.to_excel(wb2, index=False, sheet_name='Canceladas')

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Carregamento de Dados 1 concluido com sucesso!')

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'\n Falha ao Carregar Relatorio Final: {e}')
            logging.info(traceback.format_exc())

    def aggregate_dataframe():

        global tabela_df

        def contar_placas(df, status, cooperativa):
            return len(
                df[
                    (df['status'] == status) & 
                    (df['cooperativa'] == cooperativa)
                ]
            )

        lista_cooperativas = ['Segtruck', 'Stcoop', 'Viavante']
        lista_status = ['NOVO', 'RENOVAÇÃO', 'MIGRAÇÃO', 'CANCELADO']

        for nome_cooperativa in lista_cooperativas:
            for nome_status in lista_status:
                nome_variavel = f'{nome_status}_{nome_cooperativa}'

                if nome_status == 'CANCELADO':
                    globals()[nome_variavel] = contar_placas(df_canceladas, nome_status, nome_cooperativa)
                else:
                    globals()[nome_variavel] = contar_placas(df_movimentacao, nome_status, nome_cooperativa)


        #movimentações gerais --------------------------------------------------------------------------------
        geral_novas = globals()['NOVO_Viavante'] + globals()['NOVO_Stcoop'] + globals()['NOVO_Segtruck']
        geral_renovadas = globals()['RENOVAÇÃO_Viavante'] + globals()['RENOVAÇÃO_Stcoop'] + globals()['RENOVAÇÃO_Segtruck']
        geral_migracao = globals()['MIGRAÇÃO_Viavante'] + globals()['MIGRAÇÃO_Stcoop'] + globals()['MIGRAÇÃO_Segtruck']
        geral_canceladas = globals()['CANCELADO_Viavante'] + globals()['CANCELADO_Stcoop'] + globals()['CANCELADO_Segtruck']


        #placas gerais ---------------------------------------------------------------------------------------
        geral_hoje = len(df_placas_atual[df_placas_atual['status']=='ATIVO'])
        geral_segtruck = contar_placas(df_placas_atual, 'ATIVO', 'Segtruck')
        geral_stcoop = contar_placas(df_placas_atual, 'ATIVO', 'Stcoop')
        geral_viavante = contar_placas(df_placas_atual, 'ATIVO', 'Viavante')


        #tabela dataframe ------------------------------------------------------------------------------------
        índices = ['Novas', 'Renovadas', 'Migração', 'Canceladas', 'Total Empresa']
        tabela = {
            'Segtruck': [globals()['NOVO_Segtruck'], globals()['RENOVAÇÃO_Segtruck'], globals()['MIGRAÇÃO_Segtruck'], globals()['CANCELADO_Segtruck'], geral_segtruck],
            'Stcoop': [globals()['NOVO_Stcoop'], globals()['RENOVAÇÃO_Stcoop'], globals()['MIGRAÇÃO_Stcoop'], globals()['CANCELADO_Stcoop'], geral_stcoop],
            'Viavante': [globals()['NOVO_Viavante'], globals()['RENOVAÇÃO_Viavante'], globals()['MIGRAÇÃO_Viavante'], globals()['CANCELADO_Viavante'], geral_viavante],
            'Total': [geral_novas, geral_renovadas, geral_migracao, geral_canceladas, geral_hoje]
        }

        tabela_df = pd.DataFrame(tabela, index=índices)

        tabela_df = tabela_df.applymap(lambda x: f"{x:,.0f}".replace(',', '.') if isinstance(x, (int,float)) else x)

        logging.info('\n ----------------------------------------------------------------------------------')
        logging.info('\n Terceiro Processo de Transformacao de Dados concluído com sucesso!')

        return tabela_df

    def format_table():
            
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
            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Carregamento de Dados 2 concluido com sucesso!')
            # Fecha o gráfico
            plt.close()

            print(f"Tabela salva como {output_path}")
 
    def to_outlook():

        pythoncom.CoInitialize()

        # Garantir que a coluna de data está no formato correto
        df_placas_atual['data_ativacao'] = pd.to_datetime(df_placas_atual['data_ativacao'])

        # Pega a data mais recente da coluna
        analyzed_day = df_placas_atual['data_ativacao'].max().date().strftime('%d/%m/%Y')

        # Converte DataFrame para tabela HTML com índice
        tabela_html = tabela_df.to_html(classes='tabela', index=True)  # Agora inclui o índice

        # CSS embutido no HTML
        css_style = """
            <style>
                /* Estiliza o cabeçalho das colunas, o índice, a última coluna e a última linha */
                .tabela thead th, 
                .tabela tbody th, 
                .tabela td:last-child, 
                .tabela tbody tr:last-child td {
                    background-color: #f0f0f0; /* Cinza claro */
                    color: black; /* Fonte preta */
                    font-weight: bold; /* Negrito */
                    text-align: center; /* Centraliza os cabeçalhos e as células */
                    padding: 8px; /* Adiciona espaçamento interno */
                }

                /* Estiliza todas as outras células */
                .tabela td {
                    background-color: white; /* Fundo branco */
                    color: black; /* Fonte preta */
                    text-align: center; /* Centraliza os valores */
                    padding: 8px; /* Adiciona espaçamento interno */
                }

                /* Estiliza a célula do total geral (interseção da última linha e última coluna) */
                .tabela tbody tr:last-child td:last-child {
                    background-color: #404040; /* Cinza escuro */
                    color: white; /* Texto branco */
                    font-weight: bold;
                }

                /* Adiciona uma borda superior preta fina à última linha da tabela */
                .tabela tbody tr:last-child {
                    border-top: 1px solid black; /* Borda superior preta fina */
                }

                /* Adiciona bordas finas cinza entre as células */
                .tabela th, 
                .tabela td {
                    border: 1px solid #d9d9d9; /* Cinza claro */
                    border-collapse: collapse;
                }

                /* Garante espaçamento e formatação das células */
                .tabela {
                    border-spacing: 0;
                    border-collapse: collapse;
                }

                /* Formata os valores numéricos para terem duas casas decimais */
                .tabela td {
                    font-variant-numeric: tabular-nums;
                }
            </style>
        """

        # Criar o email no Outlook
        try:
            outlook = win32.Dispatch("Outlook.Application")
            email = outlook.CreateItem(0)
            email.To = "dados13@grupounus.com.br"
            email.Subject = f'[ACOMPANHAMENTO DIÁRIO DE PLACAS] - Relatório de placas ativadas do dia {analyzed_day}'
            email.HTMLBody = f"""
                <html>
                <head>
                    {css_style}  <!-- Inclui o CSS no e-mail -->
                </head>
                <body>
                    <p>Prezado(a),</p>
                    <p>A seguir, o resultado de placas ativas disposto em modelo tabular, por empresa:</p>

                    {tabela_html}  <!-- Insere a tabela formatada -->

                    <p>O total de placas do dia anterior foi de x, logo, com um <b>(acréscimo ou decréscimo)</b> de <b>y</b> placas ativas.</p> 

                    <p>Atenciosamente,</p>
                    <p>Equipe Análise de Dados - Grupo Unus</p>
                    <p><i>Este é um e-mail automático, por favor não responda</i></p>
                </body>
                </html>
            """

            email.Send()
            print("Email enviado com sucesso!")
            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Carregamento de Dados 3 concluido com sucesso!')

        except Exception as e:
            print(f"Erro ao enviar o e-mail: {e}")

    def to_whatsapp():   
            
            pyautogui.hotkey('win', 'e')
            time.sleep(1)
            pyautogui.hotkey('shift', 'tab')
            time.sleep(1)
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
            pyautogui.write('61981109691')  
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

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Carregamento de Dados 4 concluido com sucesso!')











