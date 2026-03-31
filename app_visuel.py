import streamlit as st
import json
import os
import urllib.parse

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✨", layout="centered")

FICHIER_DATA = "data_salons_blanco.json"

# --- CHARGEMENT DES DONNÉES ---
def charger_data():
    if os.path.exists(FICHIER_DATA):
        with open(FICHIER_DATA, "r", encoding="utf-8") as f:
            return json.load(f)
    # Données par défaut si le fichier n'existe pas
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
        "SALONS": [],
        "GAIN_BLANCO": 0
    }

# --- SAUVEGARDE DES DONNÉES ---
def sauvegarder(data):
    with open(FICHIER_DATA, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# Initialisation des données
data = charger_data()

# --- INTERFACE PRINCIPALE ---
st.title("✨ Blanco Beauté Connect")
st.markdown("---")

# Menu latéral
menu = st.sidebar.selectbox("Menu", ["🏠 Accueil / Réservation", "🔐 Espace Admin (Blanco.10)"])

# --- PARTIE CLIENT : ACCUEIL ---
if menu == "🏠 Accueil / Réservation":
    st.subheader("📍 Trouvez votre salon")
    
    col1, col2 = st.columns(2)
    with col1:
        ville = st.selectbox("Ville", ["Ouagadougou", "Bobo-Dioulasso"])
    with col2:
        zone = st.selectbox("Zone", list(data[ville].keys()))
    
    secteur = st.selectbox("Secteur", data[ville][zone])
    
    st.markdown("---")
    
    # Filtrer les salons du secteur
    salons_dispo = [s for s in data["SALONS"] if s['ville'] == ville and s['secteur'] == secteur]
    
    if not salons_dispo:
        st.warning(f"Aucun salon enregistré à {secteur} pour le moment.")
    else:
        for i, s in enumerate(salons_dispo):
            with st.container():
                st.write(f"### 💇‍♀️ {s['nom']} ({s['type']})")
                st.write(f"💰 Prix : **{s['prix']} FCFA**")
                
                # Options de réservation
                lang_opt = ["Français", "Mooré" if ville=="Ouagadougou" else "Dioula"]
                lang = st.radio(f"Langue pour {s['nom']}", lang_opt, horizontal=True, key=f"lang_{i}")
                
                mariage = st.checkbox("Forfait Marié(e) 💍", key=f"mar_{i}")
                
                nom_c = st.text_input("Votre Nom", key=f"nom_{i}", placeholder="Ex: Adama Traoré")
                date_h = st.text_input("Date & Heure souhaitées", value="Samedi 10h", key=f"date_{i}")
                
                # Bouton de réservation WhatsApp
                if st.button(f"Réserver chez {s['nom']}", key=f"btn_{i}", type="primary"):
                    if nom_c:
                        # Construction du message selon la langue
                        if lang == "Français":
                            intro = "Bonjour,"
                        elif lang == "Dioula":
                            intro = "I ni sogoma,"
                        else: # Mooré
                            intro = "Ne y yibeogo,"
                            
                        type_rdv = "Marié(e)" if mariage else "Simple"
                        
                        msg = f"{intro} réservation via Blanco pour {nom_c}. Type: {s['type']} ({type_rdv}) le {date_h}. Prix: {s['prix']}F."
                        
                        # Création du lien WhatsApp (wa.me)
                        # S'assure que le numéro WhatsApp commence par 226
                        wa_num = s['whatsapp']
                        if not wa_num.startswith('226') and len(wa_num) == 8:
                            wa_num = '226' + wa_num
                            
                        link = f"https://wa.me/{wa_num}?text={urllib.parse.quote(msg)}"
                        
                        # Incrémentation des gains
                        data["GAIN_BLANCO"] += 100
                        sauvegarder(data)
                        
                        st.success("Redirection vers WhatsApp...")
                        st.markdown(f'<meta http-equiv="refresh" content="0;URL={link}">', unsafe_allow_html=True)
                    else:
                        st.error("Veuillez entrer votre nom avant de réserver.")
            st.markdown("---")

# --- PARTIE ADMIN : ESPACE BLANCO ---
elif menu == "🔐 Espace Admin (Blanco.10)":
    st.subheader("Authentification")
    password = st.text_input("Code d'accès", type="password")
    
    if password == "Blanco.10":
        st.success(f"Bienvenue Blanco ! Vos gains totaux sont de : **{data['GAIN_BLANCO']} FCFA** 💸")
        st.markdown("---")
        
        # Le formulaire d'ajout (maintenant bien présent !)
        with st.expander("➕ AJOUTER UN NOUVEAU SALON", expanded=True):
            v_add = st.selectbox("Ville ", ["Ouagadougou", "Bobo-Dioulasso"])
            z_add = st.selectbox("Zone ", list(data[v_add].keys()))
            s_add = st.selectbox("Secteur ", data[v_add][z_add])
            nom_add = st.text_input("Nom du Salon")
            type_add = st.selectbox("Type", ["Coiffure", "Maquillage"])
            prix_add = st.text_input("Prix (en FCFA)")
            wa_add = st.text_input("WhatsApp (ex: 22670000000)")
            
            if st.button("✅ Enregistrer le Salon définitivement"):
                if nom_add and prix_add and wa_add:
                    # Ajout des données
                    data["SALONS"].append({
                        "ville": v_add,
                        "secteur": s_add,
                        "nom": nom_add, 
                        "type": type_add,
                        "prix": prix_add,
                        "whatsapp": wa_add
                    })
                    sauvegarder(data)
                    st.balloons() # Petite animation de succès
                    st.success(f"Salon '{nom_add}' ajouté avec succès ! Actualisez l'Accueil pour le voir.")
                else:
                    st.error("Veuillez remplir le Nom, le Prix et le WhatsApp.")
                    
        # Option pour réinitialiser les gains (cachée en bas)
        with st.expander("🗑️ Zone Danger (Réinitialiser les gains)"):
            if st.button("Mettre les gains à 0 F"):
                data["GAIN_BLANCO"] = 0
                sauvegarder(data)
                st.warning("Gains remis à 0.")
                st.rerun()

    elif password:
        st.error("Code incorrect.")
