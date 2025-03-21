import logging
import openpyxl
import shutil
import pandas as pd
import os
import traceback
from transform import Transform
from extract import Extract


class Load_relat_ativ_pend:

    def load_files():

        try:
            #criando os paths 1 e 2
            path1 = r"C:\Users\raphael.almeida\Documents\Processos\ativacoes_placas"
            path2 = r"C:\Users\raphael.almeida\Grupo Unus\analise de dados - Arquivos em excel"

            #criando os pathfiles
            file_path1 = os.path.join(path1, 'acompanhamento_placas.xlsx')
            file_path2 = os.path.join(path2, 'acompanhamento_placas.xlsx')

            #importando os dataframes
            df_final = Transform.transforming_df_final()
            df_placas_atual= Transform.transforming_df_all_placas()
            df_canceladas = Extract.extract_cancelamentos()

            #criando os wb
            with pd.ExcelWriter(file_path1, engine='openpyxl') as wb1:
                df_final.to_excel(wb1, index=False, sheet_name='Movimentações')
                df_placas_atual.to_excel(wb1, index=False, sheet_name='Ativadas')
                df_canceladas.to_excel(wb1, index=False, sheet_name='Canceladas')
            
            with pd.ExcelWriter(file_path2, engine='openpyxl') as wb2:
                df_final.to_excel(wb2, index=False, sheet_name='Movimentações')
                df_placas_atual.to_excel(wb2, index=False, sheet_name='Ativadas')
                df_canceladas.to_excel(wb2, index=False, sheet_name='Canceladas')

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Carregamento de Dados concluido com sucesso!')

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'\n Falha ao Carregar Relatorio Final: {e}')
            logging.info(traceback.format_exc())












