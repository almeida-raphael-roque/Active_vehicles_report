import pandas as pd
from transform import Transform
from extract import Extract


class Aggregate: 

    def aggregate_dataframe():
        
        df_ativadas = Transform.transforming_df_all_placas().drop_duplicates()
        df_movimentacao = Transform.transforming_df_final().drop_duplicates()
        df_canceladas = Extract.extract_cancelamentos().drop_duplicates()

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
        geral_hoje = len(df_ativadas[df_ativadas['status']=='ATIVO'])
        geral_segtruck = contar_placas(df_ativadas, 'ATIVO', 'Segtruck')
        geral_stcoop = contar_placas(df_ativadas, 'ATIVO', 'Stcoop')
        geral_viavante = contar_placas(df_ativadas, 'ATIVO', 'Viavante')


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

        print(tabela_df.head())

if __name__ == '__main__':
    Aggregate.aggregate_dataframe()

