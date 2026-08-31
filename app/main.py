from pathlib import Path

import folium
import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# ============================================================
# CONFIGURATION DE LA PAGE
# ============================================================
st.set_page_config(
    page_title="Énergie et Transition écologique au Togo",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "clean"
RAW_DIR = BASE_DIR / "data" / "raw"

# ============================================================
# FEUILLE DE STYLE (HARMONISATION TOTALE : TITRE, SIDEBAR, FOOTER)
# ============================================================
st.markdown(
    """
<style>
    /* Structure générale & Grand Titre harmonisé */
    .main-title {
        padding: 24px 28px;
        border-radius: 12px;
        background: linear-gradient(135deg, #087f5b 0%, #065f46 100%);
        box-shadow: 0 4px 14px rgba(8, 127, 91, 0.18);
        margin-bottom: 20px;
        color: #ffffff;
    }
    .main-title-badge {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        color: #a7f3d0;
        margin-bottom: 4px;
    }
    .main-title h1 {
        margin: 0;
        font-size: 28px;
        color: #ffffff;
        font-weight: 700;
        letter-spacing: -0.5px;
    }
    .main-title p {
        margin: 6px 0 0 0;
        color: #d1fae5;
        font-size: 14.5px;
        opacity: 0.95;
    }

    .section-note {
        padding: 12px 16px;
        border-left: 4px solid #087f5b;
        background: #f4faf7;
        border-radius: 6px;
        margin: 6px 0 16px 0;
        color: #2b3a42;
        font-size: 14.5px;
        line-height: 1.5;
    }
    .analysis-box {
        padding: 16px 18px;
        border-radius: 8px;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-left: 4px solid #087f5b;
        margin: 12px 0 18px 0;
        font-size: 14px;
        line-height: 1.55;
    }
    .analysis-box strong.title {
        color: #087f5b;
        font-size: 14.5px;
        display: block;
        margin-bottom: 6px;
    }
    .analysis-item {
        margin-bottom: 5px;
    }
    .analysis-item span.label {
        font-weight: 600;
        color: #1f2937;
    }
    .recommendation {
        padding: 18px;
        border-radius: 12px;
        background: #ffffff;
        border: 1px solid #dfe7e3;
        box-shadow: 0 2px 8px rgba(0,0,0,.04);
        min-height: 200px;
        margin-bottom: 14px;
    }
    .recommendation h3 {
        margin-top: 0;
        color: #087f5b;
        font-size: 17px;
        font-weight: 600;
    }
    .recommendation p {
        color: #4a5568;
        font-size: 13.5px;
        line-height: 1.5;
        margin-bottom: 8px;
    }
    .recommendation .meta-item {
        font-size: 12.5px;
        color: #2d3748;
        background: #f0fdf4;
        padding: 4px 8px;
        border-radius: 4px;
        display: inline-block;
        margin-top: 4px;
        border: 1px solid #bbf7d0;
    }

    /* Style de la barre latérale de navigation */
    [data-testid="stSidebar"] {
        background-color: #f8fafc;
        border-right: 1px solid #e2e8f0;
    }
    .sidebar-header {
        background: linear-gradient(135deg, #087f5b 0%, #065f46 100%);
        padding: 16px 18px;
        border-radius: 10px;
        color: #ffffff;
        margin-bottom: 14px;
        box-shadow: 0 2px 8px rgba(8, 127, 91, 0.18);
    }
    .sidebar-badge {
        font-size: 10px;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        font-weight: 700;
        color: #a7f3d0;
        margin-bottom: 3px;
    }
    .sidebar-title {
        font-size: 16px;
        font-weight: 700;
        letter-spacing: -0.3px;
        color: #ffffff;
    }
    .sidebar-subtitle {
        font-size: 11.5px;
        color: #d1fae5;
        margin-top: 2px;
        opacity: 0.9;
    }
    .sidebar-section-title {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748b;
        margin: 14px 0 6px 0;
        padding-left: 2px;
    }
    .sidebar-info-box {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 11px 13px;
        font-size: 11.5px;
        color: #475569;
        line-height: 1.5;
        margin-top: 14px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
    }
    .sidebar-info-box strong {
        color: #1e293b;
    }

    /* Onglets de navigation interactifs dans la barre latérale */
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label {
        background: #ffffff;
        border: 1px solid #e2e8f0;
        border-radius: 8px;
        padding: 8px 12px;
        margin-bottom: 5px;
        transition: all 0.18s ease-in-out;
        font-size: 13.5px;
        font-weight: 500;
        color: #334155;
        cursor: pointer;
        display: flex;
        align-items: center;
    }
    [data-testid="stSidebar"] .stRadio > div[role="radiogroup"] > label:hover {
        background: #f0fdf4;
        border-color: #86efac;
        color: #087f5b;
        transform: translateX(2px);
    }

    /* Footer harmonisé */
    .custom-footer {
        background: linear-gradient(135deg, #087f5b 0%, #065f46 100%);
        padding: 18px 24px;
        border-radius: 10px;
        color: #ffffff;
        text-align: center;
        margin-top: 36px;
        box-shadow: 0 2px 8px rgba(8, 127, 91, 0.15);
    }
    .custom-footer p {
        margin: 0;
        font-size: 14px;
        color: #ffffff;
        font-weight: 600;
        letter-spacing: -0.2px;
    }
    .custom-footer span {
        font-size: 12px;
        color: #d1fae5;
        display: block;
        margin-top: 3px;
        opacity: 0.9;
    }
</style>
""",
    unsafe_allow_html=True,
)

# ============================================================
# CHARGEMENT DES DONNÉES
# ============================================================
@st.cache_data
def load_data():
    elec = pd.read_csv(DATA_DIR / "01_acces_electricite.csv")
    menage = pd.read_csv(DATA_DIR / "02_energie_menages_cuisson.csv")
    emissions = pd.read_csv(DATA_DIR / "03_emissions_ges_secteur.csv")
    temp = pd.read_csv(DATA_DIR / "04_temperatures_villes.csv", encoding="utf-8")
    co2 = pd.read_csv(DATA_DIR / "05_co2_secteur_electrique.csv")
    ren = pd.read_csv(DATA_DIR / "06_energies_renouvelables.csv")
    forets = pd.read_csv(DATA_DIR / "07_zones_protegees_forets.csv")

    wdi_path = RAW_DIR / "01_indicateurs_wdi_togo.csv"
    if wdi_path.exists():
        wdi = pd.read_csv(wdi_path, skiprows=[1])
        wdi["Value"] = pd.to_numeric(wdi["Value"], errors="coerce")
        wdi["Year"] = pd.to_numeric(wdi["Year"], errors="coerce")
        wdi = wdi.dropna(subset=["Year", "Value"])
    else:
        wdi = pd.DataFrame(columns=["Year", "Indicator Name", "Value"])

    return elec, menage, emissions, temp, co2, ren, forets, wdi


df_elec, df_menage, df_emissions, df_temp, df_co2, df_ren, df_forets, df_wdi = load_data()

# ============================================================
# OUTILS D'EXTRACTION ET D'AFFICHAGE
# ============================================================
def latest_value(df, indicator, year_col="annee", value_col="valeur", max_year=None):
    sub = df[df["indicateur_fr"] == indicator].copy()
    if max_year is not None:
        sub = sub[sub[year_col] <= max_year]
    sub = sub.sort_values(year_col)
    if sub.empty:
        return None, None
    row = sub.iloc[-1]
    return float(row[value_col]), int(row[year_col])


def wdi_latest(indicator_name):
    if df_wdi.empty:
        return None, None
    sub = df_wdi[df_wdi["Indicator Name"] == indicator_name].sort_values("Year")
    if sub.empty:
        return None, None
    row = sub.iloc[-1]
    return float(row["Value"]), int(row["Year"])


def render_analysis_box(resultat: str, signification: str, implication: str, title: str = "Synthèse analytique"):
    st.markdown(
        f"""
<div class="analysis-box">
    <strong class="title">{title}</strong>
    <div class="analysis-item"><span class="label">Résultat : </span>{resultat}</div>
    <div class="analysis-item"><span class="label">Signification : </span>{signification}</div>
    <div class="analysis-item"><span class="label">Implication pour le Togo : </span>{implication}</div>
</div>
""",
        unsafe_allow_html=True,
    )


# ============================================================
# EN-TÊTE PRINCIPAL (COULEURS HARMONISÉES AVEC LA SIDEBAR)
# ============================================================
st.markdown(
    """
<div class="main-title">
    <div class="main-title-badge">RÉPUBLIQUE TOGOLAISE • DÉFI 2</div>
    <h1>Énergie et Transition écologique au Togo</h1>
    <p>Électricité | Cuisson propre | Émissions de GES | Climat | Énergies renouvelables | Forêts protégées</p>
</div>
""",
    unsafe_allow_html=True,
)

# ============================================================
# BARRE LATÉRALE DE NAVIGATION (DESIGN MODERNE ET ÉPURÉ)
# ============================================================
with st.sidebar:
    st.markdown(
        """
<div class="sidebar-header">
    <div class="sidebar-badge">DÉFI 2 — TOGO 2026</div>
    <div class="sidebar-title">Énergie & Climat</div>
    <div class="sidebar-subtitle">Tableau de bord décisionnel</div>
</div>
""",
        unsafe_allow_html=True,
    )

    st.markdown('<div class="sidebar-section-title">Navigation principale</div>', unsafe_allow_html=True)
    section = st.radio(
        "Sections",
        [
            "Vue d'ensemble",
            "1. Accès à l'électricité",
            "2. Énergie des ménages",
            "3. Émissions polluantes",
            "4. Variations climatiques",
            "5. Forêts et zones protégées",
            "6. Recommandations",
            "À propos et méthodologie",
        ],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sidebar-section-title">Filtres temporels</div>', unsafe_allow_html=True)

    all_years = sorted(
        set(pd.to_numeric(df_elec["annee"], errors="coerce").dropna().astype(int))
        | set(pd.to_numeric(df_menage["annee"], errors="coerce").dropna().astype(int))
        | set(pd.to_numeric(df_co2["annee"], errors="coerce").dropna().astype(int))
    )
    year_max = int(max(all_years))
    year_min = int(min(all_years))

    annee_ref = st.selectbox(
        "Année de référence (plafond)",
        list(range(year_max, year_min - 1, -1)),
        index=0,
    )
    st.caption(f"Données synchronisées jusqu'en **{annee_ref}**.")

    st.markdown(
        """
<div class="sidebar-info-box">
    <strong>Périmètre consolidé :</strong>
    <div>• Horizon : 1970–2022</div>
    <div>• Couverture : 5 Régions • 10 Stations</div>
    <div>• 53 zones protégées répertoriées</div>
    <div>• Sources : WDI, MERF, DGMN</div>
</div>
""",
        unsafe_allow_html=True,
    )

# ============================================================
# CALCUL DES VALEURS CLÉS DYNAMIQUES
# ============================================================
val_nat, year_nat = latest_value(df_elec, "acces_electricite_national_pct", max_year=annee_ref)
val_rural, year_rural = latest_value(df_elec, "acces_electricite_rural_pct", max_year=annee_ref)
val_urbain, year_urbain = latest_value(df_elec, "acces_electricite_urbain_pct", max_year=annee_ref)
val_clean, year_clean = latest_value(df_menage, "acces_cuisson_propre_national_pct", max_year=annee_ref)
val_clean_rur, year_clean_rur = latest_value(df_menage, "acces_cuisson_propre_rural_pct", max_year=annee_ref)
val_clean_urb, year_clean_urb = latest_value(df_menage, "acces_cuisson_propre_urbain_pct", max_year=annee_ref)

# ============================================================
# SECTION : VUE D'ENSEMBLE
# ============================================================
if section == "Vue d'ensemble":
    st.header("Vue d'ensemble")
    st.markdown(
        '<div class="section-note">Cette vue synthétise les indicateurs macro-énergétiques et environnementaux du Togo. Elle met en évidence les disparités territoriales majeures et les équilibres sectoriels qui orientent les priorités nationales.</div>',
        unsafe_allow_html=True,
    )

    # Cartes KPI
    k1, k2, k3, k4 = st.columns(4)
    k1.metric(
        "Accès national à l'électricité",
        f"{val_nat:.1f} %" if val_nat is not None else "N/D",
        f"Année {year_nat}" if year_nat else "",
    )
    k2.metric(
        "Accès en milieu rural",
        f"{val_rural:.1f} %" if val_rural is not None else "N/D",
        f"Année {year_rural}" if year_rural else "",
    )
    k3.metric(
        "Accès en milieu urbain",
        f"{val_urbain:.1f} %" if val_urbain is not None else "N/D",
        f"Année {year_urbain}" if year_urbain else "",
    )
    k4.metric(
        "Accès à la cuisson propre",
        f"{val_clean:.1f} %" if val_clean is not None else "N/D",
        f"Année {year_clean}" if year_clean else "",
    )

    if val_rural is not None and val_urbain is not None:
        ecart_actuel = val_urbain - val_rural
        render_analysis_box(
            resultat=f"En {annee_ref}, le taux d'accès national à l'électricité est de {val_nat:.1f} %, avec un écart de {ecart_actuel:.1f} points entre le milieu urbain ({val_urbain:.1f} %) et le milieu rural ({val_rural:.1f} %). En parallèle, la cuisson propre ne couvre que {val_clean:.1f} % de la population nationale.",
            signification="Le pays connaît une transition énergétique à double vitesse : alors que les zones urbaines sont presque totalement électrifiées, les zones rurales accusent un retard structurel massif aussi bien pour l'électricité que pour la cuisson propre.",
            implication="Les investissements prioritaires de l'État et des partenaires doivent se concentrer sur l'électrification rurale décentralisée (mini-réseaux et kits solaires) et sur la diffusion à grande échelle de foyers améliorés et de combustibles modernes de cuisson.",
            title="Constat macro-énergétique",
        )

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("Trajectoire de l'accès à l'électricité")
        plot_elec = df_elec[
            (df_elec["indicateur_fr"].isin([
                "acces_electricite_national_pct",
                "acces_electricite_rural_pct",
                "acces_electricite_urbain_pct",
            ]))
            & (df_elec["annee"] <= annee_ref)
        ].copy()
        plot_elec["Zone"] = plot_elec["indicateur_fr"].map({
            "acces_electricite_national_pct": "National",
            "acces_electricite_rural_pct": "Rural",
            "acces_electricite_urbain_pct": "Urbain",
        })
        fig_elec = px.line(
            plot_elec,
            x="annee",
            y="valeur",
            color="Zone",
            markers=True,
            labels={"annee": "Année", "valeur": "Taux d'accès (%)", "Zone": "Territoire"},
            color_discrete_map={"National": "#087f5b", "Rural": "#d97706", "Urbain": "#2563eb"},
        )
        fig_elec.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_elec, use_container_width=True)

    with c2:
        st.subheader("Part des énergies renouvelables")
        ren_sub = df_ren[df_ren["annee"] <= annee_ref].sort_values("annee").copy()
        fig_ren = px.area(
            ren_sub,
            x="annee",
            y="energies_renouvelables_pct",
            labels={"annee": "Année", "energies_renouvelables_pct": "Part dans la consommation finale (%)"},
            color_discrete_sequence=["#10b981"],
        )
        fig_ren.update_layout(hovermode="x unified")
        st.plotly_chart(fig_ren, use_container_width=True)

    st.subheader("Enseignements transversaux clés")
    col_a, col_b, col_c = st.columns(3)
    with col_a:
        st.markdown("**Électrification rurale**")
        st.write("Le déficit d'accès est à 75 % concentré en milieu rural. L'extension du réseau centralisé étant coûteuse, les mini-réseaux solaires autonomes constituent la solution technique la plus rapide.")
    with col_b:
        st.markdown("**Nexus Cuisson et Forêts**")
        st.write("89,4 % des ménages dépendent du bois et du charbon. Cette demande exerce une pression directe sur les 53 zones forestières protégées et explique 87,7 % des émissions de GES nationales (AFAT).")
    with col_c:
        st.markdown("**Gradient Climatique et Solaire**")
        st.write("Les températures maximales atteignent 35,5 °C en moyenne à Mango dans le Nord (pics à 41 °C). Ce climat septentrional offre un gisement solaire élevé mais accroît les besoins en pompage et chaîne du froid.")

# ============================================================
# SECTION 1 : ACCÈS À L'ÉLECTRICITÉ
# ============================================================
elif section == "1. Accès à l'électricité":
    st.header("1. Accès à l'électricité")
    st.markdown(
        '<div class="section-note">Analyse de la progression du taux d\'électrification national, de la divergence entre milieux urbain et rural, ainsi que des contraintes de fiabilité et de coût de raccordement pour les entreprises.</div>',
        unsafe_allow_html=True,
    )

    indicators = [
        "acces_electricite_national_pct",
        "acces_electricite_rural_pct",
        "acces_electricite_urbain_pct",
    ]
    labels_map = {
        "acces_electricite_national_pct": "National",
        "acces_electricite_rural_pct": "Rural",
        "acces_electricite_urbain_pct": "Urbain",
    }

    plot_df = df_elec[df_elec["indicateur_fr"].isin(indicators)].copy()
    plot_df["Zone"] = plot_df["indicateur_fr"].map(labels_map)

    # Filtres interactifs
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        zones_sel = st.multiselect(
            "Territoires à afficher",
            ["National", "Rural", "Urbain"],
            default=["National", "Rural", "Urbain"],
        )
    with col_f2:
        min_available = int(plot_df["annee"].min())
        annee_debut = st.slider("Année de début de la série", min_available, int(annee_ref), min_available)

    filtered_elec = plot_df[
        (plot_df["Zone"].isin(zones_sel))
        & (plot_df["annee"] >= annee_debut)
        & (plot_df["annee"] <= annee_ref)
    ]

    fig_elec_main = px.line(
        filtered_elec,
        x="annee",
        y="valeur",
        color="Zone",
        markers=True,
        labels={"annee": "Année", "valeur": "Taux d'accès (%)", "Zone": "Territoire"},
        color_discrete_map={"National": "#087f5b", "Rural": "#d97706", "Urbain": "#2563eb"},
    )
    fig_elec_main.update_layout(hovermode="x unified")
    st.plotly_chart(fig_elec_main, use_container_width=True)

    # Indicateurs chiffrés pour l'année sélectionnée
    c1, c2, c3, c4 = st.columns(4)
    v_nat, y_nat = latest_value(df_elec, "acces_electricite_national_pct", max_year=annee_ref)
    v_rur, y_rur = latest_value(df_elec, "acces_electricite_rural_pct", max_year=annee_ref)
    v_urb, y_urb = latest_value(df_elec, "acces_electricite_urbain_pct", max_year=annee_ref)
    gap_val = (v_urb - v_rur) if (v_urb is not None and v_rur is not None) else None

    c1.metric("Accès National", f"{v_nat:.1f} %" if v_nat else "N/D", f"en {y_nat}" if y_nat else "")
    c2.metric("Accès Rural", f"{v_rur:.1f} %" if v_rur else "N/D", f"en {y_rur}" if y_rur else "")
    c3.metric("Accès Urbain", f"{v_urb:.1f} %" if v_urb else "N/D", f"en {y_urb}" if y_urb else "")
    c4.metric("Écart Urbain - Rural", f"{gap_val:.1f} pts" if gap_val else "N/D", "Disparité territoriale")

    # Conclusion structurée
    render_analysis_box(
        resultat="En 2022, le taux d'accès atteint 96,5 % en zone urbaine contre 25,0 % en zone rurale (57,2 % au niveau national). L'écart s'est creusé de 38,1 points en 1998 (41,2 % urbain vs 3,1 % rural) à 71,5 points en 2022.",
        signification="Bien que le taux national ait progressé de +41,9 points en 24 ans, cette avancée a été très asymétrique. Les investissements sur le réseau conventionnel ont saturé la demande urbaine sans combler la fracture avec le monde rural.",
        implication="Pour atteindre l'objectif gouvernemental d'accès universel à l'horizon 2030, la priorité absolue doit être réorientée vers les zones rurales isolées via des concessions de mini-réseaux solaires et des programmes d'équipements photovoltaïques individuels.",
        title="Analyse de la dynamique d'électrification",
    )

    st.subheader("Fiabilité du service et climat des affaires")
    st.markdown("Données de la Banque mondiale (WDI) sur la qualité de fourniture électrique pour le secteur productif :")

    wdi_outages = [
        ("entreprises_touchees_coupures_pct", "Entreprises subissant des coupures de courant (% des entreprises)", "%"),
        ("pertes_coupures_pct_ventes", "Pertes de valeur dues aux coupures (% du chiffre d'affaires)", "%"),
        ("delai_connexion_jours", "Délai moyen pour obtenir un raccordement électrique (jours)", "jours"),
        ("cout_connexion_pct_revenu", "Coût d'obtention d'un raccordement (% du RNB par habitant)", "%"),
    ]
    outage_data = []
    for code, label, unit in wdi_outages:
        val, yr = latest_value(df_elec, code, max_year=annee_ref)
        if val is not None:
            outage_data.append({"Indicateur": label, "Valeur": f"{val:.1f} {unit}", "Année de référence": yr})

    if outage_data:
        st.dataframe(pd.DataFrame(outage_data), use_container_width=True, hide_index=True)
        render_analysis_box(
            resultat="93,8 % des entreprises togolaises déclarent subir des coupures électriques (2016), engendrant une perte moyenne directe de 3,7 % de leur chiffre d'affaires. Le délai moyen de raccordement était de 66 jours en 2019.",
            signification="Le défi énergétique ne se résume pas au raccordement physique : l'instabilité de l'alimentation électrique pénalise directement la compétitivité des entreprises et la rentabilité industrielle.",
            implication="La politique énergétique doit combiner extension de l'accès et modernisation du réseau de distribution (numérisation, renforcement des transformateurs, réduction des pertes en ligne).",
            title="Analyse de la qualité du réseau",
        )
    else:
        st.info("Données de fiabilité non disponibles pour la période sélectionnée.")

# ============================================================
# SECTION 2 : ÉNERGIE DES MÉNAGES ET CUISSON
# ============================================================
elif section == "2. Énergie des ménages":
    st.header("2. Énergie des ménages et cuisson")
    st.markdown(
        '<div class="section-note">Examen de la dépendance aux combustibles de cuisson traditionnels (bois, charbon) et du taux d\'adoption des solutions de cuisson propre selon le milieu de résidence.</div>',
        unsafe_allow_html=True,
    )

    clean_indicators = [
        "acces_cuisson_propre_national_pct",
        "acces_cuisson_propre_rural_pct",
        "acces_cuisson_propre_urbain_pct",
    ]
    clean_labels = {
        "acces_cuisson_propre_national_pct": "National",
        "acces_cuisson_propre_rural_pct": "Rural",
        "acces_cuisson_propre_urbain_pct": "Urbain",
    }

    clean_df = df_menage[
        (df_menage["indicateur_fr"].isin(clean_indicators))
        & (df_menage["annee"] <= annee_ref)
    ].copy()
    clean_df["Zone"] = clean_df["indicateur_fr"].map(clean_labels)

    col_sel1, col_sel2 = st.columns([1, 1])
    with col_sel1:
        cuisson_zones = st.multiselect(
            "Territoires à afficher",
            ["National", "Rural", "Urbain"],
            default=["National", "Rural", "Urbain"],
            key="ms_cuisson",
        )

    clean_filtered = clean_df[clean_df["Zone"].isin(cuisson_zones)]
    fig_clean = px.line(
        clean_filtered,
        x="annee",
        y="valeur",
        color="Zone",
        markers=True,
        labels={"annee": "Année", "valeur": "Accès à la cuisson propre (%)", "Zone": "Territoire"},
        color_discrete_map={"National": "#087f5b", "Rural": "#d97706", "Urbain": "#2563eb"},
    )
    fig_clean.update_layout(hovermode="x unified")
    st.plotly_chart(fig_clean, use_container_width=True)

    k1, k2, k3 = st.columns(3)
    k1.metric("Cuisson propre National", f"{val_clean:.1f} %" if val_clean else "N/D", f"Année {year_clean}")
    k2.metric("Cuisson propre Rural", f"{val_clean_rur:.2f} %" if val_clean_rur else "N/D", f"Année {year_clean_rur}")
    k3.metric("Cuisson propre Urbain", f"{val_clean_urb:.1f} %" if val_clean_urb else "N/D", f"Année {year_clean_urb}")

    render_analysis_box(
        resultat="En 2022, l'accès à la cuisson propre ne concerne que 11,9 % des ménages au niveau national, avec un contraste extrême entre les zones urbaines (24,15 %) et les zones rurales (0,90 %).",
        signification="Le monde rural togolais est en situation de quasi-dépendance totale aux combustibles de biomasse brute. La transition vers des combustibles propres (gaz GPL, biogaz, électricité) reste embryonnaire en dehors des centres urbains.",
        implication="La précarité énergétique de cuisson a un impact direct sur la santé des femmes et des enfants (pollution de l'air intérieur) et accélère la déforestation périurbaine et rurale.",
        title="Analyse de l'accès à la cuisson propre",
    )

    st.subheader("Structure des combustibles principaux de cuisson")

    fuel_indicators = {
        "combustible_bois_pct_menages": "Bois de chauffe",
        "combustible_charbon_pct_menages": "Charbon de bois",
        "combustible_gaz_pct_menages": "Gaz (GPL/butane)",
        "combustible_electricite_pct_menages": "Électricité",
        "combustible_paille_pct_menages": "Paille et branchages",
        "combustible_residus_agricoles_pct_menages": "Résidus agricoles",
        "combustible_bouse_pct_menages": "Bouse animale",
    }

    fuel_df_raw = df_menage[df_menage["indicateur_fr"].isin(fuel_indicators.keys())].copy()
    fuel_df_raw["Combustible"] = fuel_df_raw["indicateur_fr"].map(fuel_indicators)

    annees_fuel = sorted(fuel_df_raw["annee"].unique().tolist())
    if annees_fuel:
        sel_fuel_year = st.selectbox(
            "Année d'enquête sur les combustibles",
            annees_fuel,
            index=len(annees_fuel) - 1,
            key="fuel_yr_sel",
        )
        fuel_current = fuel_df_raw[fuel_df_raw["annee"] == sel_fuel_year].sort_values("valeur", ascending=True)

        c_f1, c_f2 = st.columns([1.3, 1])
        with c_f1:
            fig_bar_fuel = px.bar(
                fuel_current,
                x="valeur",
                y="Combustible",
                orientation="h",
                text_auto=".1f",
                labels={"valeur": "Part des ménages (%)", "Combustible": "Source d'énergie"},
                color="valeur",
                color_continuous_scale="Greens",
            )
            fig_bar_fuel.update_layout(showlegend=False, coloraxis_showscale=False)
            st.plotly_chart(fig_bar_fuel, use_container_width=True)

        with c_f2:
            fig_pie_fuel = px.pie(
                fuel_current,
                values="valeur",
                names="Combustible",
                hole=0.4,
                color_discrete_sequence=px.colors.qualitative.Safe,
            )
            fig_pie_fuel.update_traces(textposition="inside", textinfo="percent+label")
            st.plotly_chart(fig_pie_fuel, use_container_width=True)

        bois_val = fuel_current[fuel_current["Combustible"] == "Bois de chauffe"]["valeur"].sum()
        charbon_val = fuel_current[fuel_current["Combustible"] == "Charbon de bois"]["valeur"].sum()
        gaz_val = fuel_current[fuel_current["Combustible"] == "Gaz (GPL/butane)"]["valeur"].sum()
        biomasse_solide = bois_val + charbon_val

        render_analysis_box(
            resultat=f"En {sel_fuel_year}, le bois de chauffe ({bois_val:.1f} %) et le charbon de bois ({charbon_val:.1f} %) totalisent ensemble {biomasse_solide:.1f} % de l'énergie de cuisson des ménages togolais, contre {gaz_val:.1f} % pour le gaz et moins de 1 % pour l'électricité.",
            signification="Près de 9 ménages sur 10 recourent quotidiennement à la biomasse forestière pour couvrir leurs besoins nutritionnels essentiels, confirmant une très forte inertie des habitudes énergétiques domestiques.",
            implication="Pour soulager la pression sur le couvert forestier, le Togo doit déployer une politique intégrée : défiscalisation du gaz butane, structuration de filières de biogaz communautaire et distribution massive de foyers améliorés certifiés à haute efficacité thermique.",
            title="Analyse du mix de cuisson",
        )

# ============================================================
# SECTION 3 : ÉMISSIONS POLLUANTES
# ============================================================
elif section == "3. Émissions polluantes":
    st.header("3. Bilan des émissions polluantes")
    st.markdown(
        '<div class="section-note">Évaluation des émissions directes de gaz à effet de serre (GES) par secteur d\'activité économique et analyse de la trajectoire d\'émissions du secteur électrique.</div>',
        unsafe_allow_html=True,
    )

    secteur_labels = {
        "agriculture_foresterie": "Agriculture, Foresterie et Terres (AFAT)",
        "energie": "Énergie (Combustion & Procédés)",
        "procedes_industriels": "Procédés industriels (PIUP)",
        "dechets": "Déchets",
    }

    df_sect = df_emissions[
        (df_emissions["gaz_code"] == "total") & (df_emissions["secteur_code"] != "total")
    ].copy()
    df_sect["Secteur"] = df_sect["secteur_code"].map(secteur_labels)
    total_national_ges = df_sect["valeur_Gg"].sum()
    df_sect["Part (%)"] = (df_sect["valeur_Gg"] / total_national_ges) * 100

    col_e1, col_e2 = st.columns(2)
    with col_e1:
        fig_bar_ges = px.bar(
            df_sect.sort_values("valeur_Gg", ascending=True),
            x="valeur_Gg",
            y="Secteur",
            orientation="h",
            text_auto=".1f",
            labels={"valeur_Gg": "Émissions (Gg CO₂e)", "Secteur": "Secteur d'activité"},
            color="Part (%)",
            color_continuous_scale="Reds",
        )
        fig_bar_ges.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_bar_ges, use_container_width=True)

    with col_e2:
        fig_pie_ges = px.pie(
            df_sect,
            values="valeur_Gg",
            names="Secteur",
            hole=0.45,
            color_discrete_sequence=["#b91c1c", "#ea580c", "#d97706", "#64748b"],
        )
        fig_pie_ges.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie_ges, use_container_width=True)

    afat_val = df_sect[df_sect["secteur_code"] == "agriculture_foresterie"]["valeur_Gg"].values[0]
    afat_pct = df_sect[df_sect["secteur_code"] == "agriculture_foresterie"]["Part (%)"].values[0]
    nrj_val = df_sect[df_sect["secteur_code"] == "energie"]["valeur_Gg"].values[0]
    nrj_pct = df_sect[df_sect["secteur_code"] == "energie"]["Part (%)"].values[0]

    render_analysis_box(
        resultat=f"En 2018, le secteur AFAT représente à lui seul {afat_pct:.1f} % des émissions nationales directes ({afat_val:.1f} Gg CO₂e sur un total de {total_national_ges:.1f} Gg), tandis que le secteur Énergie ne contribue qu'à hauteur de {nrj_pct:.1f} % ({nrj_val:.1f} Gg).",
        signification="Le profil d'émissions du Togo est très atypique par rapport aux pays industrialisés : l'essentiel de l'empreinte carbone provient de la dégradation forestière, des changements d'usage des sols et de l'agriculture, et non de la consommation d'hydrocarbures industriels.",
        implication="La décarbonation du Togo passe impérativement par une politique agroforestière rigoureuse, la lutte contre les feux de brousse et la substitution du bois-énergie, qui constituent le premier gisement d'atténuation climatique du pays.",
        title="Analyse sectorielle des émissions de gaz à effet de serre",
    )

    st.subheader("Décomposition des gaz par secteur")
    sect_choice = st.selectbox(
        "Sélectionner un secteur pour visualiser le profil des gaz émis",
        list(secteur_labels.keys()),
        format_func=lambda x: secteur_labels[x],
    )
    df_gaz_sub = df_emissions[
        (df_emissions["secteur_code"] == sect_choice) & (df_emissions["gaz_code"] != "total")
    ].copy()
    gaz_names = {"CO2": "Dioxyde de carbone (CO₂)", "CH4": "Méthane (CH₄)", "N2O": "Protoxyde d'azote (N₂O)"}
    df_gaz_sub["Gaz"] = df_gaz_sub["gaz_code"].map(gaz_names)

    fig_gaz_pie = px.pie(
        df_gaz_sub,
        values="valeur_Gg",
        names="Gaz",
        hole=0.4,
        color_discrete_sequence=["#dc2626", "#f59e0b", "#3b82f6"],
    )
    st.plotly_chart(fig_gaz_pie, use_container_width=True)

    st.subheader("Évolution historique des émissions du secteur électrique")
    co2_elec_df = df_co2[df_co2["annee"] <= annee_ref].sort_values("annee").copy()
    fig_co2_line = px.line(
        co2_elec_df,
        x="annee",
        y="co2_secteur_electrique_MtCO2e",
        markers=True,
        labels={"annee": "Année", "co2_secteur_electrique_MtCO2e": "Émissions (Mt CO₂e)"},
        color_discrete_sequence=["#e11d48"],
    )
    fig_co2_line.update_layout(hovermode="x unified")
    st.plotly_chart(fig_co2_line, use_container_width=True)

    co2_init = co2_elec_df.iloc[0]["co2_secteur_electrique_MtCO2e"]
    co2_latest = co2_elec_df.iloc[-1]["co2_secteur_electrique_MtCO2e"]
    co2_2000_row = co2_elec_df[co2_elec_df["annee"] == 2000]
    co2_2000 = co2_2000_row.iloc[0]["co2_secteur_electrique_MtCO2e"] if not co2_2000_row.empty else co2_init
    hausse_depuis_2000 = ((co2_latest - co2_2000) / co2_2000) * 100

    render_analysis_box(
        resultat=f"Les émissions du secteur électrique sont passées de {co2_init:.4f} Mt CO₂e en 1970 et {co2_2000:.4f} Mt en 2000 à {co2_latest:.4f} Mt CO₂e en {int(co2_elec_df.iloc[-1]['annee'])}, soit une augmentation de +{hausse_depuis_2000:.1f} % depuis 2000.",
        signification="Cette augmentation traduit la mise en service de capacités thermiques pour répondre à la hausse de la demande nationale et pallier l'intermittence des importations régionales.",
        implication="Le volume absolu restant modéré (< 0,25 Mt CO₂e), le Togo a l'opportunité de verdir directement son réseau en priorisant le solaire photovoltaïque raccordé et l'hydroélectricité avant que l'empreinte thermique ne devienne bloquante.",
        title="Analyse de la trajectoire carbone du secteur électrique",
    )

