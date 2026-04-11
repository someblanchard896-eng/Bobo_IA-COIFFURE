import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté - by Blanco", page_icon="✨", layout="centered")

# --- L'ALGORITHME DE CONNEXION SÉCURISÉ (STRICTEMENT IDENTIQUE) ---
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
    st.info("Action : Vérifiez que la première ligne de vos secrets est bien [gcp_service_account]")
    st.stop()
else:
    sheet = res
    df_salons = pd.DataFrame(sheet.get_all_records())

# --- NOUVEAU DESIGN "FIERTÉ DU FASO" (CHALEUREUX & ÉPURÉ) ---
# ON ENLÈVE TOUTE IMAGE ÉTRANGÈRE, ON UTILISE DES COULEURS CHAUDES (TERRE & OR)
st.markdown("""
    <style>
    /* Fond Terre du Burkina / Crème Doux */
    .stApp { background-color: #fdfaf5; color: #4a3b2a; }
    
    /* Header avec Photo Tresses Africaines (100% Local) */
    .waouh-header { 
        background: linear-gradient(rgba(74, 59, 42, 0.4), rgba(74, 59, 42, 0.6)), url('https://images.unsplash.com/photo-1620331713531-50e5606d1945?q=80&w=1000&auto=format&fit=crop'); 
        background-size: cover; 
        background-position: center;
        padding: 80px 20px; 
        border-radius: 0 0 40px 40px; 
        text-align: center; 
        color: white; 
        margin-bottom: 30px;
        box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        border-bottom: 4px solid #d4af37;
    }
    /* Tes Textes Exacts */
    .waouh-header h1 { font-size: 55px !important; font-weight: 900 !important; color: #f1c40f !important; text-shadow: 2px 2px 6px rgba(0,0,0,0.5); margin-bottom: 5px; }
    .waouh-header h3 { font-size: 20px; color: #ffffff; margin-bottom: 10px; font-style: italic; }
    .waouh-header p { font-size: 14px; color: #ffffff; font-weight: bold; margin: 0; }

    /* Cartes Salons Chaleureuses (Gris-Marron très léger) */
    .salon-card { 
        background: #fdfdfd; padding: 25px; border-radius: 25px; 
        border: 1px solid #e9ecef; margin-bottom: 25px; 
        box-shadow: 0 8px 18px rgba(74, 59, 42, 0.05); 
    }
    
    /* Bouton Or (Terre de Sienne) */
    .stButton>button { 
        border-radius: 30px; background: linear-gradient(45deg, #d4af37, #b8860b); 
        color: white !important; font-weight: bold; border: none; height: 3.8em; width: 100%; 
        transition: 0.3s; font-size: 16px;
        box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 8px 20px rgba(212, 175, 55, 0.6); }

    /* Sidebar Admin (Sobre et Claire) */
    [data-testid="stSidebar"] { background-color: #f4eee1; border-right: 2px solid #d4af37; }
    
    /* Petites écritures pour les infos */
    .small-info { font-size: 14px; color: #6c757d; }
    </style>
    """, unsafe_allow_html=True)

# --- TES LISTES DE QUARTIERS (CONSERVÉES) ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Balkuy"]

# ==========================================
# 🛡️ ADMINISTRATION (CODE : Blanco.10) - CONSERVÉ
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>🔱 Bureau Blanco</h2>", unsafe_allow_html=True)
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
                if st.form_submit_button("✅ ENREGISTRER DANS L'EMPIRE"):
                    sheet.append_row([v, q, n, t, w, ph, 0, vid])
                    st.success("Enregistré dans l'Empire !")
                    st.rerun()
        with tab2:
            st.subheader("Gestion des Salons")
            for idx, row in df_salons.iterrows():
                with st.expander(f"{row['nom du salon']}"):
                    st.write(f"💰 Gains cumulés : {row['revenus']} F")
                    c_r1, c_r2 = st.columns(2)
                    if c_r1.button("🔄 Reset Gains", key=f"res_{idx}"):
                        sheet.update_cell(idx + 2, 7, 0)
                        st.rerun()
                    if c_r2.button("🗑️ Supprimer", key=f"del_{idx}"):
                        sheet.delete_rows(idx + 2)
                        st.rerun()

# ==========================================
# ✨ ACCUEIL CLIENT (FASO BEAUTÉ by BLANCO)
# ==========================================
# HEADER IMPACTANT (PHOTO TRESSES + TES TEXTES EXACTS)
st.markdown("""
    <div class="waouh-header">
        <h1>Faso Beauté</h1>
        <h3>Chaque femme une étoile,<br>L'éclat de votre élégance.</h3>
        <p>by Blanco</p>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#888; font-style:italic; margin-top:20px;'>Découvrez les meilleurs soins de Bobo et Ouaga</p>", unsafe_allow_html=True)

# Filtres
c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

# Affichage des salons (Conservé)
results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown('<div class="salon-card">', unsafe_allow_html=True)
        # Titre Vert Burkina (Identité locale)
        st.markdown(f"<h2 style='color:#1e7e34; text-align:center;'>✨ {row['nom du salon'].upper()}</h2>", unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 1.8])
        with col_img:
            if row['lien photo']: st.image(row['lien photo'], use_container_width=True)
            if row['video_url']: st.video(row['video_url'])
            if is_admin: st.metric("Gains", f"{row['revenus']} F")
        
        with col_form:
            st.markdown(f"<p class='small-info'><strong>Prestation :</strong> {row['type']}</p>", unsafe_allow_html=True)
            st.markdown(f"<p class='small-info'><strong>WhatsApp :</strong> {row['whatsapp']}</p>", unsafe_allow_html=True)
            
            # Formulaire (Conservé)
            n_cli = st.text_input("Votre Nom complet", key=f"n_{idx}", placeholder="Ex: Mme Sawadogo")
            rdv = st.text_input("Jour et Heure souhaitée", key=f"t_{idx}", placeholder="Ex: Samedi 14h")
            
            if st.button(f"🚀 RÉSERVER MON CRÉNEAU VIP", key=f"b_{idx}"):
                if n_cli and rdv:
                    # Mise à jour des revenus (Colonne 7) - Algorithme conservé
                    cell_row = idx + 2
                    sheet.update_cell(cell_row, 7, int(row['revenus']) + 100)
                    
                    # WhatsApp
                    msg = urllib.parse.quote(f"Bonjour, je souhaite réserver une séance de {row['type']} le {rdv} pour la cliente {n_cli} via Faso Beauté.")
                    url_wa = f"https://wa.me/226{row['whatsapp']}?text={msg}"
                    
                    st.success("Réservation validée ! +100 F")
                    # WhatsApp Button
                    st.markdown(f'<a href="{url_wa}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:45px; cursor:pointer; font-weight:bold; font-size: 16px;">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
                else:
                    st.warning("⚠️ Veuillez remplir le nom et l'heure pour réserver.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun établissement d'exception trouvé dans ce secteur. L'Administrateur peut en ajouter.")

# Bas de page
st.markdown("<p style='text-align:center; color:#d4af37; font-size:12px; margin-top:50px;'>Faso Beauté - Le Réseau Premium by Blanco © 2026</p>", unsafe_allow_html=True)
