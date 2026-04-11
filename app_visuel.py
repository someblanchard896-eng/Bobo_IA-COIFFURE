import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté | L'Excellence par Blanco", page_icon="✨", layout="centered")

# --- L'ALGORITHME DE CONNEXION SÉCURISÉ (STRICTEMENT CONSERVÉ) ---
@st.cache_resource
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        if "gcp_service_account" in st.secrets:
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
            client = gspread.authorize(creds)
            return client.open("Base_Blanco_Beaute").sheet1
        else:
            return "SECRET_MISSING"
    except Exception as e:
        return str(e)

res = connect_to_sheet()

if isinstance(res, str):
    st.error(f"⚠️ Problème de connexion : {res}")
    st.stop()
else:
    sheet = res
    df_salons = pd.DataFrame(sheet.get_all_records())

# --- DESIGN "GLAMOUR & ÉPURE" ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400&family=Poppins:wght@300;400;600&display=swap');

    /* Fond Doux */
    .stApp { background-color: #ffffff; font-family: 'Poppins', sans-serif; }
    
    /* Header Invisible (Pas de rectangle, juste la photo et le texte) */
    .glam-header { 
        background: linear-gradient(rgba(255,255,255,0.1), rgba(255,255,255,0.8)), url('https://images.unsplash.com/photo-1562322140-8baeececf3df?q=80&w=1000&auto=format&fit=crop'); 
        background-size: cover; background-position: center;
        padding: 100px 20px; text-align: center; margin-bottom: 40px; border-radius: 0 0 60px 60px;
    }
    .glam-header h1 { font-family: 'Playfair Display', serif; font-size: 65px !important; color: #d4af37 !important; margin-bottom: 0; font-weight: 700; }
    .glam-header p { font-family: 'Poppins', sans-serif; font-size: 18px; color: #4a3b2a; letter-spacing: 2px; text-transform: uppercase; }

    /* Cartes Salons Style "Instagram" (Sans gros rectangles lourds) */
    .salon-card { 
        background: white; padding: 20px; border-radius: 30px; 
        margin-bottom: 40px; border: none;
        box-shadow: 0 15px 35px rgba(0,0,0,0.05);
        transition: 0.3s ease;
    }
    .salon-card:hover { transform: translateY(-5px); }
    
    /* Titre Salon */
    .salon-name { font-family: 'Playfair Display', serif; color: #1e7e34; font-size: 28px; font-weight: bold; margin-bottom: 15px; text-align: center; }

    /* Bouton Doré Lumineux */
    .stButton>button { 
        border-radius: 50px; background: linear-gradient(45deg, #d4af37, #f1c40f); 
        color: white !important; font-weight: 600; border: none; height: 3.5em; width: 100%; 
        letter-spacing: 1px; transition: 0.4s; box-shadow: 0 10px 20px rgba(212, 175, 55, 0.2);
    }
    .stButton>button:hover { box-shadow: 0 15px 25px rgba(212, 175, 55, 0.4); transform: scale(1.02); }

    /* Inputs élégants */
    .stTextInput>div>div>input { border-radius: 15px; border: 1px solid #f0f0f0; background: #fafafa; }
    
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #fff; border-right: 1px solid #eee; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES QUARTIERS ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin"]

# --- ADMIN ---
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37; font-family:Playfair Display;'>🔱 Espace Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Code Secret", type="password")
    is_admin = (pwd == "Blanco.10")
    if is_admin:
        tab1, tab2 = st.tabs(["Ajouter", "Gérer"])
        with tab1:
            with st.form("ajout"):
                v = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
                q = st.selectbox("Secteur", secteurs_bobo if v == "BOBO-DIOULASSO" else quartiers_ouaga)
                n = st.text_input("Nom du Salon")
                t = st.radio("Type", ["Coiffure", "Institut"], horizontal=True)
                w = st.text_input("WhatsApp")
                ph = st.text_input("Lien Photo")
                vid = st.text_input("Lien Vidéo")
                if st.form_submit_button("PUBLIER"):
                    sheet.append_row([v, q, n, t, w, ph, 0, vid])
                    st.rerun()
        with tab2:
            for idx, row in df_salons.iterrows():
                with st.expander(f"{row['nom du salon']}"):
                    if st.button("🗑️ Supprimer", key=f"del_{idx}"):
                        sheet.delete_rows(idx + 2)
                        st.rerun()

# --- ACCUEIL ---
st.markdown("""
    <div class="glam-header">
        <h1>Faso Beauté</h1>
        <p>L'éclat de votre élégance</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; font-style:italic; color:#888;'>Découvrez les meilleurs soins de Bobo et Ouaga</p>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown('<div class="salon-card">', unsafe_allow_html=True)
        st.markdown(f"<div class='salon-name'>{row['nom du salon'].upper()}</div>", unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 1.5])
        with col_img:
            if row['lien photo']: st.image(row['lien photo'], use_container_width=True)
            if is_admin: st.metric("Gains", f"{row['revenus']} F")
        with col_form:
            st.write(f"✨ **{row['type']}**")
            n_cli = st.text_input("Votre Nom", key=f"n_{idx}", placeholder="Ex: Mme Sawadogo")
            rdv = st.text_input("Heure souhaitée", key=f"t_{idx}", placeholder="Ex: Samedi 14h")
            
            if st.button(f"PRENDRE RENDEZ-VOUS VIP", key=f"b_{idx}"):
                if n_cli and rdv:
                    sheet.update_cell(idx + 2, 7, int(row['revenus']) + 100)
                    msg = urllib.parse.quote(f"Bonjour, réservation pour {n_cli} à {rdv} via Faso Beauté.")
                    url_wa = f"https://wa.me/226{row['whatsapp']}?text={msg}"
                    st.success("Réservation prête !")
                    st.markdown(f'<a href="{url_wa}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:50px; border:none; height:50px; cursor:pointer; font-weight:bold; box-shadow: 0 10px 20px rgba(37, 211, 102, 0.2);">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun salon trouvé dans ce secteur.")

st.markdown("<p style='text-align:center; color:#d4af37; font-size:12px; margin-top:50px;'>Faso Beauté - by Blanco © 2026</p>", unsafe_allow_html=True)
