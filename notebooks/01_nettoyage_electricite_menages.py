import pandas as pd

# --- Chargement du fichier source (renommé) ---
df = pd.read_csv('../data/raw/01_indicateurs_wdi_togo.csv', skiprows=[1])

# --- Nettoyage de base ---
df['Indicator Name'] = df['Indicator Name'].str.strip()
df = df.drop(columns=['Country Name', 'Country ISO3'])  # colonnes constantes (= Togo)
df = df.drop_duplicates()  # le fichier source contient ~22% de lignes dupliquées

print("Shape après nettoyage de base :", df.shape)

# --- 1. Filtrage des indicateurs "accès à l'électricité" ---
mapping_elec = {
    'Access to electricity (% of population)': 'acces_electricite_national_pct',
    'Access to electricity, rural (% of rural population)': 'acces_electricite_rural_pct',
    'Access to electricity, urban (% of urban population)': 'acces_electricite_urbain_pct',
    'Cost to get electricity connection (% of income per capita)': 'cout_connexion_pct_revenu',
    'Firms experiencing electrical outages (% of firms)': 'entreprises_touchees_coupures_pct',
    'Getting electricity (rank)': 'classement_facilite_electricite',
    'Procedures required to get electricity (number)': 'nb_procedures_connexion',
    'Time required to get electricity (days)': 'delai_connexion_jours',
    'Time to obtain an electrical connection (days)': 'delai_obtention_connexion_jours',
    'Value lost due to electrical outages (% of sales for affected firms)': 'pertes_coupures_pct_ventes',
}

df_elec = df[df['Indicator Name'].isin(mapping_elec)].copy()
df_elec['indicateur_fr'] = df_elec['Indicator Name'].map(mapping_elec)
df_elec = df_elec.rename(columns={'Year': 'annee', 'Value': 'valeur', 'Indicator Code': 'code_indicateur'})
df_elec = df_elec[['annee', 'indicateur_fr', 'valeur', 'code_indicateur']].sort_values(['indicateur_fr', 'annee'])

print("Shape accès électricité :", df_elec.shape)
print(df_elec.groupby('indicateur_fr').size())

# --- Export ---
df_elec.to_csv('../data/clean/01_acces_electricite.csv', index=False)
print("Fichier exporté : ../data/clean/01_acces_electricite.csv")


# --- 2. Filtrage des indicateurs "énergie des ménages / cuisson" ---
mapping_menage = {
    'Access to clean fuels and technologies for cooking (% of population)': 'acces_cuisson_propre_national_pct',
    'Access to clean fuels and technologies for cooking, rural (% of rural population)': 'acces_cuisson_propre_rural_pct',
    'Access to clean fuels and technologies for cooking, urban (% of urban population)': 'acces_cuisson_propre_urbain_pct',
    'Main cooking fuel: LPG/natural gas/biogas (% of households)': 'combustible_gaz_pct_menages',
    'Main cooking fuel: agricultural crop (% of households)': 'combustible_residus_agricoles_pct_menages',
    'Main cooking fuel: charcoal (% of households)': 'combustible_charbon_pct_menages',
    'Main cooking fuel: dung (% of households)': 'combustible_bouse_pct_menages',
    'Main cooking fuel: electricity  (% of households)': 'combustible_electricite_pct_menages',
    'Main cooking fuel: straw/shrubs/grass (% of households)': 'combustible_paille_pct_menages',
    'Main cooking fuel: wood (% of households)': 'combustible_bois_pct_menages',
}

df_menage = df[df['Indicator Name'].isin(mapping_menage)].copy()
df_menage['indicateur_fr'] = df_menage['Indicator Name'].map(mapping_menage)
df_menage = df_menage.rename(columns={'Year': 'annee', 'Value': 'valeur', 'Indicator Code': 'code_indicateur'})
df_menage = df_menage[['annee', 'indicateur_fr', 'valeur', 'code_indicateur']].sort_values(['indicateur_fr', 'annee'])

print("Shape énergie ménages :", df_menage.shape)
print(df_menage.groupby('indicateur_fr').size())

df_menage.to_csv('../data/clean/02_energie_menages_cuisson.csv', index=False)
print("Fichier exporté : ../data/clean/02_energie_menages_cuisson.csv")