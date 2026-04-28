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
        data = sheet.get_all_records()
        df_salons = pd.DataFrame(data)
    except Exception:
        time.sleep(2)
        df_salons = pd.DataFrame(sheet.get_all_records())

# --- INTERFACE RÉVOLUTION ÉBÈNE ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap');
    .stApp { background-color: #ffffff; font-family: 'Poppins', sans-serif; }
    .main-title { text-align: center; padding: 40px 0 10px 0; }
    .main-title h1 { font-family: 'Playfair Display', serif; font-size: 55px !important; color: #d4af37 !important; margin-bottom: 0px; }
    .main-title p { font-size: 14px; color: #1a1a1a; letter-spacing: 3px; text-transform: uppercase; margin-top: -5px; font-weight: 600; }
    .salon-card { background: #ffffff; padding: 25px; border-left: 5px solid #d4af37; margin-bottom: 35px; box-shadow: 10px 10px 30px rgba(0,0,0,0.03); }
    .salon-name { font-family: 'Playfair Display', serif; color: #000; font-size: 30px; border-bottom: 1px solid #f1f1f1; margin-bottom: 15px; padding-bottom: 10px; }
    .stButton>button { border-radius: 0px; background: #000; color: #d4af37 !important; font-weight: 600; border: 1px solid #d4af37; width: 100%; transition: 0.4s; }
    .stButton>button:hover { background: #d4af37; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES DES QUARTIERS ---
secteurs_bobo = ["Sya", "Koko", "Secteur 3", "Secteur 4", "Secteur 5", "Bolomakoté", "Secteur 22", "Bobo 2010", "Sarfalao", "Belle-Ville"]
quartiers_ouaga = ["Ouaga 2000", "Karpala", "Patte d'Oie", "Dassasgho", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Saaba"]
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# --- ADMINISTRATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>🔱 Empire Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Accès Admin", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if st.button("🔄 Actualiser les données"):
        st.cache_resource.clear()
        st.rerun()

    if is_admin:
        tab1, tab2 = st.tabs(["Ajouter", "Gérer"])
        with tab1:
            v_admin = st.selectbox("Ville cible", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
            q_list_admin = secteurs_bobo if v_admin == "BOBO-DIOULASSO" else quartiers_ouaga
            with st.form("form_add_salon"):
                q_admin = st.selectbox("Choisir le Quartier", q_list_admin)
                n = st.text_input("Nom du Salon")
                t = st.radio("Type", ["Coiffure", "Institut de Beauté"], horizontal=True)
                w = st.text_input("WhatsApp (ex: 56114651)")
                ph = st.text_input("Photo Principale (Lien)")
                vid = st.text_input("Vidéo (Lien)")
                ph2 = st.text_input("Photo Portfolio 2 (Lien)")
                ph3 = st.text_input("Photo Portfolio 3 (Lien)")
                if st.form_submit_button("PUBLIER DANS L'EMPIRE"):
                    if n and w:
                        # On remplit toutes les colonnes : ville, secteur, nom, type, whatsapp, photo, revenus, video, photo2, photo3, avis_moyenne, nb_avis
                        sheet.append_row([v_admin, q_admin, n, t, w, ph, 0, vid, ph2, ph3, 5, 0])
                        st.success(f"{n} est maintenant en ligne !")
                        st.rerun()
        with tab2:
            for idx, row in df_salons.iterrows():
                with st.expander(f"Gérer : {row['nom du salon']}"):
                    if st.button(f"Supprimer", key=f"del_{idx}"):
                        sheet.delete_rows(idx + 2)
                        st.rerun()

# --- ACCUEIL CLIENT ---
st.markdown("""<div class="main-title"><h1>Faso Beauté</h1><p>by Blanco</p></div>""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Localité", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: 
    q_list_client = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Secteur / Quartier", q_list_client)

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        # Calcul des étoiles
        stars = "⭐" * int(row.get('avis_moyenne', 5))
        
        st.markdown(f'''<div class="salon-card"><div style="display:flex; justify-content:space-between;">
                        <div class="salon-name">{row["nom du salon"].upper()}</div>
                        <div style="color:#d4af37;">{stars}</div></div>''', unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 1.3])
        
        with col_img:
            # Affichage Portfolio
            st.image(row['lien photo'] if row['lien photo'] else "https://via.placeholder.com/300", use_container_width=True)
            if row.get('photo_2') or row.get('photo_3'):
                sub1, sub2 = st.columns(2)
                with sub1: 
                    if row.get('photo_2'): st.image(row['photo_2'], use_container_width=True)
                with sub2:
                    if row.get('photo_3'): st.image(row['photo_3'], use_container_width=True)

        with col_form:
            st.write(f"✨ **Spécialité : {row['type']}**")
            n_cli = st.text_input("Votre Nom", key=f"n_{idx}")
            col_j, col_h = st.columns(2)
            with col_j: jour_rdv = st.selectbox("Jour", jours_semaine, key=f"j_{idx}")
            with col_h: rdv_h = st.text_input("Heure", key=f"t_{idx}", placeholder="Ex: 16h00")
            
            if st.button(f"RÉSERVER MON CRÉNEAU", key=f"b_{idx}"):
                if n_cli and rdv_h:
                    # Mise à jour revenus (simulation acompte 100F)
                    sheet.update_cell(idx + 2, 7, int(row.get('revenus', 0)) + 100)
                    msg = urllib.parse.quote(f"Bonjour, réservation pour {n_cli} le {jour_rdv} à {rdv_h} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border:none; height:45px; cursor:pointer; font-weight:bold;">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun salon trouvé dans cette zone.")

st.markdown("<p style='text-align:center; color:#d4af37; font-size:12px;'>Faso Beauté - Excellence Burkinabè © 2026</p>", unsafe_allow_html=True)