# ============================================================
# SECTION 4 : VARIATIONS CLIMATIQUES & GRADIENT THERMIQUE
# ============================================================
elif section == "4. Variations climatiques":
    st.header("4. Variations climatiques et gradient thermique Sud-Nord")
    st.markdown(
        '<div class="section-note">Analyse des séries thermiques mensuelles (2013–2019) sur 10 stations météorologiques représentatives du gradient Sud–Nord togolais et implications pour la planification énergétique.</div>',
        unsafe_allow_html=True,
    )

    ordre_villes = [
        "Lomé",
        "Tabligbo",
        "Kouma konda",
        "Atakpamé",
        "Sotouboua",
        "Sokodé",
        "Kara",
        "Niamtougou",
        "Mango",
        "Dapaong",
    ]
    villes_existantes = [v for v in ordre_villes if v in df_temp["ville"].unique()]

    # Calcul robuste et consolidé des indicateurs climatiques par station
    tmax_df = df_temp[df_temp["type_temp"] == "temp_max"]
    tmin_df = df_temp[df_temp["type_temp"] == "temp_min"]

    avg_max = tmax_df.groupby("ville")["valeur_celsius"].agg(
        Tmax_moyenne="mean",
        Tmax_record="max"
    ).reset_index()

    avg_min = tmin_df.groupby("ville")["valeur_celsius"].agg(
        Tmin_moyenne="mean",
        Tmin_record="min"
    ).reset_index()

    avg_all = pd.merge(avg_max, avg_min, on="ville")
    avg_all["Amplitude_moyenne"] = avg_all["Tmax_moyenne"] - avg_all["Tmin_moyenne"]
    avg_all["ville"] = pd.Categorical(avg_all["ville"], categories=ordre_villes, ordered=True)
    avg_all = avg_all.sort_values("ville").reset_index(drop=True)

    hottest_row = avg_all.loc[avg_all["Tmax_moyenne"].idxmax()]
    coolest_row = avg_all.loc[avg_all["Tmax_moyenne"].idxmin()]
    max_amp_row = avg_all.loc[avg_all["Amplitude_moyenne"].idxmax()]
    min_amp_row = avg_all.loc[avg_all["Amplitude_moyenne"].idxmin()]

    # Cartes d'indicateurs thermiques majeurs
    kc1, kc2, kc3, kc4 = st.columns(4)
    kc1.metric("Station la plus chaude", f"{hottest_row['ville']}", f"{hottest_row['Tmax_moyenne']:.1f} °C moy. (pic {int(hottest_row['Tmax_record'])} °C)")
    kc2.metric("Station la plus tempérée", f"{coolest_row['ville']}", f"{coolest_row['Tmax_moyenne']:.1f} °C moy. (relief)")
    kc3.metric("Amplitude maximale (Nord)", f"{max_amp_row['ville']}", f"{max_amp_row['Amplitude_moyenne']:.1f} °C d'écart")
    kc4.metric("Régulation côtière (Sud)", f"{min_amp_row['ville']}", f"{min_amp_row['Amplitude_moyenne']:.1f} °C d'écart")

    # Onglets d'exploration dynamique
    tab_temp1, tab_temp2, tab_temp3 = st.tabs([
        "Évolution par station & comparateur",
        "Gradient territorial Sud-Nord",
        "Cycle de saisonnalité mensuelle"
    ])

    with tab_temp1:
        st.subheader("Chronologie des températures (2013–2019)")
        col_c1, col_c2, col_c3 = st.columns(3)
        with col_c1:
            villes_selectionnees = st.multiselect(
                "Choisir une ou plusieurs stations",
                villes_existantes,
                default=["Mango", "Lomé"],
                help="Sélectionnez plusieurs villes pour comparer leurs courbes de température."
            )
        with col_c2:
            annees_temp = sorted(df_temp["annee"].unique().tolist())
            annee_temp_sel = st.selectbox(
                "Période d'observation",
                ["Toutes les années (2013-2019)"] + [str(y) for y in annees_temp]
            )
        with col_c3:
            types_temp_sel = st.multiselect(
                "Indicateurs thermiques",
                ["temp_max", "temp_min"],
                default=["temp_max", "temp_min"],
                format_func=lambda x: "Température maximale" if x == "temp_max" else "Température minimale",
            )

        if villes_selectionnees and types_temp_sel:
            df_t_sub = df_temp[
                (df_temp["ville"].isin(villes_selectionnees))
                & (df_temp["type_temp"].isin(types_temp_sel))
            ].copy()

            if annee_temp_sel != "Toutes les années (2013-2019)":
                df_t_sub = df_t_sub[df_t_sub["annee"] == int(annee_temp_sel)]

            df_t_sub["date"] = pd.to_datetime(
                df_t_sub["annee"].astype(str) + "-" + df_t_sub["mois"].astype(str).str.zfill(2) + "-01"
            )
            df_t_sub["Série"] = df_t_sub["ville"] + " — " + df_t_sub["type_temp"].map(
                {"temp_max": "Max", "temp_min": "Min"}
            )

            fig_t_dyn = px.line(
                df_t_sub.sort_values("date"),
                x="date",
                y="valeur_celsius",
                color="Série",
                markers=True,
                labels={"date": "Date", "valeur_celsius": "Température (°C)", "Série": "Station & Type"},
                color_discrete_sequence=px.colors.qualitative.Dark24,
            )
            fig_t_dyn.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
            st.plotly_chart(fig_t_dyn, use_container_width=True)
        else:
            st.warning("Veuillez sélectionner au moins une station météorologique et un indicateur thermique.")

    with tab_temp2:
        st.subheader("Gradient thermique du littoral au grand Nord")
        st.markdown("Comparaison des températures maximales et minimales moyennes ordonnées géographiquement du Sud (Lomé) vers le Nord (Dapaong) :")

        fig_grad_bars = go.Figure()
        fig_grad_bars.add_trace(go.Bar(
            x=avg_all["ville"],
            y=avg_all["Tmax_moyenne"],
            name="Température maximale moyenne",
            marker_color="#dc2626",
            text=[f"{v:.1f} °C" for v in avg_all["Tmax_moyenne"]],
            textposition="auto",
        ))
        fig_grad_bars.add_trace(go.Bar(
            x=avg_all["ville"],
            y=avg_all["Tmin_moyenne"],
            name="Température minimale moyenne",
            marker_color="#2563eb",
            text=[f"{v:.1f} °C" for v in avg_all["Tmin_moyenne"]],
            textposition="auto",
        ))
        fig_grad_bars.update_layout(
            barmode="group",
            xaxis_title="Station météorologique (Sud vers le Nord)",
            yaxis_title="Température moyenne (°C)",
            hovermode="x unified",
            legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
        )
        st.plotly_chart(fig_grad_bars, use_container_width=True)

        st.dataframe(
            avg_all.rename(columns={
                "ville": "Station",
                "Tmax_moyenne": "Tmax moyenne (°C)",
                "Tmax_record": "Pic maximal absolu (°C)",
                "Tmin_moyenne": "Tmin moyenne (°C)",
                "Tmin_record": "Minimum absolu (°C)",
                "Amplitude_moyenne": "Amplitude thermique moyenne (°C)",
            }).round(1),
            use_container_width=True,
            hide_index=True,
        )

    with tab_temp3:
        st.subheader("Cycle annuel et variations saisonnières")
        st.markdown("Moyenne des températures maximales mois par mois sur la période 2013–2019 :")

        df_month_calc = df_temp[df_temp["type_temp"] == "temp_max"].groupby(
            ["ville", "mois"], as_index=False
        )["valeur_celsius"].mean()

        mois_labels = {
            1: "Janvier", 2: "Février", 3: "Mars", 4: "Avril", 5: "Mai", 6: "Juin",
            7: "Juillet", 8: "Août", 9: "Septembre", 10: "Octobre", 11: "Novembre", 12: "Décembre"
        }
        df_month_calc["Mois"] = df_month_calc["mois"].map(mois_labels)
        df_month_calc["ville"] = pd.Categorical(df_month_calc["ville"], categories=ordre_villes, ordered=True)

        fig_heat_month = px.line(
            df_month_calc.sort_values(["ville", "mois"]),
            x="Mois",
            y="valeur_celsius",
            color="ville",
            markers=True,
            labels={"valeur_celsius": "Tmax moyenne (°C)", "ville": "Station"},
            color_discrete_sequence=px.colors.qualitative.Bold,
        )
        fig_heat_month.update_layout(hovermode="x unified", legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_heat_month, use_container_width=True)

    render_analysis_box(
        resultat=f"La ville de {hottest_row['ville']} enregistre la température maximale moyenne la plus élevée à {hottest_row['Tmax_moyenne']:.1f} °C (avec des pics observés à {int(hottest_row['Tmax_record'])} °C), alors que la station d'altitude de {coolest_row['ville']} présente la moyenne la plus basse à {coolest_row['Tmax_moyenne']:.1f} °C. L'amplitude thermique mensuelle grimpe à {max_amp_row['Amplitude_moyenne']:.1f} °C dans le Nord contre seulement {min_amp_row['Amplitude_moyenne']:.1f} °C sur la côte à Lomé.",
        signification="Un gradient climatique très net sépare la zone côtière et montagneuse méridionale (tempérée par l'océan et le relief) des régions septentrionales (Savanes et Kara) soumises à un climat soudano-sahélien à forte amplitude thermique et à pics de chaleur intenses en mars-avril.",
        implication="Ce gradient impose une différenciation territoriale des politiques énergétiques : le grand Nord togolais bénéficie d'une irradiance solaire maximale justifiant de grandes centrales photovoltaïques et du pompage solaire agricole, mais requiert des solutions de froid solaire résilientes pour la conservation médicale et agroalimentaire.",
        title="Analyse du gradient thermique et des impacts énergétiques",
    )

