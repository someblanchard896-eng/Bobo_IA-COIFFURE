import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd
import time

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté | Excellence Africaine", page_icon="✨", layout="centered")

# --- L'ALGORITHME DE CONNEXION (SÉCURISÉ) ---
@st.cache_resource
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        if "gcp_service_account" in st.secrets:
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
            client = gspread.authorize(creds)
            return client.open("Base_Blanco_Beaute").sheet1
        else: return "SECRET_MISSING"
    except Exception as e: return str(e)

res = connect_to_sheet()

if isinstance(res, str):
    st.error(f"Connexion interrompue : {res}")
    st.stop()
else:
    sheet = res
    try:
        df_salons = pd.DataFrame(sheet.get_all_records())
    except Exception:
        time.sleep(2)
        df_salons = pd.DataFrame(sheet.get_all_records())

# --- INTERFACE RÉVOLUTION ÉBÈNE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap');
    .stApp { background-color: #ffffff; font-family: 'Poppins', sans-serif; }
    .main-title { text-align: center; padding: 40px 0 10px 0; background: transparent; }
    .main-title h1 { font-family: 'Playfair Display', serif; font-size: 55px !important; color: #d4af37 !important; margin-bottom: 0px; letter-spacing: -1px; }
    .main-title p { font-size: 14px; color: #1a1a1a; letter-spacing: 3px; text-transform: uppercase; margin-top: -5px; font-weight: 600; }
    .slogan-box { text-align: center; margin-bottom: 40px; }
    .slogan-box h3 { font-family: 'Playfair Display', serif; font-style: italic; color: #4a3b2a; font-weight: 400; font-size: 22px; }
    .salon-card { background: #ffffff; padding: 25px; border-radius: 0px; border-left: 5px solid #d4af37; margin-bottom: 35px; box-shadow: 10px 10px 30px rgba(0,0,0,0.03); }
    .salon-name { font-family: 'Playfair Display', serif; color: #000; font-size: 30px; border-bottom: 1px solid #f1f1f1; margin-bottom: 15px; padding-bottom: 10px; }
    .stButton>button { border-radius: 0px; background: #000; color: #d4af37 !important; font-weight: 600; border: 1px solid #d4af37; height: 3.5em; width: 100%; transition: 0.4s; }
    .stButton>button:hover { background: #d4af37; color: #000 !important; }
    .stTextInput>div>div>input, .stSelectbox>div>div>div { border-radius: 0px; border: none; border-bottom: 1px solid #ccc; background: transparent; }
    [data-testid="stSidebar"] { background-color: #f8f8f8; border-right: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES COMPLÈTES (MAILLAGE TERRITORIAL) ---
# Ajout de Bobo 2010 ici
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + [
    "Sarfalao", "Yéguéré", "Accart-ville", "Colma", "Sya", 
    "Bolomakoté", "Belle-Ville", "Dogona", "Bindougousso", "Bobo 2010"
]

quartiers_ouaga = [
    "Ouaga 2000", "Karpala", "Patte d'Oie", "Dassasgho", "Zone 1", 
    "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", 
    "Balkuy", "Cissin", "Larlé", "Tanghin", "Koulouba", 
    "Wemtenga", "Dapoya", "Paspanga", "Hamdalaye", "Saaba", 
    "Nagrin", "Kamsontenga", "Rimkieta", "Boassa", "Kilwin", "Kamboinssin"
]

jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# --- ADMINISTRATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37; font-family:Playfair Display;'>🔱 Empire Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Accès Admin", type="password")
    is_admin = (pwd == "Blanco.10")
    if is_admin:
        tab1, tab2 = st.tabs(["Ajouter", "Gérer"])
        with tab1:
            v_admin = st.selectbox("Ville cible", ["BOBO-DIOULASSO", "OUAGADOUGOU"], key="v_admin_key")
            q_list_admin = secteurs_bobo if v_admin == "BOBO-DIOULASSO" else quartiers_ouaga
            with st.form("form_add_salon"):
                q_admin = st.selectbox("Choisir le Quartier/Secteur", q_list_admin)
                n = st.text_input("Nom du Salon")
                t = st.radio("Type", ["Coiffure", "Institut de Beauté"], horizontal=True)
                w = st.text_input("WhatsApp (ex: 70000000)")
                ph = st.text_input("Lien Photo")
                vid = st.text_input("Lien Vidéo")
                if st.form_submit_button("PUBLIER DANS L'EMPIRE"):
                    if n and w:
                        sheet.append_row([v_admin, q_admin, n, t, w, ph, 0, vid])
                        st.success(f"Enregistré dans {q_admin} !")
                        st.rerun()
                    else:
                        st.warning("⚠️ Nom et WhatsApp requis.")
        with tab2:
            for idx, row in df_salons.iterrows():
                with st.expander(f"{row['nom du salon']}"):
                    if st.button(f"Supprimer définitivement", key=f"del_{idx}"):
                        sheet.delete_rows(idx + 2)
                        st.rerun()

# --- ACCUEIL CLIENT ---
st.markdown("""<div class="main-title"><h1>Faso Beauté</h1><p>by Blanco</p></div><div class="slogan-box"><h3>Chaque femme une étoile,<br>L'éclat de votre élégance.</h3></div>""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Localité", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: 
    q_list_client = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Secteur / Quartier", q_list_client)

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown(f'<div class="salon-card"><div class="salon-name">{row["nom du salon"].upper()}</div>', unsafe_allow_html=True)
        col_img, col_form = st.columns([1, 1.5])
        with col_img:
            if row['lien photo']: st.image(row['lien photo'], use_container_width=True)
            if is_admin: st.metric("Caisse Salon", f"{row['revenus']} F")
        with col_form:
            st.write(f"✨ **Spécialité : {row['type']}**")
            n_cli = st.text_input("Votre Nom", key=f"n_{idx}", placeholder="Ex: Mme Sanon")
            col_j, col_h = st.columns(2)
            with col_j: jour_rdv = st.selectbox("Jour", jours_semaine, key=f"j_{idx}")
            with col_h: rdv_h = st.text_input("Heure", key=f"t_{idx}", placeholder="Ex: 15h30")
            if st.button(f"RÉSERVER MON CRÉNEAU", key=f"b_{idx}"):
                if n_cli and rdv_h:
                    sheet.update_cell(idx + 2, 7, int(row['revenus']) + 100)
                    msg = urllib.parse.quote(f"Bonjour, réservation pour {n_cli} le {jour_rdv} à {rdv_h} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border:none; height:45px; cursor:pointer; font-weight:bold;">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun partenaire d'exception trouvé dans cette zone.")

st.markdown("<p style='text-align:center; color:#d4af37; font-size:12px; margin-top:60px;'>Faso Beauté - Excellence Burkinabè © 2026</p>", unsafe_allow_html=True)
