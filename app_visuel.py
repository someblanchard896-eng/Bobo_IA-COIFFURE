import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd
import time

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté | Empire Blanco", page_icon="✨", layout="centered")

@st.cache_resource
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
        return gspread.authorize(creds).open("Base_Blanco_Beaute").sheet1
    except Exception as e: return str(e)

sheet = connect_to_sheet()
data = sheet.get_all_records()
df_salons = pd.DataFrame(data)

# --- SÉCURITÉ DES DONNÉES ---
def safe_int(val):
    try:
        if val == "" or val is None: return 0
        return int(float(str(val).replace(" ", "").replace("F", "")))
    except: return 0

# --- STYLE CSS (Visibilité Maximale) ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; font-family: 'Poppins', sans-serif; }
    .salon-card { border-left: 5px solid #d4af37; padding: 25px; margin-bottom: 30px; box-shadow: 0px 10px 30px rgba(0,0,0,0.05); background: #fff; }
    .stButton>button { background-color: #000 !important; color: #d4af37 !important; border: 1px solid #d4af37 !important; font-weight: bold; width: 100%; height: 3.5em; }
    input::placeholder { color: #888888 !important; opacity: 1; }
    .label-style { font-weight: 600; color: #333; margin-bottom: 5px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES COMPLÈTES ---
secteurs_bobo = ["Sya", "Koko", "Secteur 3", "Secteur 4", "Secteur 5", "Bolomakoté", "Sarfalao", "Secteur 22", "Bobo 2010", "Belle-Ville"]
quartiers_ouaga = ["Ouaga 2000", "Karpala", "Patte d'Oie", "Dassasgho", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Saaba"]
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# --- SIDEBAR : CONTRÔLE TOTAL ---
with st.sidebar:
    st.title("🔱 MENU EMPIRE")
    mode = st.radio("Accès", ["Client", "Admin Empire (Blanco)", "Espace Salon Pro"])
    
    if mode == "Admin Empire (Blanco)":
        master_pwd = st.text_input("Code Maître", type="password")
        if master_pwd == "Blanco.10":
            st.success("👑 Accès Maître")
            t_add, t_fin, t_ia = st.tabs(["➕ Nouveau", "💰 Caisse", "🤖 IA Pub"])
            
            with t_add:
                with st.form("add_form"):
                    v_a = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
                    q_a = st.selectbox("Quartier", secteurs_bobo if v_a == "BOBO-DIOULASSO" else quartiers_ouaga)
                    n_a = st.text_input("Nom du Salon")
                    w_a = st.text_input("WhatsApp")
                    p_a = st.text_input("Photo")
                    c_a = st.text_input("Code Secret Salon")
                    if st.form_submit_button("CRÉER"):
                        sheet.append_row([v_a, q_a, n_a, "Institut", w_a, p_a, 0, "", "", "", 5, 1, "NON", "", "", "", "", c_a])
                        st.rerun()

            with t_fin:
                for i, r in df_salons.iterrows():
                    rev = safe_int(r.get('revenus', 0))
                    if rev > 0:
                        st.write(f"**{r['nom du salon']}** : {rev} F")
                        if st.button(f"Encaisser {r['nom du salon']}", key=f"pay_{i}"):
                            sheet.update_cell(i+2, 7, 0)
                            st.rerun()

            with t_ia:
                s_ia = st.selectbox("Choisir pour la pub", df_salons['nom du salon'])
                if st.button("🤖 GÉNÉRER TEXTE IA"):
                    pub_gen = f"✨ {s_ia} : Le prestige s'installe chez vous ! Profitez d'un accueil d'exception. #FasoBeaute"
                    idx_ia = df_salons[df_salons['nom du salon'] == s_ia].index[0] + 2
                    sheet.update_cell(idx_ia, 15, pub_gen)
                    st.success("Pub générée et publiée !")

    elif mode == "Espace Salon Pro":
        nom_sel = st.selectbox("Salon", df_salons['nom du salon'])
        user_pwd = st.text_input("Code", type="password")
        row_data = df_salons[df_salons['nom du salon'] == nom_sel].iloc[0]
        if user_pwd != "" and (user_pwd == str(row_data.get('code_secret', '')) or user_pwd == "Blanco.10"):
            with st.form("pro_form"):
                v_p = st.text_input("Lien Vidéo", value=row_data.get('video_url', ''))
                h_p = st.text_input("Horaires", value=row_data.get('horaires', ''))
                a_p = st.text_area("Articles & Boutique", value=row_data.get('articles', ''))
                if st.form_submit_button("SAUVEGARDER"):
                    idx_p = df_salons[df_salons['nom du salon'] == nom_sel].index[0] + 2
                    sheet.update_cell(idx_p, 8, v_p)
                    sheet.update_cell(idx_p, 16, h_p)
                    sheet.update_cell(idx_p, 17, a_p)
                    st.success("Modifications enregistrées !")

# --- INTERFACE CLIENT ---
st.markdown("<h1 style='text-align:center; color:#d4af37;'>FASO BEAUTÉ</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with col2: q_c = st.selectbox("🏘️ Secteur", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        sheet_row = idx + 2
        raw_avg = float(row.get('avis_moyenne', 5))
        nb_v = int(row.get('nb_avis', 1))
        
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        st.markdown(f"<h3>{row['nom du salon'].upper()} <span style='float:right; font-size:16px; color:#d4af37;'>⭐ {raw_avg}/5</span></h3>", unsafe_allow_html=True)
        
        c_img, c_form = st.columns([1, 1.2])
        with c_img:
            # Sécurité Image
            photo = row.get('lien photo', '')
            if photo and str(photo).startswith("http"):
                st.image(photo, use_container_width=True)
            else:
                st.image("https://via.placeholder.com/300x200?text=Image+Indisponible", use_container_width=True)
            
            if row.get('articles'):
                with st.expander("🛍️ Boutique"): st.write(row['articles'])
            if row.get('video_url'): st.video(row['video_url'])

        with c_form:
            st.markdown(f"🕒 **Horaires :** {row.get('horaires', '08h-20h')}")
            
            # Formulaire de réservation (Visibilité optimisée)
            st.markdown('<span class="label-style">Votre Nom</span>', unsafe_allow_html=True)
            n_cli = st.text_input("", placeholder="Ex: Mme Sanon", key=f"n_{idx}", label_visibility="collapsed")
            
            cj, ch = st.columns(2)
            with cj:
                st.markdown('<span class="label-style">Jour</span>', unsafe_allow_html=True)
                j_r = st.selectbox("", jours_semaine, key=f"j_{idx}", label_visibility="collapsed")
            with ch:
                st.markdown('<span class="label-style">Heure</span>', unsafe_allow_html=True)
                h_r = st.text_input("", placeholder="14h30", key=f"h_{idx}", label_visibility="collapsed")

            # Note Client
            u_note = st.feedback("stars", key=f"note_{idx}")
            if u_note is not None:
                new_avg = round(((raw_avg * nb_v) + (u_note + 1)) / (nb_v + 1), 1)
                sheet.update_cell(sheet_row, 11, new_avg)
                sheet.update_cell(sheet_row, 12, nb_v + 1)
                st.toast("Note enregistrée !")

            if st.button("RÉSERVER", key=f"b_{idx}"):
                if n_cli and h_r:
                    sheet.update_cell(sheet_row, 7, safe_int(row.get('revenus', 0)) + 100)
                    msg = urllib.parse.quote(f"RDV pour {n_cli} le {j_r} à {h_r} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; cursor:pointer;">📲 CONFIRMER</button></a>', unsafe_allow_html=True)
        
        # Affichage de la pub IA (Rôle rétabli)
        if row.get('pub_ia'):
            st.markdown(f"<div style='background:#fff9e6; padding:10px; border-left:3px solid #d4af37; font-size:13px; margin-top:10px;'>📣 **Note de l'Empire :** {row['pub_ia']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
