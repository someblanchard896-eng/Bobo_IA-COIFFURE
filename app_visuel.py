import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd
import time

# --- CONFIGURATION ---
st.set_page_config(page_title="Faso Beauté | Empire Blanco", page_icon="✨", layout="centered")

@st.cache_resource
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        return gspread.authorize(creds).open("Base_Blanco_Beaute").sheet1
    except Exception as e: return str(e)

sheet = connect_to_sheet()
df_salons = pd.DataFrame(sheet.get_all_records())

# --- STYLE CSS (Optimisé Mobile) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .salon-card { border-left: 5px solid #d4af37; padding: 20px; margin-bottom: 25px; box-shadow: 0px 5px 15px rgba(0,0,0,0.05); }
    /* Force la visibilité des placeholders en gris */
    input::placeholder { color: #888888 !important; opacity: 1; }
    .stButton>button { background-color: #000; color: #d4af37 !important; border: 1px solid #d4af37; font-weight: bold; width: 100%; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES QUARTIERS ---
secteurs_bobo = ["Sya", "Koko", "Secteur 3", "Secteur 4", "Secteur 5", "Bolomakoté", "Secteur 7", "Secteur 8", "Accart-ville", "Yéguéré", "Colma", "Secteur 12", "Dogona", "Bindougousso", "Secteur 15", "Secteur 16", "Sarfalao", "Secteur 18", "Secteur 19", "Secteur 20", "Secteur 21", "Secteur 22", "Bobo 2010", "Secteur 24", "Belle-Ville", "Ouezzinville"]
quartiers_ouaga = ["Ouaga 2000", "Karpala", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Balkuy", "Cissin", "Larlé", "Tanghin", "Koulouba", "Wemtenga", "Dapoya", "Paspanga", "Hamdalaye", "Saaba", "Nagrin", "Kamsontenga", "Rimkieta", "Boassa", "Kilwin", "Kamboinssin"]
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# --- SIDEBAR (ESPACE PRO & ADMIN) ---
with st.sidebar:
    st.title("🔱 Menu Empire")
    mode = st.radio("Accès", ["Client", "Admin Empire", "Espace Salon Pro"])
    
    if mode == "Espace Salon Pro":
        st.subheader("🔑 Connexion")
        nom_sel = st.selectbox("Votre Salon", df_salons['nom du salon'])
        user_pwd = st.text_input("Code Secret", type="password")
        
        salon_row = df_salons[df_salons['nom du salon'] == nom_sel].iloc[0]
        if user_pwd != "" and (user_pwd == str(salon_row.get('code_secret', '')) or user_pwd == "Blanco.10"):
            with st.form("update_pro"):
                v = st.text_input("Lien Vidéo", value=salon_row.get('video_url', ''))
                h = st.text_input("Horaires", value=salon_row.get('horaires', ''))
                a = st.text_area("Articles boutique", value=salon_row.get('articles', ''))
                if st.form_submit_button("PUBLIER"):
                    idx_s = df_salons[df_salons['nom du salon'] == nom_sel].index[0] + 2
                    sheet.update_cell(idx_s, 8, v)  # Col H
                    sheet.update_cell(idx_s, 16, h) # Col P
                    sheet.update_cell(idx_s, 17, a) # Col Q
                    st.success("Mise à jour réussie !")
                    st.rerun()

# --- INTERFACE CLIENT ---
st.markdown("<h1 style='text-align:center; color:#d4af37;'>FASO BEAUTÉ</h1>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        sheet_row = idx + 2
        raw_avg = float(row.get('avis_moyenne', 5))
        nb_v = int(row.get('nb_avis', 1))
        
        st.markdown(f'<div class="salon-card"><h3>{row["nom du salon"].upper()} <span style="float:right; font-size:16px; color:#d4af37;">⭐ {raw_avg}/5</span></h3>', unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 1.5])
        with col_img:
            st.image(row['lien photo'] if row['lien photo'] else "https://via.placeholder.com/200")
            if row.get('video_url'): st.video(row['video_url'])

        with col_form:
            st.write(f"🕒 **Horaires :** {row.get('horaires', '08h-20h')}")
            
            # --- ZONE RÉSERVATION AVEC PLACEHOLDERS ---
            n_cli = st.text_input("Votre Nom", placeholder="Entrez votre nom complet", key=f"n_{idx}")
            
            cj, ch = st.columns(2)
            with cj: j_rdv = st.selectbox("Jour souhaité", jours_semaine, key=f"j_{idx}")
            with ch: h_rdv = st.text_input("Heure", placeholder="Ex: 14h30", key=f"h_{idx}")

            # Note client
            u_note = st.feedback("stars", key=f"note_{idx}")
            if u_note is not None:
                nv = u_note + 1
                new_avg = round(((raw_avg * nb_v) + nv) / (nb_v + 1), 1)
                sheet.update_cell(sheet_row, 11, new_avg)
                sheet.update_cell(sheet_row, 12, nb_v + 1)
                st.toast("Note enregistrée !")

            if st.button("RÉSERVER MAINTENANT", key=f"b_{idx}"):
                if n_cli and h_rdv:
                    sheet.update_cell(sheet_row, 7, int(row.get('revenus', 0)) + 100)
                    msg = urllib.parse.quote(f"RDV pour {n_cli} le {j_rdv} à {h_rdv} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; cursor:pointer;">📲 CONFIRMER WHATSAPP</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun salon trouvé dans ce secteur.")
