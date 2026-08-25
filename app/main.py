import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(
    page_title="Défi 2 — Énergie & Transition écologique au Togo",
    layout="wide"
)

st.title("🇹🇬 Énergie & Transition écologique au Togo")
st.markdown("Accès à l'électricité, énergies propres et protection des forêts")

# --- Chargement des données ---
@st.cache_data
def load_data():
    df_elec = pd.read_csv('data/clean/01_acces_electricite.csv')
    df_menage = pd.read_csv('data/clean/02_energie_menages_cuisson.csv')
    df_emissions = pd.read_csv('data/clean/03_emissions_ges_secteur.csv')
    df_temp = pd.read_csv('data/clean/04_temperatures_villes.csv')
    df_co2 = pd.read_csv('data/clean/05_co2_secteur_electrique.csv')
    df_ren = pd.read_csv('data/clean/06_energies_renouvelables.csv')
    df_forets = pd.read_csv('data/clean/07_zones_protegees_forets.csv')
    return df_elec, df_menage, df_emissions, df_temp, df_co2, df_ren, df_forets

df_elec, df_menage, df_emissions, df_temp, df_co2, df_ren, df_forets = load_data()

st.success("Données chargées avec succès ✅")
st.write(f"Accès électricité : {df_elec.shape[0]} lignes")
st.write(f"Énergie ménages : {df_menage.shape[0]} lignes")
st.write(f"Émissions GES : {df_emissions.shape[0]} lignes")
st.write(f"Températures : {df_temp.shape[0]} lignes")
st.write(f"CO2 secteur électrique : {df_co2.shape[0]} lignes")
st.write(f"Énergies renouvelables : {df_ren.shape[0]} lignes")
st.write(f"Zones protégées : {df_forets.shape[0]} lignes")

st.divider()
st.header("1. Accès à l'électricité")

# --- Graphique : évolution national/rural/urbain ---
indicateurs_evolution = ['acces_electricite_national_pct', 'acces_electricite_rural_pct', 'acces_electricite_urbain_pct']
df_plot = df_elec[df_elec['indicateur_fr'].isin(indicateurs_evolution)]

labels = {
    'acces_electricite_national_pct': 'National',
    'acces_electricite_rural_pct': 'Rural',
    'acces_electricite_urbain_pct': 'Urbain',
}
df_plot = df_plot.copy()
df_plot['zone'] = df_plot['indicateur_fr'].map(labels)

fig1 = px.line(
    df_plot, x='annee', y='valeur', color='zone',
    title="Évolution de l'accès à l'électricité (1998-2022)",
    labels={'annee': 'Année', 'valeur': "Accès à l'électricité (%)", 'zone': 'Zone'}
)
st.plotly_chart(fig1, use_container_width=True, key="fig1_acces_electricite")

# --- Indicateurs clés (dernières valeurs disponibles) ---
col1, col2, col3 = st.columns(3)
for col, code, label in zip([col1, col2, col3], indicateurs_evolution, ['National', 'Rural', 'Urbain']):
    sub = df_elec[df_elec['indicateur_fr'] == code].sort_values('annee')
    derniere_valeur = sub.iloc[-1]
    col.metric(label, f"{derniere_valeur['valeur']:.1f}%", help=f"Année {int(derniere_valeur['annee'])}")

st.divider()
st.header("2. Consommation d'énergie des ménages")

# --- Graphique 1 : accès à la cuisson propre (national/rural/urbain) ---
indicateurs_cuisson = ['acces_cuisson_propre_national_pct', 'acces_cuisson_propre_rural_pct', 'acces_cuisson_propre_urbain_pct']
df_cuisson = df_menage[df_menage['indicateur_fr'].isin(indicateurs_cuisson)].copy()

labels_cuisson = {
    'acces_cuisson_propre_national_pct': 'National',
    'acces_cuisson_propre_rural_pct': 'Rural',
    'acces_cuisson_propre_urbain_pct': 'Urbain',
}
df_cuisson['zone'] = df_cuisson['indicateur_fr'].map(labels_cuisson)

fig2 = px.line(
    df_cuisson, x='annee', y='valeur', color='zone',
    title="Évolution de l'accès à la cuisson propre (2000-2022)",
    labels={'annee': 'Année', 'valeur': 'Accès cuisson propre (%)', 'zone': 'Zone'}
)
st.plotly_chart(fig2, use_container_width=True, key="fig2_acces_cuisson")

# --- Graphique 2 : répartition des combustibles de cuisson (dernière année dispo) ---
combustibles = {
    'combustible_bois_pct_menages': 'Bois',
    'combustible_charbon_pct_menages': 'Charbon',
    'combustible_gaz_pct_menages': 'Gaz/LPG',
    'combustible_electricite_pct_menages': 'Électricité',
    'combustible_residus_agricoles_pct_menages': 'Résidus agricoles',
    'combustible_paille_pct_menages': 'Paille/brousse',
    'combustible_bouse_pct_menages': 'Bouse',
}
df_combustibles = df_menage[df_menage['indicateur_fr'].isin(combustibles.keys())].copy()
df_combustibles['combustible'] = df_combustibles['indicateur_fr'].map(combustibles)
derniere_annee_combustible = df_combustibles['annee'].max()
df_combustibles_last = df_combustibles[df_combustibles['annee'] == derniere_annee_combustible]

fig3 = px.pie(
    df_combustibles_last, values='valeur', names='combustible',
    title=f"Répartition du combustible principal de cuisson ({int(derniere_annee_combustible)})"
)
st.plotly_chart(fig3, use_container_width=True, key="fig3_combustibles")



