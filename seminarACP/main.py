import pandas as pd
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA

# 1.
print('----------------- 1 -----------------')
tabel=pd.read_csv('Wholesale customers data.csv',sep=',')

print("dimensiune dataset: ",tabel.shape)
print("\nTipuri de date: \n",tabel.dtypes)
print("\nValori lipsa: ")
print(tabel.isnull().sum())
print(tabel.head())

coloane=['Fresh', "Milk", "Grocery", "Frozen", "Detergents_Paper", "Delicassen"]
x=tabel[coloane]

print(x)
#print("Statistici descriptive: ")
#print(x.describe())

# 2.
print('----------------- 2 -----------------')
scaler=StandardScaler()
date_standardizate= scaler.fit_transform(x)
print(date_standardizate)

# 3.
print('----------------- 3 -----------------')
matrice_corelatie = x.corr() # <=>  pd.DataFrame(date_standardizate, columns=coloane).corr()
sns.heatmap(matrice_corelatie, annot=True, cmap='coolwarm', fmt=".2f")
plt.show()

# 4.
print('----------------- 4 -----------------')
pca=PCA()
pca.fit(date_standardizate)

varianta_explicata = pca.explained_variance_ratio_
for i in range(len(varianta_explicata)):
    print(f"Componenta {i+1}: {varianta_explicata[i] * 100:.2f}%")

# 5.
import numpy as np

print('----------------- 5 -----------------')
suma_cumulata = np.cumsum(varianta_explicata)

for i in range(len(suma_cumulata)):
    if suma_cumulata[i] >= 0.80:
        print("Număr componente necesare:", i + 1)
        break
