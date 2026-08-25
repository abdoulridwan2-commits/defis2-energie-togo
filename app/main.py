import streamlit as st
import pandas as pd
import plotly.express as px
import folium
from streamlit_folium import st_folium

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


# ============================================================
# SIDEBAR : navigation + filtres globaux
# ============================================================
st.sidebar.header("📊 Sections du dashboard")
show_apropos = st.sidebar.checkbox("À propos du projet", value=True)

show_elec = st.sidebar.checkbox("1. Accès à l'électricité", value=True)
show_menage = st.sidebar.checkbox("2. Énergie des ménages", value=True)
show_emissions = st.sidebar.checkbox("3. Émissions polluantes", value=True)
show_climat = st.sidebar.checkbox("4. Variations climatiques", value=True)
show_forets = st.sidebar.checkbox("5. Cartographie des forêts", value=True)

st.sidebar.markdown("---")
st.sidebar.header("🔧 Filtres")

annee_min = int(min(df_elec['annee'].min(), df_menage['annee'].min(), df_co2['annee'].min()))
annee_max = int(max(df_elec['annee'].max(), df_menage['annee'].max(), df_co2['annee'].max()))
liste_annees = list(range(annee_max, annee_min - 1, -1))  # ordre décroissant : 2022, 2021, ...
annee_fin = st.sidebar.selectbox(
    "Afficher jusqu'à l'année",
    liste_annees,
    index=0,
    key="filtre_annee_fin"
)
plage_annees = (annee_min, annee_fin)
st.sidebar.caption(f"Données jusqu'en {annee_fin}")
st.sidebar.caption("ℹ️ S'applique aux sections 1, 2 et 3 (électricité, ménages, émissions)")

# ============================================================
# SECTION 1 — Accès à l'électricité
# ============================================================
if show_apropos:
    st.divider()
    st.header("À propos du projet")
    st.markdown("""
    Ce tableau de bord a été réalisé dans le cadre du **Défi 2 — Énergie & Transition écologique au Togo**.

    **Contexte** : le Togo vise l'accès universel à l'électricité d'ici 2030, tout en développant les énergies
    propres et en protégeant ses forêts. Si les villes sont bien électrifiées, les campagnes restent en retard,
    et la majorité des ménages dépend encore du bois et du charbon de bois pour cuisiner — ce qui fragilise
    les forêts togolaises.

    **Ce dashboard analyse 6 jeux de données** pour :
    - Comparer l'accès à l'électricité entre villes et villages
    - Mesurer la dépendance des ménages au bois/charbon pour la cuisson
    - Dresser le bilan des émissions de gaz à effet de serre par secteur
    - Observer les variations climatiques du Sud au Nord du pays
    - Cartographier les 53 forêts classées et zones protégées

    **Sources des données** : Banque Mondiale (World Development Indicators), données nationales togolaises.
    """)
if show_elec:
    st.divider()
    st.header("1. Accès à l'électricité")

    indicateurs_evolution = [
        'acces_electricite_national_pct',
        'acces_electricite_rural_pct',
        'acces_electricite_urbain_pct',
    ]
    labels = {
        'acces_electricite_national_pct': 'National',
        'acces_electricite_rural_pct': 'Rural',
        'acces_electricite_urbain_pct': 'Urbain',
    }

    df_plot = df_elec[
        (df_elec['indicateur_fr'].isin(indicateurs_evolution)) &
        (df_elec['annee'] >= plage_annees[0]) &
        (df_elec['annee'] <= plage_annees[1])
    ].copy()
    df_plot['zone'] = df_plot['indicateur_fr'].map(labels)

    fig1 = px.line(
        df_plot, x='annee', y='valeur', color='zone',
        title="Évolution de l'accès à l'électricité",
        labels={'annee': 'Année', 'valeur': "Accès à l'électricité (%)", 'zone': 'Zone'}
    )
    st.plotly_chart(fig1, use_container_width=True, key="fig1_acces_electricite")

    col1, col2, col3 = st.columns(3)
    for col, code, label in zip([col1, col2, col3], indicateurs_evolution, ['National', 'Rural', 'Urbain']):
        sub = df_elec[df_elec['indicateur_fr'] == code].sort_values('annee')
        derniere_valeur = sub.iloc[-1]
        col.metric(label, f"{derniere_valeur['valeur']:.1f}%", help=f"Année {int(derniere_valeur['annee'])}")


# ============================================================
# SECTION 2 — Énergie des ménages (cuisson)
# ============================================================
if show_menage:
    st.divider()
    st.header("2. Consommation d'énergie des ménages")

    indicateurs_cuisson = [
        'acces_cuisson_propre_national_pct',
        'acces_cuisson_propre_rural_pct',
        'acces_cuisson_propre_urbain_pct',
    ]
    labels_cuisson = {
        'acces_cuisson_propre_national_pct': 'National',
        'acces_cuisson_propre_rural_pct': 'Rural',
        'acces_cuisson_propre_urbain_pct': 'Urbain',
    }

    df_cuisson = df_menage[
        (df_menage['indicateur_fr'].isin(indicateurs_cuisson)) &
        (df_menage['annee'] >= plage_annees[0]) &
        (df_menage['annee'] <= plage_annees[1])
    ].copy()
    df_cuisson['zone'] = df_cuisson['indicateur_fr'].map(labels_cuisson)

    fig2 = px.line(
        df_cuisson, x='annee', y='valeur', color='zone',
        title="Évolution de l'accès à la cuisson propre",
        labels={'annee': 'Année', 'valeur': 'Accès cuisson propre (%)', 'zone': 'Zone'}
    )
    st.plotly_chart(fig2, use_container_width=True, key="fig2_acces_cuisson")

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


