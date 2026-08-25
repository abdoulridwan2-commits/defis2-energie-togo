import pandas as pd

df = pd.read_csv('../data/raw/03_temperatures_villes.csv')

# --- Découper la colonne Date (ex: "2013M1") en année + mois ---
df[['annee', 'mois']] = df['Date'].str.extract(r'(\d{4})M(\d{1,2})')
df['annee'] = df['annee'].astype(int)
df['mois'] = df['mois'].astype(int)

# --- Renommer les colonnes ---
mapping_type = {
    'Températures maximales': 'temp_max',
    'Températures minimales': 'temp_min',
}
df['type_temp'] = df['libellés'].map(mapping_type)
df = df.rename(columns={'villes': 'ville', 'Value': 'valeur_celsius', 'Unit': 'unite'})

df_final = df[['ville', 'annee', 'mois', 'type_temp', 'valeur_celsius', 'unite']]
df_final = df_final.sort_values(['ville', 'annee', 'mois', 'type_temp'])

print("Shape :", df_final.shape)
print(df_final.head(10))
print(df_final['ville'].unique())

df_final.to_csv('../data/clean/04_temperatures_villes.csv', index=False)
print("Fichier exporté : ../data/clean/04_temperatures_villes.csv")