import streamlit as st
import urllib.parse
import json
import os
from datetime import datetime

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté", page_icon="✨")

# --- BASE DE DONNÉES ---
FICHIER_DATA = "data_salons_blanco.json"

def charger_base_de_donnees():
    # Structure de secours
    default = {
        "Ouagadougou": {"Zone A": ["Koulouba"], "Zone B": ["Ouaga 2000"], "Zone C": ["Pissy"]},
        "Bobo-Dioulasso": {"Zone 1": ["Secteur 1"], "Zone 2": ["Secteur 22"], "Zone 3": ["Belle-Ville"]},
        "SALONS_ENREGISTRES": [],
        "COMMISSIONS_TOTALES": 0,
        "HISTORIQUE_GAINS": []
    }
    if os.path.exists(FICHIER_DATA):
        try:
            with open(FICHIER_DATA, "r", encoding="utf-8") as f:
                return json.load(f)
        except:
            return default
    return default

def sauvegarder(data):
    with open(FICHIER_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

db = charger_base_de_donnees()

# --- INTERFACE ---
st.title("✨ BLANCO BEAUTÉ CONNECT")
menu = st.sidebar.selectbox("Menu", ["🏠 Accueil", "🔐 Admin"])

if menu == "🏠 Accueil":
    v_nom = st.selectbox("Ville", ["Ouagadougou", "Bobo-Dioulasso"])
    
    # On s'assure que la ville existe dans la DB pour éviter l'erreur
   # --- NOUVELLE SELECTION DES QUARTIERS ---
   if v_nom == "Bobo-Dioulasso":
            options_bobo = [
                "Secteur 1 (Dioulassoba)", "Secteur 2 (Dogona / Accart-ville)", "Secteur 3 (Tounouma)", 
                "Secteur 4 (Koko)", "Secteur 5 (Kyé)", "Secteur 6 (Koua)", "Secteur 7 (Bolomakoté)", 
                "Secteur 8 (Sikasso-Cira)", "Secteur 9 (Sya/Kuin-Nima)", "Secteur 10 (Accart-ville Nord, Yéguéré)", 
                "Secteur 11 (Colma)", "Secteur 12 (Bolomakoté)", "Secteur 13 (Saint-Étienne)", 
                "Secteur 14 (Bindougousso)", "Secteur 15 (Ouezzin-Ville)", "Secteur 17 (Sarfalao)", 
                "Secteur 21 (Arrond. 7)", "Secteur 22 (Stade Sangoulé Lamizana)", "Secteur 23 (Zone résidentielle)",
                "Secteur 24 (Belle-Ville)", "Secteur 25 (Zone d'extension)", "Secteur 31 (Route de Bama)"
            ]
            s_nom = st.selectbox("Secteur / Quartier à Bobo", options=options_bobo, index=None, placeholder="Tapez ou choisissez...")
        
        else:
            options_ouaga = [
                "Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Patte d'Oie", "Gounghin", 
                "Somgandé", "Karpala", "Cissin", "Larlé", "Koulouba", "Zogona", "Wemtenga",
                "Kalgondin", "Rimkiéta", "Nagrin", "Saaba", "Hamdalaye", "Balkuy"
            ]
            s_nom = st.selectbox("Quartier à Ouaga", options=options_ouaga, index=None, placeholder="Tapez le nom du quartier...")
    else:
        st.error("Données de ville manquantes.")
        st.stop()

    # --- LA CORRECTION MIRACLE ICI ---
    # On utilise .get() pour ne pas planter si la clé n'existe pas
    tous_les_salons = db.get("SALONS_ENREGISTRES", [])
    
    # Filtrage sécurisé
    filtre = []
    for s in tous_les_salons:
        if s.get('ville') == v_nom and s.get('secteur') == s_nom:
            filtre.append(s)
    
    if not filtre:
        st.info(f"Aucun salon à {s_nom}. Blanco doit en ajouter !")
    else:
        for i, s in enumerate(filtre):
            with st.expander(f"💇‍♀️ {s['nom'].upper()} - {s['prix']} F"):
                if s.get('image'): st.image(s['image'])
                if s.get('video'): st.video(s['video'])
                
                nom_c = st.text_input("Ton Nom", key=f"n_{i}")
                if st.button("Réserver via WhatsApp", key=f"b_{i}"):
                    if nom_c:
                        msg = f"Bonjour, réservation de {nom_c} via Blanco."
                        link = f"https://wa.me/{s['whatsapp']}?text={urllib.parse.quote(msg)}"
                        # Mise à jour
                        db["COMMISSIONS_TOTALES"] = db.get("COMMISSIONS_TOTALES", 0) + 100
                        sauvegarder(db)
                        st.link_button("🟢 CONFIRMER", link)

elif menu == "🔐 Admin":
    pwd = st.text_input("Code", type="password")
    if pwd == "Blanco.10":
        st.write(f"### Gains : {db.get('COMMISSIONS_TOTALES', 0)} F")
        with st.form("ajout"):
            v = st.selectbox("Ville", ["Ouagadougou", "Bobo-Dioulasso"])
            z = st.selectbox("Zone", list(db[v].keys()))
            s = st.selectbox("Secteur", db[v][z])
            n = st.text_input("Nom Salon")
            p = st.text_input("Prix")
            w = st.text_input("WhatsApp (226...)")
            img = st.text_input("Lien Photo")
            vid = st.text_input("Lien Vidéo")
            if st.form_submit_button("Ajouter"):
                if "SALONS_ENREGISTRES" not in db: db["SALONS_ENREGISTRES"] = []
                db["SALONS_ENREGISTRES"].append({"ville":v,"secteur":s,"nom":n,"prix":p,"whatsapp":w,"image":img,"video":vid})
                sauvegarder(db)
                st.success("Salon ajouté ! Actualise la page.")
