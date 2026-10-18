import numpy as np
import pandas as pd

def nan_replace_df(tabel):
    tabel=tabel.copy()

    for col in tabel.columns:
        if pd.api.types.is_numeric_dtype(tabel[col]):
            if tabel[col].isnull().any():
                media=tabel[col].mean()
                tabel[col]=tabel[col].fillna(media)

    return tabel


def salvare_matrice(x, index_linie, index_coloana, fisier):
    tabel=pd.DataFrame(x,index=index_linie,columns=index_coloana)
    tabel.to_csv(fisier,sep=';',index=True)