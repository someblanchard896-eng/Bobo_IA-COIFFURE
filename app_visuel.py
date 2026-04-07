import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté - by Blanco", page_icon="✨", layout="centered")

# --- L'ALGORITHME DE CONNEXION (Celui qui utilise ton Secret JSON) ---
def connect_to_sheet():
    try:
        # On va chercher la clé que tu as mise dans les secrets il y a 4 jours
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        client = gspread.authorize(creds)
        # On ouvre ton fichier par son nom exact
        return client.open("Base_Blanco_Beaute").sheet1
    except Exception as e:
        return None

sheet = connect_to_sheet()

if sheet:
    data = sheet.get_all_records()
    df_salons = pd.DataFrame(data)
else:
    st.error("⚠️ Problème de lecture du Secret JSON. Vérifie que 'gcp_service_account' est toujours dans tes Secrets.")
    st.stop()

# --- DESIGN FASO BEAUTÉ (CONSERVÉ) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .waouh-header { background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1562322140-8baeececf3df?q=80&w=1000&auto=format&fit=crop'); background-size: cover; padding: 50px; border-radius: 0 0 30px 30px; text-align: center; color: #f1c40f; }
    .salon-card { background: #f9f9f9; padding: 20px; border-radius: 20px; border: 1px solid #eee; margin-bottom: 20px; }
    .stButton>button { border-radius: 25px; background: #1e7e34; color: white; font-weight: bold; border: none; height: 3.5em; width: 100%; }
    </style>
    """, unsafe_allow_html=True)

# --- TES LISTES DE QUARTIERS ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin"]

# ==========================================
# 🛡️ ADMINISTRATION (Blanco.10)
# ==========================================
with st.sidebar:
    st.title("🛡️ Espace Blanco")
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
                    st.success("Enregistré dans Google Sheet !")
                    st.rerun()
        with tab2:
            st.subheader("Gestion des Salons")
            for idx, row in df_salons.iterrows():
                with st.expander(f"{row['nom du salon']}"):
                    st.write(f"💰 Gains : {row['revenus']} F")
                    if st.button("🔄 Reset Gains", key=f"res_{idx}"):
                        sheet.update_cell(idx + 2, 7, 0) # Colonne 7 = revenus
                        st.rerun()
                    if st.button("🗑️ Supprimer", key=f"del_{idx}"):
                        sheet.delete_rows(idx + 2)
                        st.rerun()

# ==========================================
# ✨ ACCUEIL CLIENT
# ==========================================
st.markdown('<div class="waouh-header"><h1>Faso Beauté</h1><p style="color:white;">by Blanco</p></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

# Filtrage basé sur tes colonnes de Sheet
results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown('<div class="salon-card">', unsafe_allow_html=True)
        st.subheader(f"⭐ {row['nom du salon'].upper()}")
        col_img, col_form = st.columns([1, 2])
        with col_img:
            if row['lien photo']: st.image(row['lien photo'])
            if is_admin: st.metric("Gains", f"{row['revenus']} F")
        with col_form:
            st.write(f"**{row['type']}** | WhatsApp : {row['whatsapp']}")
            n_cli = st.text_input("Nom", key=f"n_{idx}")
            rdv = st.text_input("Heure", key=f"t_{idx}")
            if st.button(f"🚀 RÉSERVER", key=f"b_{idx}"):
                if n_cli and rdv:
                    # L'algorithme ajoute 100 F dans le Sheet directement
                    nouveau_gain = int(row['revenus']) + 100
                    sheet.update_cell(idx + 2, 7, nouveau_gain)
                    msg = urllib.parse.quote(f"Réservation pour {n_cli} à {rdv} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:45px; cursor:pointer;">📲 WHATSAPP</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
