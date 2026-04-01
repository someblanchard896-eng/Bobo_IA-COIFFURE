import streamlit as st
import urllib.parse
import json
import os
from datetime import datetime

# --- BASE DE DONNÉES PRIVÉE ---
FICHIER_DATA = "data_salons_blanco.json"

def charger_base_de_donnees():
    if os.path.exists(FICHIER_DATA):
        with open(FICHIER_DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    return {
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
        "HISTORIQUE_GAINS": [] # <-- NOUVEAU : Pour le suivi précis
    }

def sauvegarder(data):
    with open(FICHIER_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

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

    liste = [s for s in db["SALONS_ENREGISTRES"] if s['ville'] == v_nom and s['secteur'] == s_nom]
    
    if not liste:
        st.info(f"Aucun salon enregistré à {s_nom} pour le moment.")
    else:
        for i, s in enumerate(liste):
            with st.container(border=True):
                st.subheader(f"💇‍♀️ {s['nom'].upper()}")
                
                # AFFICHAGE IMAGE DIRECTE
                if s.get('image'):
                    st.image(s['image'], use_container_width=True)
                
                # AFFICHAGE VIDÉO / TIKTOK
                if s.get('video'):
                    st.video(s['video'])
                
                st.write(f"💰 Prix moyen : **{s['prix']} FCFA**")
                
                langues = ["Français", "Dioula"] if v_nom == "Bobo-Dioulasso" else ["Français", "Mooré"]
                lang_sel = st.radio(f"Langue du message ({s['nom']})", langues, key=f"lang_{i}", horizontal=True)
                nom_c = st.text_input("Votre Nom complet", key=f"nom_{i}")
                
                if st.button(f"Réserver chez {s['nom']}", key=f"btn_{i}", type="primary"):
                    if nom_c:
                        intro = TEXTES_WA[lang_sel]
                        msg = f"{intro} {nom_c}.\n📍 Secteur : {s_nom}\n💰 Prix : {s['prix']} F\nRéservé via Blanco."
                        link = f"https://wa.me/{s['whatsapp']}?text={urllib.parse.quote(msg)}"
                        
                        # MISE À JOUR DES GAINS AVEC PRÉCISION
                        db["COMMISSIONS_TOTALES"] += 100
                        now = datetime.now().strftime("%d/%m/%Y %H:%M")
                        db["HISTORIQUE_GAINS"].append(f"100 F - Salon {s['nom']} ({now})")
                        sauvegarder(db)
                        
                        st.success("✅ Réservation prête !")
                        st.link_button("🟢 CONFIRMER SUR WHATSAPP", link)
                    else:
                        st.error("Veuillez entrer votre nom.")

elif menu == "🔐 Gestion Privée (Blanco)":
    st.subheader("Accès réservé")
    password_input = st.text_input("Entrez le code secret :", type="password")

    if password_input == "Blanco.10":
        st.success("Bonjour Blanco !")
        col_g1, col_g2 = st.columns(2)
        col_g1.metric("💰 Total des Gains", f"{db['COMMISSIONS_TOTALES']} FCFA")
        
        with col_g2.expander("Détails des gains"):
            if db.get("HISTORIQUE_GAINS"):
                for g in reversed(db["HISTORIQUE_GAINS"]):
                    st.write(f"· {g}")
            else:
                st.write("Aucun gain pour le moment.")
        
        st.markdown("---")
        st.write("### ➕ Ajouter un partenaire & Publicité (Images/Vidéos)")
        with st.form("form_admin", clear_on_submit=True):
            v_a = st.selectbox("Ville ", ["Ouagadougou", "Bobo-Dioulasso"])
            z_a = st.selectbox("Zone ", list(db[v_a].keys()))
            s_a = st.selectbox("Secteur ", db[v_a][z_a])
            nom_s = st.text_input("Nom du Salon")
            prix_s = st.text_input("Prix moyen")
            wa_s = st.text_input("Numéro WhatsApp (226...)")
            
            st.write("🖼️ **Médias du Salon**")
            img_s = st.text_input("Lien de l'IMAGE (ex: lien direct de la coiffure)")
            vid_s = st.text_input("Lien VIDÉO (TikTok ou MP4)")

            if st.form_submit_button("Enregistrer définitivement"):
                if nom_s and wa_s:
                    db["SALONS_ENREGISTRES"].append({
                        "ville": v_a, "secteur": s_a, "nom": nom_s,
                        "prix": prix_s, "whatsapp": wa_s,
                        "image": img_s if img_s else None,
                        "video": vid_s if vid_s else None
                    })
                    sauvegarder(db)
                    st.balloons()
                    st.success(f"Salon {nom_s} ajouté avec succès !")
