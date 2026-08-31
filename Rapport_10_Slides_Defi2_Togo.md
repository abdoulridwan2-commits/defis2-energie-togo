# Rapport de Présentation (10 Slides) — Défi 2 : Énergie & Transition Écologique au Togo

---

## Slide 1 — Page de Titre
- **Titre principal** : DÉFI 2 — ÉNERGIE & TRANSITION ÉCOLOGIQUE AU TOGO
- **Sous-titre** : Accès à l'électricité, énergies propres et protection des forêts : un tableau de bord décisionnel pour éclairer les politiques publiques.
- **Auteur** : Abdoulaye Ridwan — Licence 2 Géographie
- **Année** : 2026

---

## Slide 2 — Contexte & Problématique
- **Objectif Togo 2030** : Atteindre l'accès universel à l'électricité tout en réduisant l'empreinte carbone et en protégeant les écosystèmes forestiers.
- **Chiffres clés du constat** :
  - **96,5 %** d'accès à l'électricité en milieu urbain (2022) contre **25,0 %** en milieu rural (écart de **71,5 points**).
  - **89,4 %** des ménages togolais dépendent du bois et du charbon pour la cuisson (2017).
- **Le Double Défi** : Accélérer l'électrification des campagnes tout en stoppant la dégradation forestière liée à la cuisson traditionnelle.

---

## Slide 3 — Méthodologie & Sources des Données
- **Sources officielles exploitées** :
  1. *Banque mondiale (WDI)* : Séries temporelles d'accès à l'énergie (1998–2022) et enquêtes de fiabilité (coupures, délais).
  2. *Ministère de l'Environnement (MERF)* : Inventaire national des émissions de GES (2018) et cartographie des 53 zones protégées.
  3. *Météo Togo (DGMN)* : Séries thermiques mensuelles 2013–2019 sur 10 stations synoptiques.
  4. *Base de données OMS / Banque mondiale* : Enquêtes ménages sur les combustibles de cuisson (2000–2022).
- **Stack technique** : Python, Pandas, Streamlit, Plotly, Folium.

---

## Slide 4 — Axe 1 : Accès à l'Électricité
- **Tendance historique (1998–2022)** :
  - Gain national de **+41,9 points** (15,3 % en 1998 $\rightarrow$ 57,2 % en 2022).
  - L'accès rural est passé de 3,1 % à 25,0 % (multiplié par 8).
  - L'accès urbain a atteint la quasi-saturation (96,5 %).
- **Disparité territoriale** : L'écart urbain/rural s'est creusé de 38,1 points en 1998 à **71,5 points en 2022**.
- **Fiabilité** : 93,8 % des entreprises subissent des coupures régulières avec une perte de 3,7 % du chiffre d'affaires.
- **Orientation clé** : Priorité absolue aux concessions de mini-réseaux et kits solaires décentralisés pour le milieu rural.

---

## Slide 5 — Axe 2 : Énergie des Ménages & Cuisson
- **Structure des combustibles de cuisson (2017)** :
  - Bois de chauffe : **51,8 %**
  - Charbon de bois : **37,6 %**
  - Total Biomasse ligneuse solide : **89,4 %**
  - Gaz GPL : **8,8 %** | Électricité : **0,3 %**
- **Accès à la cuisson propre** : Seulement **11,9 %** au niveau national en 2022 (24,15 % en urbain vs **0,90 %** en rural).
- **Enjeu** : Urgence sanitaire (pollution intérieure) et écologique (pression sur les forêts).

---

## Slide 6 — Axe 3 : Bilan des Émissions de GES
- **Répartition sectorielle des émissions directes (2018)** :
  - **AFAT (Agriculture, Foresterie & Terres)** : **35 830 Gg CO₂e (87,73 %)**
  - **Énergie** : **2 518 Gg CO₂e (6,16 %)**
  - **Procédés industriels** : 2 481 Gg (6,07 %) | Déchets : 14 Gg (0,03 %)
- **Profil des gaz** : 99,57 % des émissions de l'AFAT sont sous forme de CO₂ lié au déboisement.
- **Secteur électrique** : Hausse de **+142,7 % depuis 2000** (0,24 Mt CO₂e en 2022), justifiant un verdissement précoce du mix.

---

## Slide 7 — Axe 4 : Variations Climatiques & Gradient Sud-Nord
- **Gradient thermique marqué** :
  - Station la plus chaude : **Mango** (Tmax moyenne **35,5 °C**, pic maximal à **41,0 °C**).
  - Station septentrionale : **Dapaong** (**34,3 °C**, pics à 40 °C).
  - Station d'altitude fraîche : **Kouma Konda** (**29,1 °C**).
  - Côte tempérée : **Lomé** (**32,3 °C**, amplitude modérée de 7,5 °C).
- **Implication énergétique** : Potentiel solaire maximal dans le Nord (Savanes) couplé à des besoins accrus en pompage solaire et chaîne du froid médicale/agricole.

---

## Slide 8 — Axe 5 : Forêts & Espaces Protégés
- **Inventaire territorial (53 zones classées)** :
  - **Plateaux** : 20 zones (37,7 % du total)
  - **Kara** : 12 zones (22,6 %)
  - **Maritime** : 10 zones (18,9 %)
  - **Centrale** : 7 zones (13,2 %)
  - **Savanes** : 4 zones (7,5 %)
- **Nexus Bois-Énergie / Forêts** : Les massifs forestiers des Plateaux et de la Kara approvisionnent les marchés urbains en charbon. Nécessité de créer des ceintures de bois-énergie dédiées.

---

## Slide 9 — Axe 6 : Recommandations Stratégiques 2026–2030
1. **Électrification rurale décentralisée** : Mini-réseaux et kits solaires autonomes (*Cible : Savanes, Centrale, Plateaux ruraux*).
2. **Cuisson propre à grande échelle** : Exonération de TVA sur le GPL, foyers améliorés certifiés (*Cible : Périurbain et rural*).
3. **Protection forestière communautaire** : Plantations de bois-énergie à croissance rapide (*Cible : Plateaux et Kara*).
4. **Fiabilité et digitalisation du réseau** : Réduction des coupures industrielles (*Cible : Pôles économiques de Lomé et Tabligbo*).
5. **Accélération des renouvelables réseau** : Nouvelles centrales solaires photovoltaïques (*Cible : Axe Nord-Sud*).
6. **Adaptation climatique** : Pompage solaire et réfrigération solaire (*Cible : Région des Savanes*).

---

## Slide 10 — Conclusion & Clôture
- **Synthèse** : La transition écologique au Togo doit concilier rattrapage du retard rural et préservation du capital forestier national.
- **Livrable interactif** : Le tableau de bord Streamlit consolidé offre des filtres dynamiques, une cartographie géoréférencée et des métriques en temps réel pour appuyer la prise de décision.
- **Contact & Soutenance** : *Abdoulaye Ridwan — Défi 2 : Énergie & Transition écologique au Togo*.
