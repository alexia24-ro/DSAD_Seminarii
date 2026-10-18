import pandas as pd
import numpy as np

df=pd.read_csv('data_out/winequality-red.csv', sep=';')

print("Dimensiune set de date: ")
print(df.shape)

print("Primele 5 randuri: ")
print(df.head())

print("Tipuri coloane: ")
print(df.dtypes)


from functii_online import nan_replace_df
df=nan_replace_df(df)
print("Mai există valori lipsă?", df.isnull().values.any())


import os
vinuri_bune= df[df["quality"]>=7]
os.makedirs("data_out",exist_ok=True)
vinuri_bune.to_csv("data_out/vinuri_calitate_min7.csv",sep=";",index=False)
print(vinuri_bune.head())
print("Numar de vinuri: ",len(vinuri_bune))


vinuri_sortate=df.sort_values(by="alcohol",ascending=False)
top50=vinuri_sortate.head(50)
top50.to_csv("data_out/top50_alcool.csv",sep=";",index=False)
print(top50[["alcohol"]])
print("nr vinuri: ",len(top50))

os.makedirs("data.out",exist_ok=True)
medii=df.groupby("quality")[["alcohol","pH"]].mean()
medii.to_csv("data_out/medii_pe_calitate.csv",sep=";")
print(medii)

df["aciditate_toatala"]=(df["fixed acidity"]+df["volatile acidity"]+df["citric acid"])
rezultatC6=df[["quality","alcohol","aciditate_toatala","pH"]]
rezultatC6.to_csv("data_out/vinuri_cu_aciditate.csv",sep=';',index=False)
print(rezultatC6.head())

medii=df.groupby("quality")["alcohol"].mean()
calitate_maxi=medii.idxmax()
rez=pd.DataFrame({"quality":[calitate_maxi]})
rez.to_csv("data_out/calitate_max_alcool.csv",sep=';',index=False)
print(rez)

coloane = ["fixed acidity","volatile acidity","citric acid","alcohol","quality"]
date=df[coloane]
R=date.corr()
R.to_csv("data_out//R.csv",sep=';',index=True)
print(R)

# utilizez deviatia standard a populatiei
media=df["alcohol"].mean()
deviatia_standard=df["alcohol"].std(ddof=0)
df["alcohol_std"]=(df["alcohol"]-media)/deviatia_standard
df[["alcohol","alcohol_std"]].to_csv("data_out/alcohol_standardizat.csv",sep=";",index=False)
print(df["alcohol_std"].mean())
print(df["alcohol_std"].std(ddof=0))



from scipy.spatial.distance import cdist
coloane=["fixed acidity","volatile acidity","alcohol"]
vinuriCerute=df[coloane].head(20).copy()

for col in coloane:
    med=vinuriCerute[col].mean()
    dev_std=vinuriCerute[col].std(ddof=0)
    vinuriCerute[col]=(vinuriCerute[col]-med)/dev_std

D=cdist(vinuriCerute,vinuriCerute,metric="euclidean")

#D=pd.DataFrame(D)
#D.to_csv("data_out/d_euclid_20.csv",sep=';',index=False,header=False)
#print(D.head(10))
etichete=list(range(1,21))
from functii_online import salvare_matrice
salvare_matrice(D,etichete,etichete,"data_out/d_euclid_20.csv")


