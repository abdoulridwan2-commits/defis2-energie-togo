from pathlib import Path

import folium
import pandas as pd
import plotly.express as px
import streamlit as st
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium

# ============================================================
# CONFIGURATION
# ============================================================
st.set_page_config(
    page_title="Énergie & Transition écologique au Togo",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parents[1]
DATA_DIR = BASE_DIR / "data" / "clean"
RAW_DIR = BASE_DIR / "data" / "raw"

# ============================================================
# STYLE
# ============================================================
st.markdown(
    """
<style>
    .main-title {
        padding: 24px 28px;
        border-radius: 16px;
        background: linear-gradient(135deg, #eef8f4 0%, #f7fbff 100%);
        border: 1px solid #d7e8e2;
        margin-bottom: 18px;
    }
    .main-title h1 { margin: 0; font-size: 34px; }
    .main-title p { margin: 8px 0 0 0; color: #52606d; font-size: 16px; }
    .section-note {
        padding: 12px 16px;
        border-left: 4px solid #087f5b;
        background: #f4faf7;
        border-radius: 8px;
        margin: 8px 0 16px 0;
    }
    .insight {
        padding: 15px 18px;
        border-radius: 10px;
        background: #f8fafc;
        border: 1px solid #e5e7eb;
        margin: 8px 0;
    }
    .recommendation {
        padding: 18px;
        border-radius: 12px;
        background: #ffffff;
        border: 1px solid #dfe7e3;
        box-shadow: 0 2px 8px rgba(0,0,0,.04);
        min-height: 180px;
    }
    .small-muted { color: #6b7280; font-size: 13px; }
</style>
""",
    unsafe_allow_html=True,
)

st.markdown(
    """
<div class="main-title">
    <h1>⚡ Énergie & Transition écologique au Togo</h1>
    <p>Électricité • cuisson propre • émissions • climat • énergies renouvelables • forêts protégées</p>
</div>
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
    temp = pd.read_csv(DATA_DIR / "04_temperatures_villes.csv")
    co2 = pd.read_csv(DATA_DIR / "05_co2_secteur_electrique.csv")
    ren = pd.read_csv(DATA_DIR / "06_energies_renouvelables.csv")
    forets = pd.read_csv(DATA_DIR / "07_zones_protegees_forets.csv")

    # Données WDI brutes : utilisées pour compléter l'analyse de fiabilité du réseau
    # et la structure des combustibles de cuisson.
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
# OUTILS
# ============================================================
def latest_value(df, indicator, year_col="annee", value_col="valeur"):
    sub = df[df["indicateur_fr"] == indicator].copy().sort_values(year_col)
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


def insight_box(title, text):
    st.markdown(
        f'<div class="insight"><strong>{title}</strong><br>{text}</div>',
        unsafe_allow_html=True,
    )


# ============================================================
# SIDEBAR : NAVIGATION + FILTRES
# ============================================================
st.sidebar.title("📊 Navigation")
section = st.sidebar.radio(
    "Aller à une section",
    [
        "Vue d'ensemble",
        "1. Accès à l'électricité",
        "2. Énergie des ménages",
        "3. Émissions polluantes",
        "4. Variations climatiques",
        "5. Forêts et zones protégées",
        "6. Recommandations",
        "À propos & méthodologie",
    ],
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔧 Filtres")

all_years = sorted(
    set(pd.to_numeric(df_elec["annee"], errors="coerce").dropna().astype(int))
    | set(pd.to_numeric(df_menage["annee"], errors="coerce").dropna().astype(int))
    | set(pd.to_numeric(df_co2["annee"], errors="coerce").dropna().astype(int))
)
year_max = max(all_years)
year_min = min(all_years)

annee_fin = st.sidebar.selectbox(
    "Année de référence",
    list(range(year_max, year_min - 1, -1)),
    index=0,
)

st.sidebar.caption(f"Année sélectionnée : **{annee_fin}**")
st.sidebar.caption("Les séries historiques conservent leurs années disponibles.")

# ============================================================
# VALEURS CLÉS
# ============================================================
val_nat, year_nat = latest_value(df_elec, "acces_electricite_national_pct")
val_rural, year_rural = latest_value(df_elec, "acces_electricite_rural_pct")
val_urbain, year_urbain = latest_value(df_elec, "acces_electricite_urbain_pct")
val_clean, year_clean = latest_value(df_menage, "acces_cuisson_propre_national_pct")

# ============================================================
# VUE D'ENSEMBLE
# ============================================================
if section == "Vue d'ensemble":
    st.header("🎯 Vue d'ensemble")
    st.markdown(
        '<div class="section-note">Cette vue synthétise les principaux résultats du dashboard et met en évidence les écarts qui doivent guider les décisions publiques.</div>',
        unsafe_allow_html=True,
    )

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("⚡ Accès national", f"{val_nat:.1f}%" if val_nat is not None else "N/D", f"Données {year_nat}")
    k2.metric("🏘️ Accès rural", f"{val_rural:.1f}%" if val_rural is not None else "N/D", f"Données {year_rural}")
    k3.metric("🏙️ Accès urbain", f"{val_urbain:.1f}%" if val_urbain is not None else "N/D", f"Données {year_urbain}")
    k4.metric("🔥 Cuisson propre", f"{val_clean:.1f}%" if val_clean is not None else "N/D", f"Données {year_clean}")

    if val_rural is not None and val_urbain is not None:
        ecart = val_urbain - val_rural
        insight_box(
            "📌 Constat majeur",
            f"L'écart d'accès à l'électricité entre les zones urbaines et rurales atteint <strong>{ecart:.1f} points</strong> dans les dernières données disponibles. La priorité est donc l'électrification décentralisée des villages et localités encore mal desservies.",
        )

    c1, c2 = st.columns(2)
    with c1:
        plot = df_elec[df_elec["indicateur_fr"].isin([
            "acces_electricite_national_pct",
            "acces_electricite_rural_pct",
            "acces_electricite_urbain_pct",
        ])].copy()
        plot["Zone"] = plot["indicateur_fr"].map({
            "acces_electricite_national_pct": "National",
            "acces_electricite_rural_pct": "Rural",
            "acces_electricite_urbain_pct": "Urbain",
        })
        fig = px.line(plot, x="annee", y="valeur", color="Zone", markers=True,
                      title="Accès à l'électricité : évolution nationale, rurale et urbaine",
                      labels={"annee": "Année", "valeur": "Accès (%)"})
        fig.update_layout(legend_title_text="Zone", hovermode="x unified")
        st.plotly_chart(fig, use_container_width=True)

    with c2:
        ren = df_ren.sort_values("annee")
        fig = px.area(ren, x="annee", y="energies_renouvelables_pct",
                      title="Part des énergies renouvelables dans la consommation finale",
                      labels={"annee": "Année", "energies_renouvelables_pct": "Part (%)"})
        st.plotly_chart(fig, use_container_width=True)

    st.subheader("🔎 Trois signaux à retenir")
    a, b, c = st.columns(3)
    with a:
        st.markdown("**⚡ Électrification**")
        st.write("La progression nationale masque un retard rural important. Les solutions hors réseau peuvent accélérer la couverture des villages.")
    with b:
        st.markdown("**🔥 Cuisson**")
        st.write("La dépendance au bois et au charbon reste un enjeu énergétique et environnemental majeur ; les foyers améliorés et combustibles propres sont prioritaires.")
    with c:
        st.markdown("**🌳 Environnement**")
        st.write(f"La base cartographique contient **{len(df_forets)} zones protégées/forêts** à surveiller et à mettre en relation avec les pressions énergétiques locales.")

# ============================================================
# SECTION 1 — ÉLECTRICITÉ
# ============================================================
elif section == "1. Accès à l'électricité":
    st.header("1. ⚡ Accès à l'électricité")
    st.markdown("<div class='section-note'>Comparer les trajectoires urbaines et rurales permet d'identifier où l'effort d'investissement doit être concentré.</div>", unsafe_allow_html=True)

    indicators = [
        "acces_electricite_national_pct",
        "acces_electricite_rural_pct",
        "acces_electricite_urbain_pct",
    ]
    labels = {
        "acces_electricite_national_pct": "National",
        "acces_electricite_rural_pct": "Rural",
        "acces_electricite_urbain_pct": "Urbain",
    }
    plot = df_elec[df_elec["indicateur_fr"].isin(indicators)].copy()
    plot["Zone"] = plot["indicateur_fr"].map(labels)

    f1, f2 = st.columns(2)
    with f1:
        zone_filter = st.multiselect("Zones à comparer", ["National", "Rural", "Urbain"], default=["National", "Rural", "Urbain"])
    with f2:
        min_year = int(plot["annee"].min())
        start_year = st.slider("Début de la période", min_year, int(annee_fin), min_year)

    filtered = plot[(plot["Zone"].isin(zone_filter)) & (plot["annee"] >= start_year) & (plot["annee"] <= annee_fin)]
    fig = px.line(filtered, x="annee", y="valeur", color="Zone", markers=True,
                  title="Évolution de l'accès à l'électricité",
                  labels={"annee": "Année", "valeur": "Accès à l'électricité (%)"})
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    for col, indicator, label in zip([c1, c2, c3], indicators, ["National", "Rural", "Urbain"]):
        sub = df_elec[(df_elec["indicateur_fr"] == indicator) & (df_elec["annee"] <= annee_fin)].sort_values("annee")
        if not sub.empty:
            row = sub.iloc[-1]
            col.metric(label, f"{row['valeur']:.1f}%", f"{int(row['annee'])}")

    if val_rural is not None and val_urbain is not None:
        gap = val_urbain - val_rural
        insight_box("📊 Analyse", f"Le différentiel urbain-rural est de <strong>{gap:.1f} points</strong>. Une stratégie uniforme ne suffirait pas : l'électrification rurale doit privilégier des solutions adaptées à la faible densité et aux coûts de raccordement élevés.")

    st.subheader("⚡ Fiabilité et coût d'accès au réseau")
    outage_indicators = [
        "Firms experiencing electrical outages (% of firms)",
        "Power outages in firms in a typical month (number)",
        "Value lost due to electrical outages (% of sales for affected firms)",
        "Time to obtain an electrical connection (days)",
        "Cost to get electricity connection (% of income per capita)",
    ]
    outage_labels = {
        outage_indicators[0]: "Entreprises touchées par des coupures (%)",
        outage_indicators[1]: "Coupures par mois (nombre)",
        outage_indicators[2]: "Pertes liées aux coupures (% ventes)",
        outage_indicators[3]: "Délai de connexion (jours)",
        outage_indicators[4]: "Coût de connexion (% revenu)",
    }
    rows = []
    for name in outage_indicators:
        value, year = wdi_latest(name)
        if value is not None:
            rows.append({"Indicateur": outage_labels[name], "Valeur": value, "Année": year})
    if rows:
        outage_df = pd.DataFrame(rows)
        st.dataframe(outage_df, use_container_width=True, hide_index=True)
        r1, r2, r3 = st.columns(3)
        if len(outage_df) >= 3:
            r1.metric("Coupures/mois", f"{outage_df.iloc[1]['Valeur']:.1f}", f"{int(outage_df.iloc[1]['Année'])}")
            r2.metric("Entreprises touchées", f"{outage_df.iloc[0]['Valeur']:.1f}%", f"{int(outage_df.iloc[0]['Année'])}")
            r3.metric("Pertes sur ventes", f"{outage_df.iloc[2]['Valeur']:.1f}%", f"{int(outage_df.iloc[2]['Année'])}")
        insight_box("💡 Implication", "L'accès ne se résume pas au raccordement : la qualité du service, le délai et le coût de connexion doivent aussi être améliorés pour que l'électrification produise un bénéfice économique durable.")
    else:
        st.info("Les indicateurs de fiabilité ne sont pas disponibles dans les données brutes chargées.")

# ============================================================
# SECTION 2 — MÉNAGES
# ============================================================
elif section == "2. Énergie des ménages":
    st.header("2. 🔥 Énergie des ménages et cuisson")
    st.markdown("<div class='section-note'>La cuisson propre constitue un levier simultané de santé, de réduction de la pression sur le bois-énergie et de protection des forêts.</div>", unsafe_allow_html=True)

    indicators = [
        "acces_cuisson_propre_national_pct",
        "acces_cuisson_propre_rural_pct",
        "acces_cuisson_propre_urbain_pct",
    ]
    labels = {
        "acces_cuisson_propre_national_pct": "National",
        "acces_cuisson_propre_rural_pct": "Rural",
        "acces_cuisson_propre_urbain_pct": "Urbain",
    }
    plot = df_menage[df_menage["indicateur_fr"].isin(indicators)].copy()
    plot["Zone"] = plot["indicateur_fr"].map(labels)
    selected_zones = st.multiselect("Zones", ["National", "Rural", "Urbain"], default=["National", "Rural", "Urbain"], key="cuisson_zones")
    plot = plot[plot["Zone"].isin(selected_zones)]
    fig = px.line(plot, x="annee", y="valeur", color="Zone", markers=True,
                  title="Évolution de l'accès à la cuisson propre",
                  labels={"annee": "Année", "valeur": "Accès (%)"})
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    # Combustibles à partir des données WDI
    fuel_names = {
        "Main cooking fuel: wood (% of households)": "Bois",
        "Main cooking fuel: charcoal (% of households)": "Charbon",
        "Main cooking fuel: LPG/natural gas/biogas (% of households)": "Gaz / LPG / biogaz",
        "Main cooking fuel: electricity  (% of households)": "Électricité",
        "Main cooking fuel: agricultural crop (% of households)": "Résidus agricoles",
        "Main cooking fuel: straw/shrubs/grass (% of households)": "Paille / broussailles",
        "Main cooking fuel: dung (% of households)": "Bouse",
    }
    fuel_rows = []
    for ind, label in fuel_names.items():
        value, year = wdi_latest(ind)
        if value is not None:
            fuel_rows.append({"Combustible": label, "Part des ménages (%)": value, "Année": year})
    fuel_df = pd.DataFrame(fuel_rows)

    if not fuel_df.empty:
        col1, col2 = st.columns([1.2, 1])
        with col1:
            fig = px.bar(fuel_df.sort_values("Part des ménages (%)"), x="Part des ménages (%)", y="Combustible", orientation="h",
                         title=f"Combustibles principaux de cuisson — dernières données disponibles",
                         labels={"Part des ménages (%)": "Part des ménages (%)"}, text_auto=".1f")
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            st.dataframe(fuel_df.sort_values("Part des ménages (%)", ascending=False), use_container_width=True, hide_index=True)

        bois = fuel_df.loc[fuel_df["Combustible"] == "Bois", "Part des ménages (%)"]
        charbon = fuel_df.loc[fuel_df["Combustible"] == "Charbon", "Part des ménages (%)"]
        if not bois.empty and not charbon.empty:
            combustible_solide = float(bois.iloc[0] + charbon.iloc[0])
            insight_box("🔥 Analyse", f"Le bois et le charbon représentent ensemble environ <strong>{combustible_solide:.1f}%</strong> des ménages dans les dernières observations disponibles. Réduire cette dépendance est directement lié à la protection des ressources forestières.")

# ============================================================
# SECTION 3 — ÉMISSIONS
# ============================================================
elif section == "3. Émissions polluantes":
    st.header("3. 🌍 Bilan des émissions polluantes")
    st.markdown("<div class='section-note'>Le secteur de l'énergie doit être comparé aux autres secteurs afin d'éviter une lecture isolée des émissions.</div>", unsafe_allow_html=True)

    df_secteur = df_emissions[(df_emissions["gaz_code"] == "total") & (df_emissions["secteur_code"] != "total")].copy()
    labels = {
        "energie": "Énergie",
        "procedes_industriels": "Procédés industriels",
        "agriculture_foresterie": "Agriculture & foresterie",
        "dechets": "Déchets",
    }
    df_secteur["Secteur"] = df_secteur["secteur_code"].map(labels)
    df_secteur["Part (%)"] = df_secteur["valeur_Gg"] / df_secteur["valeur_Gg"].sum() * 100

    c1, c2 = st.columns(2)
    with c1:
        fig = px.bar(df_secteur.sort_values("valeur_Gg"), x="valeur_Gg", y="Secteur", orientation="h", text_auto=".0f",
                     title="Émissions de GES par secteur (2018)", labels={"valeur_Gg": "Gg CO₂e"})
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        fig = px.pie(df_secteur, values="valeur_Gg", names="Secteur", hole=.4,
                     title="Contribution relative des secteurs")
        st.plotly_chart(fig, use_container_width=True)

    energie = df_secteur.loc[df_secteur["secteur_code"] == "energie", "Part (%)"]
    if not energie.empty:
        st.metric("Part du secteur énergie", f"{float(energie.iloc[0]):.1f}%", "du total 2018")

    gaz = df_emissions[(df_emissions["secteur_code"] == "energie") & (df_emissions["gaz_code"] != "total")].copy()
    gaz_labels = {"CO2": "CO₂", "CH4": "Méthane (CH₄)", "N2O": "Protoxyde d'azote (N₂O)"}
    gaz["Gaz"] = gaz["gaz_code"].map(gaz_labels)
    fig = px.pie(gaz, values="valeur_Gg", names="Gaz", hole=.4, title="Gaz émis par le secteur de l'énergie")
    st.plotly_chart(fig, use_container_width=True)

    co2 = df_co2.sort_values("annee")
    fig = px.line(co2, x="annee", y="co2_secteur_electrique_MtCO2e", markers=True,
                  title="Évolution des émissions du secteur électrique",
                  labels={"annee": "Année", "co2_secteur_electrique_MtCO2e": "Mt CO₂e"})
    st.plotly_chart(fig, use_container_width=True)

    top_sector = df_secteur.sort_values("valeur_Gg", ascending=False).iloc[0]
    insight_box("📌 Conclusion", f"En 2018, <strong>{top_sector['Secteur']}</strong> est le secteur le plus émetteur dans les données disponibles ({top_sector['valeur_Gg']:.0f} Gg). La transition énergétique doit donc être articulée avec les politiques agricoles, forestières, industrielles et de gestion des déchets.")

# ============================================================
# SECTION 4 — CLIMAT
# ============================================================
elif section == "4. Variations climatiques":
    st.header("4. 🌡️ Variations climatiques : du Sud au Nord")
    st.markdown("<div class='section-note'>Les températures sont comparées sur 10 villes pour visualiser le gradient Sud–Nord et réfléchir aux besoins énergétiques futurs.</div>", unsafe_allow_html=True)

    ordre_villes = ["Lomé", "Tabligbo", "Kouma konda", "Atakpamé", "Sotouboua", "Sokodé", "Kara", "Niamtougou", "Mango", "Dapaong"]
    villes_disponibles = [v for v in ordre_villes if v in df_temp["ville"].unique()]
    ville = st.selectbox("Choisir une ville", villes_disponibles)
    types = st.multiselect("Types de température", sorted(df_temp["type_temp"].unique()), default=sorted(df_temp["type_temp"].unique()), key="temp_types")

    d = df_temp[(df_temp["ville"] == ville) & (df_temp["type_temp"].isin(types))].copy()
    d["date"] = pd.to_datetime(d["annee"].astype(str) + "-" + d["mois"].astype(str) + "-01")
    fig = px.line(d, x="date", y="valeur_celsius", color="type_temp", title=f"Évolution des températures — {ville}",
                  labels={"date": "Date", "valeur_celsius": "Température (°C)", "type_temp": "Type"})
    fig.update_layout(hovermode="x unified")
    st.plotly_chart(fig, use_container_width=True)

    avg = df_temp[df_temp["type_temp"] == "temp_max"].groupby("ville", as_index=False)["valeur_celsius"].mean()
    avg["ville"] = pd.Categorical(avg["ville"], categories=ordre_villes, ordered=True)
    avg = avg.sort_values("ville")
    fig = px.bar(avg, x="ville", y="valeur_celsius", text_auto=".1f",
                 title="Température maximale moyenne — Sud → Nord",
                 labels={"ville": "Ville", "valeur_celsius": "Température maximale moyenne (°C)"})
    st.plotly_chart(fig, use_container_width=True)

    hottest = avg.loc[avg["valeur_celsius"].idxmax()]
    coolest = avg.loc[avg["valeur_celsius"].idxmin()]
    insight_box("🌡️ Analyse", f"Dans la moyenne disponible, <strong>{hottest['ville']}</strong> présente la température maximale moyenne la plus élevée ({hottest['valeur_celsius']:.1f} °C), tandis que <strong>{coolest['ville']}</strong> est la plus basse ({coolest['valeur_celsius']:.1f} °C). Cette variation doit être prise en compte dans le dimensionnement et l'implantation des solutions énergétiques.")

# ============================================================
# SECTION 5 — FORÊTS
# ============================================================
elif section == "5. Forêts et zones protégées":
    st.header("5. 🌳 Forêts et zones protégées")
    st.markdown("<div class='section-note'>La carte localise les zones protégées afin de repérer les espaces naturels à intégrer dans les politiques de transition énergétique et de cuisson propre.</div>", unsafe_allow_html=True)

    regions = ["Toutes"] + sorted(df_forets["region"].dropna().unique().tolist())
    region = st.selectbox("Filtrer par région", regions)
    d = df_forets if region == "Toutes" else df_forets[df_forets["region"] == region]

    k1, k2, k3 = st.columns(3)
    k1.metric("Zones affichées", len(d))
    k2.metric("Régions représentées", d["region"].nunique())
    if "annee_creation" in d:
        years = pd.to_numeric(d["annee_creation"], errors="coerce").dropna()
        k3.metric("Création la plus ancienne", int(years.min()) if not years.empty else "N/D")

    st.caption("💡 Cliquez sur les marqueurs pour consulter le nom, la région, la préfecture et la localité.")
    m = folium.Map(location=[8.6, 1.0], zoom_start=7, tiles="CartoDB positron")
    cluster = MarkerCluster().add_to(m)
    region_colors = {"Maritime": "blue", "Plateaux": "green", "Centrale": "orange", "Kara": "red", "Savanes": "purple"}

    for _, row in d.iterrows():
        if pd.isna(row.get("latitude")) or pd.isna(row.get("longitude")):
            continue
        popup = (
            f"<b>{row['nom_zone']}</b><br>"
            f"Région : {row['region']}<br>"
            f"Préfecture : {row['prefecture']}<br>"
            f"Commune : {row['commune']}<br>"
            f"Localité : {row['localite']}<br>"
            f"Création : {row['annee_creation']}"
        )
        folium.Marker(
            [row["latitude"], row["longitude"]],
            popup=popup,
            tooltip=row["nom_zone"],
            icon=folium.Icon(color=region_colors.get(row["region"], "gray"), icon="leaf"),
        ).add_to(cluster)

    st_folium(m, use_container_width=True, height=560, key="carte_forets_v2")

    counts = df_forets["region"].value_counts().reset_index()
    counts.columns = ["Région", "Nombre de zones"]
    fig = px.bar(counts.sort_values("Nombre de zones"), x="Nombre de zones", y="Région", orientation="h", text_auto=True,
                 title="Répartition des zones protégées par région")
    st.plotly_chart(fig, use_container_width=True)

    insight_box("🌳 Interprétation", "La carte doit servir à cibler les actions : dans les territoires proches des zones protégées, les alternatives au bois-énergie — cuisson propre, foyers améliorés, solaire et autres solutions locales — peuvent réduire la pression sur les ressources forestières.")

# ============================================================
# SECTION 6 — RECOMMANDATIONS
# ============================================================
elif section == "6. Recommandations":
    st.header("6. 💡 Recommandations pratiques")
    st.markdown("<div class='section-note'>Les recommandations ci-dessous sont directement reliées aux constats du dashboard et sont conçues pour être opérationnelles à l'horizon 2030.</div>", unsafe_allow_html=True)

    c1, c2 = st.columns(2)
    with c1:
        st.markdown("""<div class="recommendation"><h3>☀️ 1. Électrifier les villages</h3><p>Déployer des mini-réseaux solaires et des kits solaires dans les localités rurales faiblement couvertes. Prioriser les zones où l'extension du réseau classique est coûteuse.</p><b>Indicateur de suivi :</b> taux d'accès rural.</div>""", unsafe_allow_html=True)
    with c2:
        st.markdown("""<div class="recommendation"><h3>⚡ 2. Améliorer la fiabilité</h3><p>Réduire les coupures, le délai de connexion et le coût du raccordement. L'électrification doit être mesurée par la qualité du service, pas uniquement par le nombre de raccordements.</p><b>Indicateurs :</b> coupures/mois, pertes économiques, délai de connexion.</div>""", unsafe_allow_html=True)

    c3, c4 = st.columns(2)
    with c3:
        st.markdown("""<div class="recommendation"><h3>🔥 3. Accélérer la cuisson propre</h3><p>Subventionner les foyers améliorés et les solutions LPG/biogaz, accompagner les ménages ruraux et développer des filières locales de cuisson propre.</p><b>Indicateur :</b> part des ménages utilisant une cuisson propre.</div>""", unsafe_allow_html=True)
    with c4:
        st.markdown("""<div class="recommendation"><h3>🌳 4. Protéger les forêts</h3><p>Concentrer la surveillance et le reboisement autour des zones protégées vulnérables et réduire la demande de bois-énergie grâce aux alternatives propres.</p><b>Indicateurs :</b> zones surveillées, reboisement, consommation de bois.</div>""", unsafe_allow_html=True)

    c5, c6 = st.columns(2)
    with c5:
        st.markdown("""<div class="recommendation"><h3>🌱 5. Développer les renouvelables</h3><p>Accroître les investissements dans le solaire et les solutions décentralisées, particulièrement adaptées à certaines zones rurales.</p><b>Indicateur :</b> part des énergies renouvelables.</div>""", unsafe_allow_html=True)
    with c6:
        st.markdown("""<div class="recommendation"><h3>🌡️ 6. Anticiper le climat</h3><p>Intégrer les variations de température dans le dimensionnement des infrastructures énergétiques et dans la planification territoriale.</p><b>Indicateur :</b> évolution des températures par ville.</div>""", unsafe_allow_html=True)

    st.subheader("🎯 Priorités 2026–2030")
    priorities = pd.DataFrame({
        "Priorité": ["Électrification rurale", "Cuisson propre", "Fiabilité du réseau", "Protection des forêts", "Énergies renouvelables"],
        "Horizon": ["2026–2030"] * 5,
        "Action clé": [
            "Mini-réseaux solaires et kits solaires",
            "Foyers améliorés + LPG/biogaz",
            "Réduire coupures, délais et coûts",
            "Surveillance + alternatives au bois-énergie",
            "Solaire décentralisé et investissements propres",
        ],
    })
    st.dataframe(priorities, use_container_width=True, hide_index=True)

# ============================================================
# À PROPOS & MÉTHODOLOGIE
# ============================================================
else:
    st.header("📘 À propos & méthodologie")
    st.markdown("""
### Problématique
Le Togo ambitionne de garantir l'accès à l'électricité pour tous d'ici 2030, tout en développant les énergies propres et en protégeant son environnement. Le dashboard met en évidence les écarts territoriaux, la dépendance aux combustibles traditionnels, les émissions et la vulnérabilité des espaces forestiers.

### Méthodologie
- **Électricité :** évolution de l'accès national, rural et urbain ; calcul de l'écart urbain-rural.
- **Fiabilité :** exploitation des indicateurs WDI disponibles sur les coupures, les pertes, les délais et le coût de connexion.
- **Ménages :** évolution de la cuisson propre et comparaison des principaux combustibles.
- **Émissions :** comparaison des secteurs et analyse des gaz du secteur énergétique.
- **Climat :** comparaison des températures sur 10 villes du Sud au Nord.
- **Forêts :** cartographie interactive des zones protégées et analyse de leur répartition régionale.
- **Renouvelables :** évolution de leur part dans la consommation finale d'énergie.

### Sources
Les données du projet proviennent principalement des fichiers fournis pour le challenge et des indicateurs de la **Banque mondiale (World Development Indicators)** présents dans le dossier de données.

### Limites
Les années disponibles ne sont pas identiques pour tous les indicateurs. Les comparaisons sont donc faites sur les périodes effectivement couvertes par chaque jeu de données et l'année de référence est affichée lorsque cela est pertinent.
""")

# ============================================================
# FOOTER
# ============================================================
st.markdown("---")
st.markdown(
    '<p class="small-muted" style="text-align:center;">Défi 2 — Énergie & Transition écologique au Togo · Dashboard réalisé par Abdoulaye Ridwan</p>',
    unsafe_allow_html=True,
)