st.divider()
st.header("3. Bilan des émissions polluantes (2018)")

col1, col2 = st.columns(2)

with col1:
    # --- Graphique 1 : émissions totales par secteur ---
    df_secteur = df_emissions[(df_emissions['gaz_code'] == 'total') & (df_emissions['secteur_code'] != 'total')]
    labels_secteur = {
        'energie': 'Énergie',
        'procedes_industriels': 'Procédés industriels',
        'agriculture_foresterie': 'Agriculture & Foresterie',
        'dechets': 'Déchets',
    }
    df_secteur = df_secteur.copy()
    df_secteur['secteur'] = df_secteur['secteur_code'].map(labels_secteur)

    fig4 = px.bar(
        df_secteur.sort_values('valeur_Gg', ascending=True),
        x='valeur_Gg', y='secteur', orientation='h',
        title="Émissions de GES par secteur (Gg)",
        labels={'valeur_Gg': 'Émissions (Gg CO2eq)', 'secteur': 'Secteur'}
    )
    st.plotly_chart(fig4, use_container_width=True, key="fig4_emissions_secteur")

with col2:
    # --- Graphique 2 : répartition par type de gaz (secteur Énergie uniquement) ---
    df_gaz_energie = df_emissions[(df_emissions['secteur_code'] == 'energie') & (df_emissions['gaz_code'] != 'total')]
    labels_gaz = {'CO2': 'CO2', 'CH4': 'Méthane (CH4)', 'N2O': 'Protoxyde d\'azote (N2O)'}
    df_gaz_energie = df_gaz_energie.copy()
    df_gaz_energie['gaz'] = df_gaz_energie['gaz_code'].map(labels_gaz)

    fig5 = px.pie(
        df_gaz_energie, values='valeur_Gg', names='gaz',
        title="Répartition des gaz — Secteur Énergie"
    )
    st.plotly_chart(fig5, use_container_width=True,  key="fig5_gaz_energie")

# --- Graphique 3 : évolution du CO2 secteur électrique ---
fig6 = px.line(
    df_co2, x='annee', y='co2_secteur_electrique_MtCO2e',
    title="Évolution des émissions CO2 du secteur électrique (1970-2022)",
    labels={'annee': 'Année', 'co2_secteur_electrique_MtCO2e': 'Émissions CO2 (Mt CO2e)'}
)
st.plotly_chart(fig6, use_container_width=True, key="fig6_co2_electrique")


st.divider()
st.header("4. Variations climatiques (Sud → Nord)")

# --- Ordre géographique Sud -> Nord ---
ordre_villes = ['Lomé', 'Tabligbo', 'Kouma konda', 'Atakpamé', 'Sotouboua',
                 'Sokodé', 'Kara', 'Niamtougou', 'Mango', 'Dapaong']

# --- Sélecteur de ville ---
ville_choisie = st.selectbox("Choisir une ville", ordre_villes)

df_ville = df_temp[df_temp['ville'] == ville_choisie].copy()
df_ville['date'] = pd.to_datetime(df_ville['annee'].astype(str) + '-' + df_ville['mois'].astype(str) + '-01')

fig7 = px.line(
    df_ville, x='date', y='valeur_celsius', color='type_temp',
    title=f"Évolution des températures — {ville_choisie} (2013-2019)",
    labels={'date': 'Date', 'valeur_celsius': 'Température (°C)', 'type_temp': 'Type'}
)
st.plotly_chart(fig7, use_container_width=True, key="fig7_temp_ville")

# --- Comparaison Sud/Nord : température moyenne max par ville ---
df_moy_ville = df_temp[df_temp['type_temp'] == 'temp_max'].groupby('ville', as_index=False)['valeur_celsius'].mean()
df_moy_ville['ville'] = pd.Categorical(df_moy_ville['ville'], categories=ordre_villes, ordered=True)
df_moy_ville = df_moy_ville.sort_values('ville')

fig8 = px.bar(
    df_moy_ville, x='ville', y='valeur_celsius',
    title="Température maximale moyenne par ville (Sud → Nord)",
    labels={'ville': 'Ville', 'valeur_celsius': 'Température max moyenne (°C)'}
)
st.plotly_chart(fig8, use_container_width=True, key="fig8_temp_sud_nord")



st.divider()
st.header("5. Cartographie des zones protégées et forêts classées")

import folium
from streamlit_folium import st_folium

# --- Filtre par région ---
regions = ['Toutes'] + sorted(df_forets['region'].unique().tolist())
region_choisie = st.selectbox("Filtrer par région", regions, key="filtre_region_forets")

if region_choisie == 'Toutes':
    df_forets_filtre = df_forets
else:
    df_forets_filtre = df_forets[df_forets['region'] == region_choisie]

st.write(f"{len(df_forets_filtre)} zone(s) affichée(s)")

# --- Carte centrée sur le Togo ---
m = folium.Map(location=[8.6, 1.0], zoom_start=7, tiles="OpenStreetMap")

couleurs_region = {
    'Maritime': 'blue',
    'Plateaux': 'green',
    'Centrale': 'orange',
    'Kara': 'red',
    'Savanes': 'purple',
}

for _, row in df_forets_filtre.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"<b>{row['nom_zone']}</b><br>Région: {row['region']}<br>Préfecture: {row['prefecture']}<br>Créée: {row['annee_creation']}",
        tooltip=row['nom_zone'],
        icon=folium.Icon(color=couleurs_region.get(row['region'], 'gray'))
    ).add_to(m)

st_folium(m, use_container_width=True, height=500, key="carte_forets")