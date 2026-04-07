import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd

# --- CONFIGURATION HAUTE COUTURE ---
st.set_page_config(page_title="Faso Beauté | L'Excellence par Blanco", page_icon="✨", layout="centered")

# --- CONNEXION ALGORITHME (SECRET JSON) ---
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Base_Blanco_Beaute").sheet1
    except Exception:
        return None

sheet = connect_to_sheet()
if sheet:
    df_salons = pd.DataFrame(sheet.get_all_records())
else:
    st.error("⚠️ Connexion interrompue. Vérifiez vos Secrets Streamlit.")
    st.stop()

# --- DESIGN "WAHOU" BLACK & GOLD ---
st.markdown("""
    <style>
    /* Fond Sombre et Elégant */
    .stApp { background-color: #0b0d11; color: #ffffff; }
    
    /* Header Royal */
    .hero-section {
        background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)), url('https://images.unsplash.com/photo-1560066984-138dadb4c035?q=80&w=1000&auto=format&fit=crop');
        background-size: cover; background-position: center;
        padding: 80px 20px; border-radius: 0 0 50px 50px; text-align: center;
        border-bottom: 3px solid #d4af37; margin-bottom: 40px;
    }
    .hero-section h1 { color: #d4af37 !important; font-size: 60px !important; font-weight: 900 !important; text-shadow: 2px 2px 10px rgba(0,0,0,0.5); margin-bottom: 10px; }
    .hero-section p { font-size: 22px; color: #f8f9fa; font-style: italic; }
    
    /* Boutons Blanco */
    .stButton>button {
        width: 100%; border-radius: 30px; height: 3.8em;
        background: linear-gradient(45deg, #d4af37, #b8860b);
        color: #000000 !important; font-weight: bold; border: none;
        font-size: 18px; box-shadow: 0 4px 15px rgba(212, 175, 55, 0.3);
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.5); }
    
    /* Cartes Salons Luxe */
    .salon-card {
        background: rgba(255, 255, 255, 0.05); padding: 30px; border-radius: 25px;
        border: 1px solid rgba(214, 175, 55, 0.2); margin-bottom: 30px;
        backdrop-filter: blur(10px);
    }
    
    /* Sidebar Admin */
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #d4af37; }
    .stMetric { background: rgba(214, 175, 55, 0.1); padding: 10px; border-radius: 15px; border: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- QUARTIERS ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin"]

# ==========================================
# 🛡️ ESPACE ADMIN (DANS LA SIDEBAR DISCRÈTE)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color: #d4af37;'>🔱 Bureau Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Clé d'accès", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
        st.success("Empire Connecté")
        tab_a, tab_g = st.tabs(["Ajouter", "Gérer"])
        with tab_a:
            with st.form("add"):
                v = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
                q = st.selectbox("Quartier", secteurs_bobo if v == "BOBO-DIOULASSO" else quartiers_ouaga)
                n = st.text_input("Nom du Salon")
                t = st.radio("Type", ["Coiffure", "Institut"], horizontal=True)
                w = st.text_input("WhatsApp")
                ph = st.text_input("URL Photo")
                vid = st.text_input("URL Vidéo")
                if st.form_submit_button("PUBLIER DANS L'EMPIRE"):
                    sheet.append_row([v, q, n, t, w, ph, 0, vid])
                    st.rerun()
        with tab_g:
            for idx, row in df_salons.iterrows():
                st.write(f"**{row['nom du salon']}** ({row['revenus']} F)")
                if st.button("Reset", key=f"rs_{idx}"):
                    sheet.update_cell(idx + 2, 7, 0)
                    st.rerun()
                if st.button("Supprimer", key=f"dp_{idx}"):
                    sheet.delete_rows(idx + 2)
                    st.rerun()

# ==========================================
# ✨ ACCUEIL FASO BEAUTÉ (L'EXPÉRIENCE CLIENT)
# ==========================================

# HEADER IMPACTANT
st.markdown("""
    <div class="hero-section">
        <h1>FASO BEAUTÉ</h1>
        <p>Par Blanco : L'Art de la Beauté Burkinabè à portée de main.</p>
        <br>
        <div style="background: rgba(212, 175, 55, 0.1); padding: 15px; border-radius: 15px; border: 1px dashed #d4af37; margin: 0 50px;">
            <h4 style="color: #d4af37; margin:0;">💎 RÉSERVEZ MAINTENANT</h4>
            <p style="font-size: 14px; margin:0;">Ne perdez plus de temps, les meilleurs salons de Bobo et Ouaga vous attendent.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

# FILTRES DE RECHERCHE
c1, c2 = st.columns(2)
with c1:
    v_c = st.selectbox("📍 Choisissez votre Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2:
    q_list = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Choisissez votre Quartier", q_list)

st.markdown("<br>", unsafe_allow_html=True)

# AFFICHAGE DES SALONS FILTRÉS
results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        
        st.markdown(f"<h2 style='color:#d4af37; text-align:center;'>✨ {row['nom du salon'].upper()} ✨</h2>", unsafe_allow_html=True)
        
        col_m, col_f = st.columns([1, 1.5])
        
        with col_m:
            if row['lien photo']: st.image(row['lien photo'], use_container_width=True)
            if row['video_url']: st.video(row['video_url'])
            if is_admin: st.metric("Gains", f"{row['revenus']} F")
            
        with col_f:
            st.markdown(f"🖋️ **{row['type']}** | 📍 {row['secteur']}")
            st.markdown(f"📱 WhatsApp : {row['whatsapp']}")
            
            with st.container():
                nom_c = st.text_input("Votre Nom", key=f"n_{idx}", placeholder="Ex: Mme Sawadogo")
                presta = st.selectbox("Prestation souhaitée", ["Coiffure Luxe", "Mariage 💍", "Maquillage Pro", "Soins VIP"], key=f"p_{idx}")
                rdv = st.text_input("Jour et Heure", key=f"t_{idx}", placeholder="Ex: Samedi à 14h")
                
                if st.button(f"🚀 RÉSERVER MON CRÉNEAU VIP", key=f"b_{idx}"):
                    if nom_c and rdv:
                        # Update Gains +100
                        new_val = int(row['revenus']) + 100
                        sheet.update_cell(idx + 2, 7, new_val)
                        
                        # WhatsApp Link
                        msg = urllib.parse.quote(f"Bonjour, je souhaite réserver pour une prestation {presta} le {rdv} pour la cliente {nom_c} via Faso Beauté.")
                        wa_url = f"https://wa.me/226{row['whatsapp']}?text={msg}"
                        
                        st.balloons()
                        st.success("Votre demande est prête, Patron !")
                        st.markdown(f'<a href="{wa_url}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:50px; cursor:pointer; font-weight:bold;">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
                    else:
                        st.warning("⚠️ Remplissez votre nom et l'heure pour valider.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown("<p style='text-align:center; color:gray;'>Aucun établissement d'exception trouvé dans ce secteur pour le moment.</p>", unsafe_allow_html=True)

st.markdown("<p style='text-align:center; color:#d4af37; font-size:12px; margin-top:50px;'>Faso Beauté - L'Excellence Burkinabè © 2026 | Powered by Blanco</p>", unsafe_allow_html=True)