# ============================================================
# SECTION 5 : FORÊTS ET ZONES PROTÉGÉES
# ============================================================
elif section == "5. Forêts et zones protégées":
    st.header("5. Forêts et zones protégées")
    st.markdown(
        '<div class="section-note">Cartographie interactive et répartition territoriale des 53 forêts classées et zones protégées togolaises soumises aux pressions du prélèvement de bois-énergie.</div>',
        unsafe_allow_html=True,
    )

    regions_list = ["Toutes les régions"] + sorted(df_forets["region"].dropna().unique().tolist())

    col_r1, col_r2 = st.columns(2)
    with col_r1:
        reg_selected = st.selectbox("Filtrer par région administrative", regions_list)
    with col_r2:
        search_txt = st.text_input("Rechercher une zone protégée par son nom", "")

    forets_filtered = df_forets.copy()
    if reg_selected != "Toutes les régions":
        forets_filtered = forets_filtered[forets_filtered["region"] == reg_selected]
    if search_txt.strip():
        forets_filtered = forets_filtered[
            forets_filtered["nom_zone"].str.contains(search_txt.strip(), case=False, na=False)
        ]

    # Métriques synthétiques
    m1, m2, m3 = st.columns(3)
    m1.metric("Zones protégées affichées", len(forets_filtered))
    m2.metric("Régions couvertes", forets_filtered["region"].nunique())
    annees_cr = pd.to_numeric(forets_filtered["annee_creation"], errors="coerce").dropna()
    m3.metric("Création la plus ancienne", int(annees_cr.min()) if not annees_cr.empty else "N/D")

    # Carte Folium
    m_togo = folium.Map(location=[8.6, 1.1], zoom_start=7, tiles="CartoDB positron")
    cluster = MarkerCluster().add_to(m_togo)
    reg_colors = {
        "Maritime": "blue",
        "Plateaux": "green",
        "Centrale": "orange",
        "Kara": "red",
        "Savanes": "purple",
    }

    for _, row in forets_filtered.iterrows():
        if pd.isna(row.get("latitude")) or pd.isna(row.get("longitude")):
            continue
        popup_txt = f"""
        <b>{row.get('nom_zone', 'N/A')}</b><br>
        Région : {row.get('region', 'N/A')}<br>
        Préfecture : {row.get('prefecture', 'N/A')}<br>
        Commune : {row.get('commune', 'N/A')}<br>
        Localité : {row.get('localite', 'N/A')}<br>
        Année de création : {row.get('annee_creation', 'N/A')}
        """
        folium.Marker(
            location=[float(row["latitude"]), float(row["longitude"])],
            popup=popup_txt,
            tooltip=str(row.get("nom_zone", "Zone")),
            icon=folium.Icon(color=reg_colors.get(row.get("region"), "gray"), icon="info-sign"),
        ).add_to(cluster)

    st_folium(m_togo, use_container_width=True, height=520, key="carte_togo_forets")

    # Répartition par région
    c_dist1, c_dist2 = st.columns(2)
    with c_dist1:
        st.subheader("Nombre de zones protégées par région")
        counts_reg = df_forets["region"].value_counts().reset_index()
        counts_reg.columns = ["Région", "Nombre de zones"]
        fig_bar_reg = px.bar(
            counts_reg.sort_values("Nombre de zones", ascending=True),
            x="Nombre de zones",
            y="Région",
            orientation="h",
            text_auto=True,
            color="Nombre de zones",
            color_continuous_scale="Greens",
        )
        fig_bar_reg.update_layout(coloraxis_showscale=False)
        st.plotly_chart(fig_bar_reg, use_container_width=True)

    with c_dist2:
        st.subheader("Inventaire détaillé")
        st.dataframe(
            forets_filtered[["nom_zone", "region", "prefecture", "commune", "annee_creation"]].rename(
                columns={
                    "nom_zone": "Nom de la zone",
                    "region": "Région",
                    "prefecture": "Préfecture",
                    "commune": "Commune",
                    "annee_creation": "Création",
                }
            ),
            use_container_width=True,
            hide_index=True,
        )

    render_analysis_box(
        resultat="Le Togo compte 53 zones protégées et forêts classées enregistrées. La région des Plateaux concentre 20 zones (37,7 % du total national), suivie de la Kara (12 zones), de la Maritime (10 zones), de la Centrale (7 zones) et des Savanes (4 zones).",
        signification="Le patrimoine forestier togolais est fortement concentré le long de l'axe écologique central et méridional. Ces espaces subissent la pression directe du prélèvement de bois et de la carbonisation pour approvisionner les grands marchés urbains (Lomé, Sokodé, Kara).",
        implication="La préservation de ces 53 zones protégées exige la création de périmètres de reboisement dédiés au bois-énergie en périphérie et l'accélération de l'offre en foyers améliorés pour réduire structurellement le prélèvement forestier.",
        title="Analyse spatiale de la protection forestière",
    )

