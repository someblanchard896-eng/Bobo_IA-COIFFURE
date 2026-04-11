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
        # Vérification du nom du secret (Assure-toi que c'est bien [gcp_service_account] dans tes Secrets)
        if "gcp_service_account" in st.secrets:
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
            client = gspread.authorize(creds)
            # Ouvre ton fichier par son nom exact
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
    # Lecture des données du Sheet
    df_salons = pd.DataFrame(sheet.get_all_records())

# --- NOUVEAU DESIGN "PRESTIGE" (INSPIRED BY L'ART DE COIFFURE) ---
st.markdown("""
    <style>
    /* Polices de luxe */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap');

    /* Fond Marbre & Épuré */
    .stApp { 
        background-color: #ffffff; 
        background-image: url('https://www.transparenttextures.com/patterns/white-marble.png');
        color: #1a1a1a;
        font-family: 'Poppins', sans-serif;
    }
    
    /* Header invisible avec photo d'entrée (Image 4) */
    .prestige-header { 
        background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url('https://i.ibb.co/vzF4Nqj/entrance.png'); 
        background-size: cover; background-position: center;
        padding: 80px 20px; border-radius: 0 0 50px 50px; text-align: center; color: white; margin-bottom: 40px;
        border-bottom: 3px solid #d4af37;
    }
    .prestige-header h1 { font-family: 'Playfair Display', serif; font-size: 60px !important; color: #d4af37 !important; margin-bottom: 0; }
    .prestige-header p { font-size: 18px; color: #f8f9fa; font-style: italic; }

    /* Cartes Salons Style "Instagram Luxe" */
    .salon-card { 
        background: rgba(255, 255, 255, 0.9); padding: 30px; border-radius: 30px; 
        border: 1px solid #eaeaea; margin-bottom: 30px; 
        box-shadow: 0 15px 35px rgba(0,0,0,0.05); 
        backdrop-filter: blur(5px);
    }
    .salon-name { font-family: 'Playfair Display', serif; color: #1e7e34; font-size: 32px; font-weight: bold; margin-bottom: 15px; }

    /* Bouton Or Prestige */
    .stButton>button { 
        border-radius: 50px; background: linear-gradient(45deg, #d4af37, #b8860b); 
        color: white !important; font-weight: bold; border: none; height: 3.5em; width: 100%; 
        transition: 0.3s; font-size: 16px;
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.3);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(212, 175, 55, 0.5); }

    /* Sidebar Admin (Chaude) */
    [data-testid="stSidebar"] { background-color: #fff; border-right: 2px solid #d4af37; }
    
    /* Petites écritures */
    .small-info { font-size: 14px; color: #6c757d; }
    </style>
    """, unsafe_allow_html=True)

# --- TES LISTES DE QUARTIERS (CONSERVÉES) ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin"]

# ==========================================
# 🛡️ ADMINISTRATION (CODE : Blanco.10) - CONSERVÉ
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37; font-family: Playfair Display;'>🔱 Espace Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Code Secret", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
        st.success("Empire Connecté")
        tab1, tab2 = st.tabs(["➕ Ajouter", "⚙️ Gérer"])
        with tab1:
            with st.form("ajout"):
                v = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
                q = st.selectbox("Secteur", secteurs_bobo if v == "BOBO-DIOULASSO" else quartiers_ouaga)
                n = st.text_input("Nom du Salon")
                t = st.radio("Type", ["Coiffure", "Institut"], horizontal=True)
                w = st.text_input("WhatsApp")
                ph = st.text_input("Lien Photo")
                vid = st.text_input("Lien Vidéo")
                if st.form_submit_button("PUBLIER DANS L'EMPIRE"):
                    sheet.append_row([v, q, n, t, w, ph, 0, vid])
                    st.rerun()
        with tab2:
            st.subheader("Gestion des Salons")
            for idx, row in df_salons.iterrows():
                with st.expander(f"{row['nom du salon']}"):
                    st.write(f"💰 Gains cumulés : {row['revenus']} F")
                    if st.button("🗑️ Supprimer", key=f"del_{idx}"):
                        sheet.delete_rows(idx + 2)
                        st.rerun()

# ==========================================
# ✨ ACCUEIL CLIENT (FASO BEAUTÉ by BLANCO)
# ==========================================
# HEADER IMPACTANT (PHOTO ENTRÉE SALON + TES TEXTES EXACTS)
st.markdown("""
    <div class="prestige-header">
        <h1>Faso Beauté</h1>
        <p>by Blanco</p>
        <div style="background: rgba(255, 255, 255, 0.1); padding: 10px; border-radius: 10px; border: 1px dashed #f1c40f; margin-top: 20px;">
            <p style="font-size: 16px; margin: 0; color: #ffffff;">Chaque femme une étoile,<br>L'éclat de votre élégance.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# Filtres (Conservés)
c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville de recherche", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

# Affichage des salons (Conservé)
results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        # Fond carte avec photo intérieur (Image 5) en surimpression légère
        st.markdown(f'<div class="salon-card" style="background-image: linear-gradient(rgba(255,255,255,0.9), rgba(255,255,255,0.9)), url(\'https://i.ibb.co/q9xYmK0/interior.png\'); background-size: cover;">', unsafe_allow_html=True)
        st.markdown(f"<div class='salon-name'>{row['nom du salon'].upper()}</div>", unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 1.8])
        with col_img:
            if row['lien photo']: st.image(row['lien photo'], use_container_width=True)
            if row['video_url']: st.video(row['video_url'])
            if is_admin: st.metric("Gains", f"{row['revenus']} F")
        
        with col_form:
            st.markdown(f"<p class='small-info'>✨ **{row['type']}**</p>", unsafe_allow_html=True)
            
            # Formulaire (Conservé)
            n_cli = st.text_input("Votre Nom", key=f"n_{idx}", placeholder="Ex: Mme Sawadogo")
            rdv = st.text_input("Heure souhaitée", key=f"t_{idx}", placeholder="Ex: Samedi 14h")
            
            if st.button(f"🚀 RÉSERVER MON CRÉNEAU VIP", key=f"b_{idx}"):
                if n_cli and rdv:
                    # Mise à jour des revenus (Colonne 7) - Algorithme conservé
                    sheet.update_cell(idx + 2, 7, int(row['revenus']) + 100)
                    
                    # WhatsApp
                    msg = urllib.parse.quote(f"Bonjour, réservation pour {n_cli} à {rdv} via Faso Beauté.")
                    url_wa = f"https://wa.me/226{row['whatsapp']}?text={msg}"
                    
                    st.success("Réservation validée !")
                    # WhatsApp Button
                    st.markdown(f'<a href="{url_wa}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:45px; cursor:pointer; font-weight:bold; font-size: 16px;">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Remplissez le nom et l'heure.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun salon trouvé dans ce secteur.")

# Bas de page
st.markdown("<p style='text-align:center; color:#d4af37; font-size:12px; margin-top:50px;'>Faso Beauté - by Blanco © 2026</p>", unsafe_allow_html=True)
