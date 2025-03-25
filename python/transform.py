import pandas as pd
import numpy as np
import datetime as dt
from extract import Extract
import logging
import traceback
import numpy as np

logging.basicConfig(
    level=logging.INFO,  # Exibe mensagens a partir de INFO
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler()  # Garante logs no console
    ]
)

df_ativ = Extract.extract_ativacoes()
df_renov = Extract.extract_renovacoes()
df_all_placas = Extract.extract_all_placas()
df_canceladas = Extract.extract_cancelamentos()

class Transform:
        
    def transforming_df_movimentacao():

        global df_movimentacao

        try:

            # JUNTANDO OS DATAFRAMES
            if not df_renov.empty:
                df_renov['status'] = 'RENOVAÇÃO'
                df_movimentacao = pd.concat([df_ativ, df_renov])
            else:
                df_movimentacao = df_ativ
            
        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha ao juntar os dataframes: {e}')

        try:

            # CRIANDO DATAFRAME FINAL

            # CRIANDO COLUNA DE MIGRAÇÃO (MIGRATION_FROM)
            df_movimentacao['migration_from'] = None


            # ATUALIZANDO MIGRAÇÕES DE PLACAS (SEGTRUCK & STCOOP ---> VIAVANTE)
            for idx, row in df_movimentacao.iterrows():
                
                df_filtred = df_all_placas[
                    (df_all_placas['placa'] == row['placa']) |
                    (df_all_placas['chassi'] == row['chassi'])
                ]

                if not df_filtred.empty and len(df_filtred['cooperativa'].values) > 1:

                    if df_filtred['cooperativa'].values[1] != row['cooperativa'] and row['status'] != 'CANCELADO':
                        df_movimentacao.at[idx, 'status'] = 'MIGRAÇÃO'

                        if df_filtred['cooperativa'].values[1] == 'Segtruck':
                            df_movimentacao.at[idx, 'migration_from'] = 'Segtruck'

                        elif df_filtred['cooperativa'].values[1] == 'Stcoop':
                            df_movimentacao.at[idx, 'migration_from'] = 'Stcoop'
                        else:
                            df_movimentacao.at[idx, 'migration_from'] = 'Viavante'
                else: 
                    df_movimentacao.at[idx, 'migration_from'] = 'NULL' 
     
            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f' Processo de atualização de status de placas migradas realizado com sucesso!')
        
        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha na atualização de status de placas migradas: {e}')
            logging.info(traceback.format_exc())


        try:

            # TRANSFORMANDO O STATUS 'ATIVO' EM 'NOVO'
            df_movimentacao.loc[df_movimentacao['status'] == 'ATIVO', 'status'] = 'NOVO'

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha ao unir os dataframes: {e}')
            logging.info(traceback.format_exc())


        try:
            df_movimentacao['id_conjunto'] = df_movimentacao['id_conjunto'].fillna(0)
            df_movimentacao['matricula'] = df_movimentacao['matricula'].fillna(0)
            df_movimentacao['conjunto'] = df_movimentacao['conjunto'].fillna(0)
            df_movimentacao['placa'] = df_movimentacao['placa'].fillna('SEM-PLACA')
            df_movimentacao['chassi'] = df_movimentacao['chassi'].fillna('NULL')
            df_movimentacao['status'] = df_movimentacao['status'].fillna('NULL')
            df_movimentacao['data_ativacao'] = df_movimentacao['data_ativacao'].fillna(pd.Timestamp('1900-01-01'))
            df_movimentacao['cooperativa'] = df_movimentacao['cooperativa'].fillna('NULL')
            df_movimentacao['migration_from'] = df_movimentacao['migration_from'].fillna('NULL')
            

            
            today = pd.Timestamp.today().normalize()

            # Converte a coluna 'data_ativacao' para datetime (caso ainda não esteja)
            df_movimentacao['data_ativacao'] = pd.to_datetime(df_movimentacao['data_ativacao'], format='%d/%m/%Y', errors='coerce')

            # Filtra os registros onde 'data_ativacao' é menor que today
            df_movimentacao = df_movimentacao[df_movimentacao['data_ativacao'] < today]

            # Converte 'data_ativacao' para apenas a data (removendo horário) de forma segura
            df_movimentacao['data_ativacao'] = df_movimentacao['data_ativacao'].dt.date


            
            # df_movimentacao = df_movimentacao.fillna('NULL')

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info('\n Processo de Transformacao de Dados 1 concluido com sucesso!')

        except Exception as e:

            logging.info('\n ----------------------------------------------------------------------------------')
            logging.info(f'Falha ao realizar tratamento de dados: {e}')
            logging.info(traceback.format_exc())

        return df_movimentacao
    

    def transforming_df_all_placas():

        global df_placas_atual
        
        try:
            today = pd.Timestamp.today()
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
    












        