# ============================================================
# SECTION 6 : RECOMMANDATIONS (ICÔNES AUTORISÉES)
# ============================================================
elif section == "6. Recommandations":
    st.header("6. Recommandations stratégiques et opérationnelles")
    st.markdown(
        '<div class="section-note">Les recommandations ci-dessous sont directement adossées aux résultats empiriques issus des données réelles du projet et formulées pour la feuille de route 2026–2030 du Togo.</div>',
        unsafe_allow_html=True,
    )

    r_c1, r_c2 = st.columns(2)
    with r_c1:
        st.markdown(
            """
<div class="recommendation">
    <h3>☀️ 1. Électrification rurale décentralisée</h3>
    <p><b>Justification :</b> L'écart d'accès à l'électricité atteint 71,5 points en 2022 (25,0 % rural vs 96,5 % urbain). L'extension du réseau centralisé est ralentie par les coûts d'infrastructure élevés.</p>
    <p><b>Action clé :</b> Déployer prioritairement des mini-réseaux solaires photovoltaïques hybrides et subventionner les kits solaires certifiés dans les localités rurales isolées.</p>
    <span class="meta-item">📍 <b>Cibles territoriales :</b> Régions des Savanes, Centrale et Plateaux ruraux</span>
</div>
""",
            unsafe_allow_html=True,
        )

    with r_c2:
        st.markdown(
            """
<div class="recommendation">
    <h3>🔥 2. Déploiement massif de la cuisson propre</h3>
    <p><b>Justification :</b> 89,4 % des ménages utilisent le bois et le charbon, et l'accès à la cuisson propre en zone rurale n'est que de 0,90 %.</p>
    <p><b>Action clé :</b> Exonérer de TVA les équipements de gaz GPL, standardiser la production locale de foyers améliorés à haut rendement et initier des digesteurs de biogaz communautaires.</p>
    <span class="meta-item">📍 <b>Cibles territoriales :</b> Périphéries urbaines de Lomé/Kara et zones rurales</span>
</div>
""",
            unsafe_allow_html=True,
        )

    r_c3, r_c4 = st.columns(2)
    with r_c3:
        st.markdown(
            """
<div class="recommendation">
    <h3>🌳 3. Protection forestière et ceintures de bois-énergie</h3>
    <p><b>Justification :</b> Le secteur AFAT génère 87,7 % des émissions de GES nationales, principalement causées par la déforestation et le prélèvement de combustible.</p>
    <p><b>Action clé :</b> Sécuriser les 53 zones protégées (notamment dans les Plateaux - 20 zones et Kara - 12 zones) et créer des plantations de bois-énergie à croissance rapide à exploitation contrôlée.</p>
    <span class="meta-item">📍 <b>Cibles territoriales :</b> Régions des Plateaux, Centrale et Kara</span>
</div>
""",
            unsafe_allow_html=True,
        )

    with r_c4:
        st.markdown(
            """
<div class="recommendation">
    <h3>⚡ 4. Fiabilisation du réseau et productivité économique</h3>
    <p><b>Justification :</b> 93,8 % des entreprises togolaises subissent des coupures d'électricité récurrentes avec une perte de 3,7 % du chiffre d'affaires.</p>
    <p><b>Action clé :</b> Moderniser les sous-stations de distribution, digitaliser la maintenance préventive et raccourcir les délais de raccordement industriel (actuellement 66 jours).</p>
    <span class="meta-item">📍 <b>Cibles territoriales :</b> Pôles économiques de Lomé, Tabligbo et Sokodé</span>
</div>
""",
            unsafe_allow_html=True,
        )

    r_c5, r_c6 = st.columns(2)
    with r_c5:
        st.markdown(
            """
<div class="recommendation">
    <h3>🌱 5. Verdissement du mix de production électrique</h3>
    <p><b>Justification :</b> Les émissions de CO₂ du secteur électrique ont progressé de +142,7 % depuis 2000 avec l'essor de la production thermique.</p>
    <p><b>Action clé :</b> Raccorder de nouvelles centrales solaires photovoltaïques au réseau interconnecté et réhabiliter les petites centrales hydroélectriques pour stabiliser l'approvisionnement propre.</p>
    <span class="meta-item">📍 <b>Cibles territoriales :</b> National (axe Blitta - Sokodé - Mango)</span>
</div>
""",
            unsafe_allow_html=True,
        )

    with r_c6:
        st.markdown(
            """
<div class="recommendation">
    <h3>🌡️ 6. Adaptation climatique et valorisation solaire</h3>
    <p><b>Justification :</b> Les températures maximales moyennes dépassent 35,5 °C dans le Nord (Mango, Dapaong) avec des pointes à 41 °C.</p>
    <p><b>Action clé :</b> Électrifier par pompage solaire les périmètres agricoles irrigués et équiper les centres de santé de climatisation solaire pour sécuriser la chaîne du froid.</p>
    <span class="meta-item">📍 <b>Cibles territoriales :</b> Région des Savanes et Préfecture de l'Oti</span>
</div>
""",
            unsafe_allow_html=True,
        )

    st.subheader("Matrice de priorisation stratégique (2026–2030)")
    priorite_df = pd.DataFrame({
        "Axe stratégique": [
            "Électrification rurale",
            "Cuisson propre",
            "Protection des forêts",
            "Fiabilité du réseau",
            "Énergies renouvelables réseau",
            "Adaptation climatique",
        ],
        "Cible territoriale": [
            "Savanes, Centrale, Plateaux ruraux",
            "National (priorité périurbain et rural)",
            "Plateaux (20 zones), Kara (12 zones)",
            "Pôles industriels et urbains (Lomé)",
            "National (sites solaires de l'axe Nord-Sud)",
            "Région des Savanes (Mango, Dapaong)",
        ],
        "Action prioritaire": [
            "Mini-réseaux et kits solaires autonomes",
            "Subventions GPL et foyers améliorés certifiés",
            "Ceintures de bois-énergie et surveillance communautaire",
            "Réduction des coupures et modernisation du réseau",
            "Extension des centrales solaires raccordées",
            "Pompage solaire agricole et chaîne du froid médicale",
        ],
        "Indicateur d'impact": [
            "Taux d'accès rural (%)",
            "Part des ménages à cuisson propre (%)",
            "Émissions AFAT évitées (Gg CO₂e)",
            "Fréquence des coupures et pertes d'entreprises (%)",
            "Capacité solaire raccordée (MW)",
            "Périmètres irrigués sous pompage solaire (ha)",
        ],
    })
    st.dataframe(priorite_df, use_container_width=True, hide_index=True)

