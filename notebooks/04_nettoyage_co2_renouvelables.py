import pandas as pd

df_co2 = pd.read_csv('../data/raw/04_co2_secteur_electrique.csv')
df_ren = pd.read_csv('../data/raw/05_energies_renouvelables.csv')

# --- CO2 secteur électrique ---
df_co2_clean = df_co2[df_co2['value'].notna()].copy()
df_co2_clean = df_co2_clean.rename(columns={'date': 'annee', 'value': 'co2_secteur_electrique_MtCO2e'})
df_co2_clean = df_co2_clean[['annee', 'co2_secteur_electrique_MtCO2e']].sort_values('annee')

# --- Énergies renouvelables ---
df_ren_clean = df_ren[df_ren['value'].notna()].copy()
df_ren_clean = df_ren_clean.rename(columns={'date': 'annee', 'value': 'energies_renouvelables_pct'})
df_ren_clean = df_ren_clean[['annee', 'energies_renouvelables_pct']].sort_values('annee')

print("CO2 secteur électrique :", df_co2_clean.shape)
print("Énergies renouvelables :", df_ren_clean.shape)

df_co2_clean.to_csv('../data/clean/05_co2_secteur_electrique.csv', index=False)
df_ren_clean.to_csv('../data/clean/06_energies_renouvelables.csv', index=False)
print("Fichiers exportés.")