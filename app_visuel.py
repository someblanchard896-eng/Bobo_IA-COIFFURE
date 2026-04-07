import streamlit as st
import urllib.parse
import pandas as pd

# --- CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Beauté Connect BF", page_icon="✨", layout="centered")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f5f7f9; }
    .stButton>button { width: 100%; border-radius: 10px; height: 3em; background-color: #27ae60; color: white; }
    .caisse { font-size: 24px; font-weight: bold; color: #f1c40f; background-color: #2c3e50; padding: 15px; border-radius: 15px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# --- GESTION DE LA MÉMOIRE (SIMULÉE POUR LE WEB) ---
if 'gains_totaux' not in st.session_state:
    st.session_state.gains_totaux = 0

# --- BASE DE DONNÉES DES QUARTIERS ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma"]
quartiers_ouaga = [
    "Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", 
    "Pissy", "Gounghin", "Somgandé", "Larlé", "Cissin", "Koulouba", "Wemtenga", "Dagnoën", 
    "Zone du Bois", "1200 Logements", "Kamsonghin", "Samandin", "Paspanga", "Ouidi", 
    "Nemnin", "Tanghin", "Zone Industrielle", "Bendogo", "Kalgondin", "Nagrin", "Bassinko", 
    "Kossodo", "Balkuy"
]

# --- TITRE ET CAISSE ---
st.title("✨ BEAUTÉ CONNECT ✨")
st.markdown(f'<div class="caisse">💰 MA CAISSE PATRON : {st.session_state.gains_totaux} F CFA</div>', unsafe_allow_html=True)

# --- NAVIGATION ---
menu = st.sidebar.radio("MENU", ["Réserver un Salon", "Administration"])

if menu == "Réserver un Salon":
    st.subheader("📍 Choisissez votre ville")
    ville = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
    
    if ville == "BOBO-DIOULASSO":
        quartier = st.selectbox("Secteur / Quartier", secteurs_bobo)
    else:
        quartier = st.selectbox("Quartier / Secteur", quartiers_ouaga)

    st.divider()
    
    # Simulation d'un salon pour le test (Tu pourras lier ta base Google Sheets ici plus tard)
    st.info(f"Salons disponibles à {quartier}")
    nom_salon = st.text_input("Nom du Salon (Ex: Touche Magique)")
    type_etab = st.radio("Type", ["Salon de Coiffure", "Institut de Beauté"])
    num_wa = st.text_input("WhatsApp du Salon (ex: 70000000)")

    st.divider()
    st.subheader("📝 Formulaire de Réservation")
    nom_client = st.text_input("Nom de la cliente")
    prestation = st.selectbox("Prestation", ["Coiffure Simple", "Mariage 💍 / Grand Événement"])
    date_heure = st.text_input("Jour et Heure (ex: Samedi 10h)")

    if st.button("🚀 CONFIRMER & ENVOYER (GAGNER 100F)"):
        if nom_client and date_heure and num_wa:
            # Calcul des 100 F
            st.session_state.gains_totaux += 100
            
            # Message WhatsApp Royal
            texte = (f"Bonjour comment allez vous, je veux une réservation pour une {prestation} "
                     f"le {date_heure} pour la cliente {nom_client} via Beauté Connect.")
            
            msg_encoded = urllib.parse.quote(texte)
            # Nettoyage numéro
            num = num_wa.replace(" ", "").replace("+", "")
            num_final = f"226{num}" if not num.startswith("226") else num
            
            wa_link = f"https://wa.me/{num_final}?text={msg_encoded}"
            
            st.success("Félicitations Patron ! 100 F encaissés.")
            st.markdown(f'[📲 Cliquer ici pour ouvrir le WhatsApp du Salon]({wa_link})', unsafe_allow_html=True)
        else:
            st.error("Veuillez remplir toutes les informations !")

elif menu == "Administration":
    st.subheader("🔐 Espace Admin")
    code = st.text_input("Code Secret", type="password")
    if code == "0001":
        st.success("Accès autorisé, Patron.")
        st.write("Ici tu pourras bientôt voir la liste de tous tes partenaires enregistrés.")
        # Ajout d'un bouton pour réinitialiser la caisse si besoin
        if st.button("Réinitialiser la Caisse"):
            st.session_state.gains_totaux = 0
            st.rerun()

st.sidebar.markdown("---")
st.sidebar.write("✉️ Contact Support Patron")
