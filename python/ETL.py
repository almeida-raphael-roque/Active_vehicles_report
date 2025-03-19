# EXTRACT
import awswrangler as awr
import logging
import pandas as pd
import numpy as np
import datetime as dt
import traceback
import openpyxl
import shutil
import os


logging.basicConfig(
    level=logging.INFO,  # Exibe mensagens a partir de INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Garante logs no console
    ]
)


logging.info('\n ----------------------------------------------------------------------------------')
logging.info('\n Executando Rotina - RELATÓRIO DE PLACAS ATIVADAS')

class Extract:
    
    def extract_ativacoes():

        try:

            dir_query = r"C:\Users\raphael.almeida\Documents\Processos\ativacoes_placas\sql\placas_novas.sql"

            with open(dir_query, 'r') as file:
                query = file.read()

            df_ativ = awr.athena.read_sql_query(query,database='silver')
        
            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Relatorio ativacoes de placas novas  - Dados Extraidos com sucesso!')

            return df_ativ

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'\n Falha ao Extrair relatorio ativacoes (Viavante): {e}')


    def extract_renovacoes():

        try:

            dir_query = r"C:\Users\raphael.almeida\Documents\Processos\ativacoes_placas\sql\placas_renovadas.sql"

            with open(dir_query, 'r') as file:
                query = file.read()

            df_renov = awr.athena.read_sql_query(query, database='silver')
        
            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Relatorio renovacoes (Vivante)  - Dados Extraidos com sucesso!')

            return df_renov

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'\n Falha ao Extrair relatorio renovacoes (Viavante): {e}')


    def extract_cancelamentos():

        try:

            dir_query = r"C:\Users\raphael.almeida\Documents\Processos\ativacoes_placas\sql\placas_canceladas.sql"

            with open(dir_query, 'r') as file:
                query = file.read()

            df_cancel = awr.athena.read_sql_query(query, database='silver')
        
            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Relatorio renovacoes (Vivante)  - Dados Extraidos com sucesso!')

            return df_cancel

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'\n Falha ao Extrair relatorio renovacoes (Viavante): {e}')


    def extract_all_placas():

        try:

            dir_query = r"C:\Users\raphael.almeida\Documents\Processos\ativacoes_placas\sql\placas_total_ordem.sql"

            with open(dir_query, 'r') as file:
                query = file.read()

            df_all_placas = awr.athena.read_sql_query(query, database='silver')
        
            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Relatorio renovacoes(Stcoop)  - Dados Extraidos com sucesso!')

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Extracao de Dados concluido com sucesso!')

            return df_all_placas

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'\n Falha ao Extrair relatorio renovacoes (Stcoop): {e}')




print("extract ok")



#############################            TRANSFORM



class Transform:
        
    def transforming_df_final():

        try:

            df_ativ = Extract.extract_ativacoes()
            df_renov = Extract.extract_renovacoes()
            df_all_placas = Extract.extract_all_placas()
            


            # JUNTANDO OS DATAFRAMES
            if not df_renov.empty:
                df_renov['status'] = 'RENOVAÇÃO'
                df_final = pd.concat([df_ativ, df_renov])
            else:
                df_final = df_ativ
            

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha ao juntar os dataframes: {e}')

        try:

            # CRIANDO DATAFRAME FINAL

            # CRIANDO COLUNA DE MIGRAÇÃO (MIGRATION_FROM)
            df_final['migration_from'] = None


            # ATUALIZANDO MIGRAÇÕES DE PLACAS (SEGTRUCK & STCOOP ---> VIAVANTE)
            for idx, row in df_final.iterrows():
                
                df_filtred = df_all_placas[
                    (df_all_placas['placa'] == row['placa']) |
                    (df_all_placas['chassi'] == row['chassi'])
                ]

                if not df_filtred.empty and len(df_filtred['cooperativa'].values) > 1:

                    if df_filtred['cooperativa'].values[1] != row['cooperativa'] and row['status'] != 'CANCELADO':
                        df_final.at[idx, 'status'] = 'MIGRAÇÃO'

                        if df_filtred['cooperativa'].values[1] == 'Segtruck':
                            df_final.at[idx, 'migration_from'] = 'Segtruck'

                        elif df_filtred['cooperativa'].values[1] == 'Stcoop':
                            df_final.at[idx, 'migration_from'] = 'Stcoop'
                        else:
                            df_final.at[idx, 'migration_from'] = 'Viavante'
                else: 
                    df_final.at[idx, 'migration_from'] = 'NULL' 
     
            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f' Processo de atualização de status de placas migradas realizado com sucesso!')
        
        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha na atualização de status de placas migradas: {e}')
            logging.info(traceback.format_exc())


        try:

            # TRANSFORMANDO O STATUS 'ATIVO' EM 'NOVO'
            df_final.loc[df_final['status'] == 'ATIVO', 'status'] = 'NOVO'

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha ao unir os dataframes: {e}')
            logging.info(traceback.format_exc())


        try:
            df_final['id_conjunto'] = df_final['id_conjunto'].fillna(0)
            df_final['matricula'] = df_final['matricula'].fillna(0)
            df_final['conjunto'] = df_final['conjunto'].fillna(0)
            df_final['placa'] = df_final['placa'].fillna('SEM-PLACA')
            df_final['chassi'] = df_final['chassi'].fillna('NULL')
            df_final['status'] = df_final['status'].fillna('NULL')
            df_final['data_ativacao'] = df_final['data_ativacao'].fillna(pd.Timestamp('1900-01-01'))
            df_final['cooperativa'] = df_final['cooperativa'].fillna('NULL')
            df_final['migration_from'] = df_final['migration_from'].fillna('NULL')
            

            
            today = pd.Timestamp.today().normalize()

            # Converte a coluna 'data_ativacao' para datetime (caso ainda não esteja)
            df_final['data_ativacao'] = pd.to_datetime(df_final['data_ativacao'], format='%d/%m/%Y', errors='coerce')

            # Filtra os registros onde 'data_ativacao' é menor que today
            df_final = df_final[df_final['data_ativacao'] < today]

            # Converte 'data_ativacao' para apenas a data (removendo horário) de forma segura
            df_final['data_ativacao'] = df_final['data_ativacao'].dt.date


            
            # df_final = df_final.fillna('NULL')

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Transformacao de Dados concluido com sucesso!')

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha ao realizar tratamento de dados: {e}')
            logging.info(traceback.format_exc())

        return df_final
    

    def transforming_df_all_placas():

        try:
            today = pd.Timestamp.today()
            df_all_placas = Extract.extract_all_placas()
            df_all_placas['data_ativacao'] = pd.to_datetime(df_all_placas['data_ativacao'],format='%d/%m/%Y')
            df_placas_atual = df_all_placas.loc[df_all_placas.groupby('placa')['data_ativacao'].idxmax()] 
            df_placas_atual = df_placas_atual[pd.to_datetime(df_placas_atual['data_ativacao'])<today]
            df_placas_atual['data_ativacao']=df_placas_atual['data_ativacao'].dt.date

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Segundo Processo de Transformacao de Dados concluído com sucesso!')

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha ao realizar o segundo tratamento de dados: {e}')
            logging.info(traceback.format_exc())

        return df_placas_atual



#############################            LOAD



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

            #pode dar errado
            return df_final, df_placas_atual, df_canceladas

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Carregamento de Dados concluido com sucesso!')

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'\n Falha ao Carregar Relatorio Final: {e}')
            logging.info(traceback.format_exc())





if __name__ == '__main__':
    Load_relat_ativ_pend.load_files()