# ============================================================
# SECTION : À PROPOS ET MÉTHODOLOGIE
# ============================================================
else:
    st.header("À propos et méthodologie")
    st.markdown("""
### Cadre analytique
Ce tableau de bord s'inscrit dans le cadre du **Défi 2 — Énergie et Transition écologique au Togo**. Il vise à fournir une vision chiffrée, objective et rigoureuse des dynamiques énergétiques, environnementales et climatiques togolaises.

### Périmètre des données et méthodologie de calcul
- **Accès à l'électricité (1998–2022) :** Suivi des taux d'accès national, rural et urbain. Calcul de l'écart urbain–rural ($Écart = Taux_{Urbain} - Taux_{Rural}$).
- **Fiabilité et climat des affaires :** Indicateurs World Development Indicators (WDI) de la Banque mondiale sur la prévalence des coupures électriques, les pertes sur chiffre d'affaires des entreprises et les délais de connexion.
- **Énergie des ménages et cuisson (2000–2022) :** Analyse de l'évolution de la cuisson propre et ventilation détaillée par type de combustible (bois, charbon de bois, gaz GPL, électricité, biomasse secondaire). Calcul du ratio de dépendance à la biomasse ligneuse solide ($Bois + Charbon$).
- **Émissions de gaz à effet de serre (2018) :** Inventaire national des émissions directes ventilé par secteur économique (AFAT, Énergie, Procédés industriels, Déchets) et par type de gaz ($CO_2$, $CH_4$, $N_2O$).
- **Secteur électrique (1970–2022) :** Trajectoire historique des émissions de dioxyde de carbone ($Mt CO_2e$) issues de la production électrique.
- **Variations climatiques (2013–2019) :** Analyse de 1 680 observations mensuelles sur 10 stations météorologiques togolaises réparties du Sud vers le Nord (Lomé, Tabligbo, Kouma Konda, Atakpamé, Sotouboua, Sokodé, Kara, Niamtougou, Mango, Dapaong).
- **Forêts et zones protégées :** Cartographie géoréférencée des 53 réserves, forêts classées et parcs nationaux du Togo avec ventilation régionale.

### Sources des données
1. **Banque mondiale (World Development Indicators - WDI) :** Séries temporelles d'accès à l'énergie et enquêtes d'entreprises.
2. **Ministère de l'Environnement et des Ressources Forestières du Togo (MERF) :** Inventaire des émissions de GES et cartographie des zones protégées.
3. **Direction Générale de la Météorologie Nationale du Togo :** Relevés de températures mensuelles par station synoptique.
4. **Base de données d'accès à l'énergie de l'OMS / Banque mondiale :** Enquêtes ménages sur les combustibles de cuisson.

### Précisions méthodologiques et limites
Les séries chronologiques possèdent des horizons temporels distincts selon la périodicité des enquêtes nationales. Les indicateurs calculés et visualisations précisent systématiquement l'année de référence associée afin de garantir l'exactitude des comparaisons.
""")

# ============================================================
# PIED DE PAGE (HARMONISÉ AVEC LA SIDEBAR ET LE GRAND TITRE)
# ============================================================
st.markdown(
    """
<div class="custom-footer">
    <p>Défi 2 — Énergie et Transition écologique au Togo</p>
    <span>Tableau de bord d'aide à la décision publique • Données consolidées 2026</span>
</div>
""",
    unsafe_allow_html=True,
)