# ============================================================
# SECTION 3 — Émissions polluantes
# ============================================================
if show_emissions:
    st.divider()
    st.header("3. Bilan des émissions polluantes (2018)")

    col1, col2 = st.columns(2)

    with col1:
        df_secteur = df_emissions[(df_emissions['gaz_code'] == 'total') & (df_emissions['secteur_code'] != 'total')].copy()
        labels_secteur = {
            'energie': 'Énergie',
            'procedes_industriels': 'Procédés industriels',
            'agriculture_foresterie': 'Agriculture & Foresterie',
            'dechets': 'Déchets',
        }
        df_secteur['secteur'] = df_secteur['secteur_code'].map(labels_secteur)

        fig4 = px.bar(
            df_secteur.sort_values('valeur_Gg', ascending=True),
            x='valeur_Gg', y='secteur', orientation='h',
            title="Émissions de GES par secteur (Gg)",
            labels={'valeur_Gg': 'Émissions (Gg CO2eq)', 'secteur': 'Secteur'}
        )
        st.plotly_chart(fig4, use_container_width=True, key="fig4_emissions_secteur")

    with col2:
        df_gaz_energie = df_emissions[(df_emissions['secteur_code'] == 'energie') & (df_emissions['gaz_code'] != 'total')].copy()
        labels_gaz = {'CO2': 'CO2', 'CH4': 'Méthane (CH4)', 'N2O': "Protoxyde d'azote (N2O)"}
        df_gaz_energie['gaz'] = df_gaz_energie['gaz_code'].map(labels_gaz)

        fig5 = px.pie(
            df_gaz_energie, values='valeur_Gg', names='gaz',
            title="Répartition des gaz — Secteur Énergie"
        )
        st.plotly_chart(fig5, use_container_width=True, key="fig5_gaz_energie")

    df_co2_filtre = df_co2[(df_co2['annee'] >= plage_annees[0]) & (df_co2['annee'] <= plage_annees[1])]

    fig6 = px.line(
        df_co2_filtre, x='annee', y='co2_secteur_electrique_MtCO2e',
        title="Évolution des émissions CO2 du secteur électrique",
        labels={'annee': 'Année', 'co2_secteur_electrique_MtCO2e': 'Émissions CO2 (Mt CO2e)'}
    )
    st.plotly_chart(fig6, use_container_width=True, key="fig6_co2_electrique")


# ============================================================
# SECTION 4 — Variations climatiques
# ============================================================
if show_climat:
    st.divider()
    st.header("4. Variations climatiques (Sud → Nord)")

    ordre_villes = ['Lomé', 'Tabligbo', 'Kouma konda', 'Atakpamé', 'Sotouboua',
                     'Sokodé', 'Kara', 'Niamtougou', 'Mango', 'Dapaong']

    ville_choisie = st.selectbox("Choisir une ville", ordre_villes, key="select_ville")

    df_ville = df_temp[df_temp['ville'] == ville_choisie].copy()
    df_ville['date'] = pd.to_datetime(df_ville['annee'].astype(str) + '-' + df_ville['mois'].astype(str) + '-01')

    fig7 = px.line(
        df_ville, x='date', y='valeur_celsius', color='type_temp',
        title=f"Évolution des températures — {ville_choisie}",
        labels={'date': 'Date', 'valeur_celsius': 'Température (°C)', 'type_temp': 'Type'}
    )
    st.plotly_chart(fig7, use_container_width=True, key="fig7_temp_ville")

    df_moy_ville = df_temp[df_temp['type_temp'] == 'temp_max'].groupby('ville', as_index=False)['valeur_celsius'].mean()
    df_moy_ville['ville'] = pd.Categorical(df_moy_ville['ville'], categories=ordre_villes, ordered=True)
    df_moy_ville = df_moy_ville.sort_values('ville')

    fig8 = px.bar(
        df_moy_ville, x='ville', y='valeur_celsius',
        title="Température maximale moyenne par ville (Sud → Nord)",
        labels={'ville': 'Ville', 'valeur_celsius': 'Température max moyenne (°C)'}
    )
    st.plotly_chart(fig8, use_container_width=True, key="fig8_temp_sud_nord")


# ============================================================
# SECTION 5 — Cartographie des forêts
# ============================================================
if show_forets:
    st.divider()
    st.header("5. Cartographie des zones protégées et forêts classées")

    regions = ['Toutes'] + sorted(df_forets['region'].unique().tolist())
    region_choisie = st.selectbox("Filtrer par région", regions, key="filtre_region_forets")

    if region_choisie == 'Toutes':
        df_forets_filtre = df_forets
    else:
        df_forets_filtre = df_forets[df_forets['region'] == region_choisie]

    st.write(f"{len(df_forets_filtre)} zone(s) affichée(s)")

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