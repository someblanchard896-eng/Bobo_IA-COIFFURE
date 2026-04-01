import streamlit as st
import urllib.parse
import json
import os
from datetime import datetime

# --- BASE DE DONNÉES PRIVÉE ---
FICHIER_DATA = "data_salons_blanco.json"

def charger_base_de_donnees():
    # Structure par défaut (si le fichier est vide ou n'existe pas)
    default_data = {
        "Ouagadougou": {
            "Zone A (Centre/Nord)": ["Koulouba", "Tampouy", "Somgandé", "Tanghin", "Paspanga"],
            "Zone B (Sud/Est)": ["Ouaga 2000", "Patte d'Oie", "Dassasgho", "Wemtenga", "Dagnoën"],
            "Zone C (Ouest)": ["Pissy", "Gounghin", "Larlé", "Cissin", "Rimkieta"]
        },
        "Bobo-Dioulasso": {
            "Zone 1 (Centre/Sya)": ["Secteur 1", "Secteur 2", "Secteur 5", "Secteur 4", "Accart-ville"],
            "Zone 2 (Est/Sud)": ["Secteur 22", "Secteur 25", "Secteur 24", "Secteur 23", "Bolomakoté"],
            "Zone 3 (Nord/Ouest)": ["Belle-Ville", "Secteur 9", "Secteur 15", "Secteur 10", "Kuinima"]
        },
        "SALONS_ENREGISTRES": [],
        "COMMISSIONS_TOTALES": 0,
        "HISTORIQUE_GAINS": []
    }

    if os.path.exists(FICHIER_DATA):
        try:
            with open(FICHIER_DATA, "r", encoding="utf-8") as f:
                data = json.load(f)
                # SÉCURITÉ : On vérifie que chaque tiroir important existe
                for key in ["SALONS_ENREGISTRES", "COMMISSIONS_TOTALES", "HISTORIQUE_GAINS"]:
                    if key not in data:
                        data[key] = default_data[key]
                return data
        except:
            return default_data
    return default_data

def sauvegarder(data):
    with open(FICHIER_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Chargement de la DB avec la nouvelle sécurité
db = charger_base_de_donnees()

# --- TRADUCTIONS (TES SECRETS) ---
TEXTES_WA = {
    "Français": "Bonjour Madame la Directrice, une nouvelle réservation de",
    "Dioula": "I ni sogoma ba, résérvation kura do don ka bò Blanco fè,",
    "Mooré": "Ne y yibeogo maam, tibo-n-taase n yaa Blanco n tooli,"
}

st.title("✨ BLANCO BEAUTÉ CONNECT")

menu = st.sidebar.selectbox("Aller vers...", ["🏠 Accueil Clients", "🔐 Gestion Privée (Blanco)"])

if menu == "🏠 Accueil Clients":
    st.subheader("📍 Trouvez votre salon à proximité")
    v_nom = st.selectbox("Ville", ["Ouagadougou", "Bobo-Dioulasso"])
    z_nom = st.selectbox("Zone", list(db[v_nom].keys()))
    s_nom = st.selectbox("Secteur", db[v_nom][z_nom])

    # La ligne qui posait problème est maintenant sécurisée
    liste = db.get("SALONS_ENREGISTRES", [])
    filtre = [s for s in liste if s.get('ville') == v_nom and s.get('secteur') == s_nom]
    
    if not filtre:
        st.info(f"Aucun salon enregistré à {s_nom} pour le moment.")
    else:
        for i, s in enumerate(filtre):
            with st.container(border=True):
                st.subheader(f"💇‍♀️ {s['nom'].upper()}")
                if s.get('image'): st.image(s['image'], use_container_width=True)
                if s.get('video'): st.video(s['video'])
                st.write(f"💰 Prix moyen : *{s['prix']} FCFA*")
                
                langues = ["Français", "Dioula"] if v_nom == "Bobo-Dioulasso" else ["Français", "Mooré"]
                lang_sel = st.radio(f"Langue", langues, key=f"lang_{i}", horizontal=True)
                nom_c = st.text_input("Votre Nom", key=f"nom_{i}")
                
                if st.button(f"Réserver chez {s['nom']}", key=f"btn_{i}", type="primary"):
                    if nom_c:
                        intro = TEXTES_WA[lang_sel]
                        msg = f"{intro} {nom_c}.\n📍 Secteur : {s_nom}\n💰 Prix : {s['prix']} F\nRéservé via Blanco."
                        link = f"https://wa.me/{s['whatsapp']}?text={urllib.parse.quote(msg)}"
                        db["COMMISSIONS_TOTALES"] += 100
                        db["HISTORIQUE_GAINS"].append(f"100 F - {s['nom']} ({datetime.now().strftime('%d/%m %H:%M')})")
                        sauvegarder(db)
                        st.link_button("🟢 CONFIRMER SUR WHATSAPP", link)

elif menu == "🔐 Gestion Privée (Blanco)":
    password_input = st.text_input("Code secret :", type="password")
    if password_input == "Blanco.10":
        st.metric("💰 Gains", f"{db['COMMISSIONS_TOTALES']} FCFA")
        with st.expander("Détails"):
            for g in reversed(db.get("HISTORIQUE_GAINS", [])): st.write(f"· {g}")
        
        st.write("### ➕ Ajouter un Salon")
        with st.form("admin_form", clear_on_submit=True):
            v = st.selectbox("Ville", ["Ouagadougou", "Bobo-Dioulasso"])
            s = st.selectbox("Secteur", db[v][list(db[v].keys())[0]]) # Simplifié pour le test
            n = st.text_input("Nom")
            p = st.text_input("Prix")
            w = st.text_input("WhatsApp (226...)")
            img = st.text_input("Lien Image")
            vid = st.text_input("Lien Vidéo/TikTok")
            
            if st.form_submit_button("Valider"):
                db["SALONS_ENREGISTRES"].append({"ville":v,"secteur":s,"nom":n,"prix":p,"whatsapp":w,"image":img,"video":vid})
                sauvegarder(db)
                st.success("Enregistré !")
