import pandas as pd
from ETL import Load_relat_ativ_pend

df_final, df_placas_atual, df_canceladas = Load_relat_ativ_pend.load_files()

df_final.head()