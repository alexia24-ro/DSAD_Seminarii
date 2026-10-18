import pandas as pd

df_industria=pd.read_csv("IndustriaAlimentara.csv",index_col=0)
print(df_industria.head())

#1
#coloane_activitati = ['Carne', 'Peste', 'LegumeFructe', 'Uleiuri', 'Lactate', 'Morarit', 'Panificatie']
coloane_activitati=list(df_industria)[2:]
filtru_angajati=df_industria[coloane_activitati].sum(axis=1)>0
df_cerinta1=df_industria[filtru_angajati]
df_cerinta1.to_csv("data_out/Cerinta1.csv")

#2
total_angajati = df_industria[coloane_activitati].sum(axis=1)
df_cerinta2=df_industria[['Localitate']].copy()
df_procente=(df_industria[coloane_activitati].div(total_angajati,axis=0)*100).round(2)
print(df_procente)
df_cerinta2 = pd.concat([df_cerinta2, df_procente], axis=1)
df_cerinta2.to_csv("data_out/Cerinta2.csv")

#3
df_populatie=pd.read_csv("PopulatieLocalitati.csv",index_col=0)

industria_alim_loc=df_industria.merge(df_populatie,left_index=True,right_index=True)
print(industria_alim_loc)
print("------------------------")
industria_alim_jud=industria_alim_loc[coloane_activitati+["Populatie","Judet"]].groupby("Judet").sum()
print(industria_alim_jud)
#var1: cerinta3 = (industria_alim_jud[coloane_activitati].sum(axis=1) / industria_alim_jud["Populatie"])
cerinta3=industria_alim_jud.apply(func=lambda x:x[coloane_activitati].sum()/x["Populatie"],axis=1)
cerinta3.name="Pondere"
cerinta3=cerinta3.sort_values(ascending=False)
cerinta3.to_csv("data_out/Cerinta3.csv")


#4
cerinta4=industria_alim_jud[coloane_activitati].idxmax(axis=1)
cerinta4.name="Activitate_Dominanta"
cerinta4.to_csv("data_out/Cerinta4.csv")
print("--------------- 4 --------------")
print(cerinta4)

#5
def calcul_medie_ponderata(grup):
    return (grup[coloane_activitati]
            .multiply(grup["Populatie"],axis=0)
            .sum()/ grup["Populatie"].sum()
            )


df_judete=pd.read_csv("Coduri_Judete.csv",index_col=0)
print(df_judete.head())
industria_alim_loc_noua=industria_alim_loc[coloane_activitati+["Judet","Populatie"]].merge(df_judete["Regiune"],
                                                                                           left_on="Judet",right_index=True)
cerinta5=industria_alim_loc_noua[coloane_activitati+["Populatie","Regiune"]].groupby(by="Regiune").apply(calcul_medie_ponderata).round(3)
print("--------------- 5 --------------")
print(cerinta5)
cerinta5.to_csv("data_out/Cerinta5.csv")


#6
print(industria_alim_jud)
total_national=industria_alim_jud.sum(axis=0)
cerinta6=industria_alim_jud.apply(
    lambda x: (x[coloane_activitati]/total_national[coloane_activitati])
              /(x["Populatie"]/total_national["Populatie"]),axis=1

)
cerinta6.round(3).to_csv("data_out/Cerinta6.csv")