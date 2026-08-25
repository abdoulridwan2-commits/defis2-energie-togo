import pandas as pd

df = pd.read_csv('../data/raw/02_emissions_ges_secteur.csv')

# --- Corrections ---
df['type'] = df['type'].replace({'mnooxydes d’azote (N2O)': 'Protoxyde d’azote (N2O)'})

mapping_secteur = {
    'Total': 'total',
    'Energie': 'energie',
    'Procédés Industriels et Utilisation des Produits (PIUP)': 'procedes_industriels',
    'Agriculture, Foresterie et autres Affectations des Terres (AFAT)': 'agriculture_foresterie',
    'Déchets': 'dechets',
}
mapping_gaz = {
    'Total': 'total',
    'Dioxyde de carbone (CO2)': 'CO2',
    'Méthane(CH4)': 'CH4',
    'Protoxyde d’azote (N2O)': 'N2O',
}

df['secteur_code'] = df['secteur'].map(mapping_secteur)
df['gaz_code'] = df['type'].map(mapping_gaz)
df = df.rename(columns={'Date': 'annee', 'Value': 'valeur_Gg', 'Unit': 'unite'})
df_final = df[['annee', 'secteur_code', 'gaz_code', 'valeur_Gg', 'unite']]

print("Shape :", df_final.shape)
print(df_final)

df_final.to_csv('../data/clean/03_emissions_ges_secteur.csv', index=False)
print("Fichier exporté : ../data/clean/03_emissions_ges_secteur.csv")