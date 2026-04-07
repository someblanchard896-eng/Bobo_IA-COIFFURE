import streamlit as st
import urllib.parse
import pandas as pd

# --- CONFIGURATION "WAOUH" ---
st.set_page_config(page_title="Beauté Connect - Patron Edition", page_icon="✨", layout="wide")

# --- DESIGN PREMIUM ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 20px; height: 3.5em; background: linear-gradient(45deg, #27ae60, #2ecc71); color: white; font-weight: bold; border: none; }
    .caisse-box { background: #1f2937; padding: 20px; border-radius: 15px; border-left: 5px solid #f1c40f; margin-bottom: 25px; text-align: center; }
    .salon-card { background: #262730; padding: 15px; border-radius: 10px; border: 1px solid #4b5563; margin-bottom: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- MÉMOIRE DES GAINS (100F PAR RÉSA) ---
if 'mon_argent' not in st.session_state:
    st.session_state.mon_argent = 0

# --- BASE DE DONNÉES DES VILLES ET QUARTIERS ---
data_quartiers = {
    "BOBO-DIOULASSO": [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma", "Sya"],
    "OUAGADOUGOU": [
        "Karpala (Secteur 46)", "Ouaga 2000", "Zone 1", "Dassasgho", "Patte d'Oie", "Pissy", "Zogona", 
        "Tampouy", "Gounghin", "Somgandé", "Larlé", "Cissin", "Koulouba", "Wemtenga", "Dagnoën", 
        "Zone du Bois", "1200 Logements", "Kamsonghin", "Samandin", "Paspanga", "Ouidi", "Nemnin", 
        "Tanghin", "Zone Industrielle", "Bendogo", "Kalgondin", "Nagrin", "Bassinko", "Kossodo", "Balkuy"
    ]
}

# --- BARRE LATÉRALE (ADMIN & INFOS) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/3135/3135715.png", width=100)
    st.title("Espace Patron")
    st.markdown(f"### 💰 MA CAISSE\n## {st.session_state.mon_argent} F CFA")
    st.divider()
    admin_code = st.text_input("Code Admin", type="password")
    if st.button("Réinitialiser Caisse") and admin_code == "0001":
        st.session_state.mon_argent = 0
        st.rerun()

# --- CORPS DE L'APPLICATION ---
st.title("✨ BEAUTÉ CONNECT ✨")
st.markdown("*Le réseau n°1 de la coiffure et de la beauté au Burkina Faso*")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("📍 Localisation")
    ville = st.selectbox("Choisir la ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
    quartier = st.selectbox("Choisir le Secteur / Quartier", data_quartiers[ville])
    
    st.subheader("🏢 Établissement")
    type_salon = st.radio("Type d'établissement", ["Salon de Coiffure 💇‍♂️", "Institut de Beauté 💄"], horizontal=True)
    nom_salon = st.text_input("Nom du Salon partenaire")
    wa_salon = st.text_input("WhatsApp du Salon (ex: 70000000)")
    
    st.subheader("📸 Médias (Liens)")
    url_photo = st.text_input("Lien Photo (i.ibb.co)")
    url_video = st.text_input("Lien Vidéo (Streamable/YouTube)")

with col2:
    st.subheader("📅 Détails de la Réservation")
    nom_client = st.text_input("Nom de la cliente")
    prestation = st.selectbox("Type de prestation", ["Coiffure Simple", "Mariage 💍 / Grand Événement"])
    
    # Date et Heure précises
    col_date, col_heure = st.columns(2)
    with col_date:
        jour = st.text_input("Jour (ex: Samedi)")
    with col_heure:
        heure = st.text_input("Heure (ex: 10h30)")

    st.divider()
    
    # --- LE BOUTON MAGIQUE ---
    if st.button("🚀 CONFIRMER LA RÉSERVATION"):
        if nom_client and jour and heure and wa_salon:
            # Crédit de 100F pour le Patron
            st.session_state.mon_argent += 100
            
            # Construction du message Royal
            message_brut = (f"Bonjour comment allez vous, je veux une réservation pour une {prestation} "
                            f"le {jour} à {heure} pour la cliente {nom_client} via Beauté Connect.")
            
            encoded_msg = urllib.parse.quote(message_brut)
            
            # Formatage numéro WhatsApp (+226)
            num_clean = wa_salon.replace(" ", "").replace("+", "")
            num_final = f"226{num_brut}" if not num_brut.startswith("226") else num_brut
            
            wa_link = f"https://wa.me/{num_final}?text={encoded_msg}"
            
            # Affichage Waouh du succès
            st.balloons()
            st.success(f"Réservation confirmée ! Vous avez gagné 100 F CFA.")
            
            # Affichage des médias si présents
            if url_photo: st.image(url_photo, caption="Aperçu du travail")
            if url_video: st.video(url_video)
            
            st.markdown(f'''
                <a href="{wa_link}" target="_blank">
                    <button style="width:100%; height:50px; border-radius:10px; background-color:#25D366; color:white; font-weight:bold; border:none; cursor:pointer;">
                        📲 ENVOYER LE MESSAGE WHATSAPP AU SALON
                    </button>
                </a>
                ''', unsafe_allow_html=True)
        else:
            st.warning("⚠️ Patron, il manque des infos pour valider les 100 F !")

st.divider()
st.caption("Beauté Connect v3.0 - Bobo & Ouaga Network")
