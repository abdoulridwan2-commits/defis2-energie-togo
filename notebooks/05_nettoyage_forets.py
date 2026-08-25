import pandas as pd
from shapely import wkt

df = pd.read_csv('../data/raw/06_zones_protegees_forets.csv')

# --- Calcul du centroïde (latitude/longitude) pour chaque zone ---
df['geom'] = df['geometry'].apply(wkt.loads)
df['longitude'] = df['geom'].apply(lambda g: g.centroid.x)
df['latitude'] = df['geom'].apply(lambda g: g.centroid.y)
df['superficie_deg2'] = df['geom'].apply(lambda g: g.area)  # approximation, pas en km²

# --- Renommage des colonnes ---
df = df.rename(columns={
    'region_nom_bdd': 'region',
    'prefecture_nom_bdd': 'prefecture',
    'commune_nom_bdd': 'commune',
    'canton_nom_bdd': 'canton',
    'nom_localite': 'localite',
    'etab_nom': 'nom_zone',
    'etab_creation_date': 'annee_creation',
})

df_final = df[['FID', 'nom_zone', 'region', 'prefecture', 'commune', 'canton',
               'localite', 'annee_creation', 'latitude', 'longitude', 'superficie_deg2', 'geometry']]

print("Shape :", df_final.shape)
print(df_final[['nom_zone', 'region', 'latitude', 'longitude']].head(10))

df_final.to_csv('../data/clean/07_zones_protegees_forets.csv', index=False)
print("Fichier exporté : ../data/clean/07_zones_protegees_forets.csv")