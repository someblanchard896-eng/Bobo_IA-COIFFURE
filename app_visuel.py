import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd
import time

# --- CONNEXION ---
@st.cache_resource
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        return gspread.authorize(creds).open("Base_Blanco_Beaute").sheet1
    except Exception as e: return str(e)

sheet = connect_to_sheet()
df_salons = pd.DataFrame(sheet.get_all_records())

# --- STYLE CSS ---
st.markdown("<style>.stApp { background-color: #ffffff; } .salon-card { border-left: 5px solid #d4af37; padding: 20px; margin-bottom: 25px; box-shadow: 0px 5px 15px rgba(0,0,0,0.05); }</style>", unsafe_allow_html=True)

# --- SIDEBAR : LE SYSTÈME DE CODES ---
with st.sidebar:
    st.title("🔱 Empire Blanco")
    mode = st.radio("Accès", ["Client", "Admin Empire", "Espace Salon Pro"])
    
    if mode == "Admin Empire":
        master_pwd = st.text_input("Code Maître", type="password")
        if master_pwd == "Blanco.10":
            st.success("Accès Total Activé")
            # Fonctions de gestion financière ici...

    elif mode == "Espace Salon Pro":
        st.subheader("🔑 Connexion Partenaire")
        nom_select = st.selectbox("Sélectionnez votre Salon", df_salons['nom du salon'])
        user_pwd = st.text_input("Votre Code Secret", type="password")
        
        # Récupération des infos du salon
        salon_data = df_salons[df_salons['nom du salon'] == nom_select].iloc[0]
        vrai_code_salon = str(salon_data.get('code_secret', ''))
        
        # VERIFICATION : Code du salon OU Code Maître Blanco
        if user_pwd != "" and (user_pwd == vrai_code_salon or user_pwd == "Blanco.10"):
            st.success(f"Bienvenue, {nom_select}")
            with st.form("update_pro"):
                new_vid = st.text_input("Lien Vidéo (TikTok/Insta)", value=salon_data.get('video_url', ''))
                new_hor = st.text_input("Horaires", value=salon_data.get('horaires', ''))
                new_art = st.text_area("Articles & Boutique", value=salon_data.get('articles', ''))
                
                if st.form_submit_button("SAUVEGARDER LES MODIFICATIONS"):
                    idx_s = df_salons[df_salons['nom du salon'] == nom_select].index[0]
                    row_s = idx_s + 2
                    sheet.update_cell(row_s, 8, new_vid)  # Col H
                    sheet.update_cell(row_s, 16, new_hor) # Col P
                    sheet.update_cell(row_s, 17, new_art) # Col Q
                    st.success("Mises à jour publiées !")
                    st.rerun()
        elif user_pwd != "":
            st.error("Code incorrect. Contactez l'Empire au +226 56114651")

# --- INTERFACE CLIENT (Moyenne & Réservation) ---
st.markdown("<h1 style='text-align:center; color:#d4af37;'>FASO BEAUTÉ</h1>", unsafe_allow_html=True)

v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
# (Note: Tu peux remettre tes listes complètes de quartiers ici)
q_c = st.selectbox("🏘️ Quartier", ["Quartiers..."]) 

results = df_salons[(df_salons['ville'] == v_c)] # Filtre simplifié pour l'exemple

if not results.empty:
    for idx, row in results.iterrows():
        sheet_row = idx + 2
        # CALCUL MOYENNE RÉELLE
        raw_avg = float(row.get('avis_moyenne', 5))
        nb_v = int(row.get('nb_avis', 1))
        
        st.markdown(f'<div class="salon-card"><h3>{row["nom du salon"].upper()} <span style="float:right; font-size:16px;">⭐ {raw_avg}/5</span></h3>', unsafe_allow_html=True)
        
        c_img, c_form = st.columns([1, 1.5])
        with c_img:
            st.image(row['lien photo'] if row['lien photo'] else "https://via.placeholder.com/200")
            if row.get('articles'):
                with st.expander("🛍️ Boutique"): st.write(row['articles'])
            if row.get('video_url'): st.video(row['video_url'])

        with c_form:
            st.write(f"🕒 {row.get('horaires', '08h-20h')}")
            
            # NOTE CLIENT
            u_note = st.feedback("stars", key=f"note_{idx}")
            if u_note is not None:
                n_val = u_note + 1
                new_avg = round(((raw_avg * nb_v) + n_val) / (nb_v + 1), 1)
                sheet.update_cell(sheet_row, 11, new_avg)
                sheet.update_cell(sheet_row, 12, nb_v + 1)
                st.toast("Merci pour votre avis !")

            n_cli = st.text_input("Votre Nom", key=f"n_{idx}")
            col_j, col_h = st.columns(2)
            with col_j: j_rdv = st.selectbox("Jour", ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"], key=f"j_{idx}")
            with col_h: h_rdv = st.text_input("Heure", key=f"h_{idx}")

            if st.button("RÉSERVER", key=f"b_{idx}"):
                sheet.update_cell(sheet_row, 7, int(row.get('revenus', 0)) + 100)
                msg = urllib.parse.quote(f"RDV pour {n_cli} le {j_rdv} à {h_rdv}.")
                st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px;">CONFIRMER</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
