import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté - by Blanco", page_icon="✨", layout="centered")

# --- L'ALGORITHME DE CONNEXION (SÉCURISÉ) ---
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        return client.open("Base_Blanco_Beaute").sheet1
    except Exception as e:
        return None

sheet = connect_to_sheet()

if sheet:
    data = sheet.get_all_records()
    df_salons = pd.DataFrame(data)
else:
    st.error("⚠️ Problème de connexion. Vérifiez vos Secrets Streamlit.")
    st.stop()

# --- DESIGN "WAHOU" LUXE LUMINEUX (BLANC, OR & VERT) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #2c3e50; }
    
    /* Header avec dégradé Prestige */
    .waouh-header { 
        background: linear-gradient(135deg, #1e7e34 0%, #d4af37 100%); 
        padding: 60px; 
        border-radius: 0 0 40px 40px; 
        text-align: center; 
        color: white; 
        box-shadow: 0 10px 20px rgba(0,0,0,0.1);
        margin-bottom: 30px;
    }
    .waouh-header h1 { font-size: 55px !important; font-weight: 900 !important; margin: 0; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    
    /* Cartes Salons */
    .salon-card { 
        background: #fdfdfd; 
        padding: 25px; 
        border-radius: 25px; 
        border: 1px solid #f1f1f1; 
        margin-bottom: 25px; 
        box-shadow: 0 8px 15px rgba(0,0,0,0.05); 
    }
    
    /* Bouton Or */
    .stButton>button { 
        border-radius: 30px; 
        background: linear-gradient(45deg, #d4af37, #b8860b); 
        color: white !important; 
        font-weight: bold; 
        border: none; 
        height: 3.5em; 
        width: 100%; 
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(212, 175, 55, 0.4); }

    /* Sidebar Admin */
    [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 2px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- TES LISTES DE QUARTIERS ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Balkuy"]

# ==========================================
# 🛡️ ADMINISTRATION (Blanco.10)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#1e7e34;'>🔱 Bureau Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Code Secret", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
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
                if st.form_submit_button("✅ ENREGISTRER"):
                    sheet.append_row([v, q, n, t, w, ph, 0, vid])
                    st.success("Enregistré dans l'Empire !")
                    st.rerun()
        with tab2:
            st.subheader("Gestion des Salons")
            for idx, row in df_salons.iterrows():
                with st.expander(f"{row['nom du salon']}"):
                    st.write(f"💰 Gains : {row['revenus']} F")
                    if st.button("🔄 Reset Gains", key=f"res_{idx}"):
                        sheet.update_cell(idx + 2, 7, 0)
                        st.rerun()
                    if st.button("🗑️ Supprimer", key=f"del_{idx}"):
                        sheet.delete_rows(idx + 2)
                        st.rerun()

# ==========================================
# ✨ ACCUEIL CLIENT
# ==========================================
st.markdown('<div class="waouh-header"><h1>Faso Beauté</h1><p style="color:white; font-style:italic;">by Blanco</p></div>', unsafe_allow_html=True)

st.markdown("<h4 style='text-align:center;'>Réservez l'excellence pour votre beauté</h4>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

# Filtrage
results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown('<div class="salon-card">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#1e7e34; text-align:center;'>✨ {row['nom du salon'].upper()}</h3>", unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 2])
        with col_img:
            if row['lien photo']: st.image(row['lien photo'], use_container_width=True)
            if is_admin: st.metric("Gains", f"{row['revenus']} F")
        
        with col_form:
            st.write(f"🖋️ **{row['type']}** | WhatsApp : {row['whatsapp']}")
            n_cli = st.text_input("Votre Nom", key=f"n_{idx}", placeholder="Ex: Mme Sawadogo")
            rdv = st.text_input("Jour et Heure", key=f"t_{idx}", placeholder="Ex: Samedi 14h")
            
            if st.button(f"🚀 RÉSERVER MON CRÉNEAU VIP", key=f"b_{idx}"):
                if n_cli and rdv:
                    # Mise à jour des revenus (Colonne 7)
                    nouveau_gain = int(row['revenus']) + 100
                    sheet.update_cell(idx + 2, 7, nouveau_gain)
                    
                    msg = urllib.parse.quote(f"Bonjour, réservation pour {n_cli} à {rdv} via Faso Beauté.")
                    url_wa = f"https://wa.me/226{row['whatsapp']}?text={msg}"
                    
                    st.success("Réservation enregistrée ! +100 F")
                    st.markdown(f'<a href="{url_wa}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:45px; cursor:pointer; font-weight:bold;">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
                else:
                    st.warning("Veuillez remplir le nom et l'heure.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun salon disponible ici. Blanco peut en ajouter dans le menu à gauche.")

st.markdown("<p style='text-align:center; color:gray; font-size:12px; margin-top:50px;'>Faso Beauté - Le Réseau Premium by Blanco © 2026</p>", unsafe_allow_html=True)
