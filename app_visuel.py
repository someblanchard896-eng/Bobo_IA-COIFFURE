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
# Chargement initial des données
df_salons = pd.DataFrame(sheet.get_all_records())

# --- STYLE CSS PRESTIGE ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; font-family: 'Poppins', sans-serif; }
    .salon-card { border-left: 5px solid #d4af37; padding: 20px; margin-bottom: 25px; box-shadow: 0px 5px 15px rgba(0,0,0,0.05); }
    input::placeholder { color: #888888 !important; }
    .stButton>button { background-color: #000 !important; color: #d4af37 !important; border: 1px solid #d4af37 !important; font-weight: bold; width: 100%; }
    .stTabs [data-baseweb="tab-list"] { gap: 10px; }
    .stTabs [data-baseweb="tab"] { background-color: #f8f8f8; border-radius: 4px; padding: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES ---
secteurs_bobo = ["Sya", "Koko", "Secteur 3", "Secteur 4", "Secteur 5", "Bolomakoté", "Sarfalao", "Secteur 22", "Bobo 2010", "Belle-Ville"]
quartiers_ouaga = ["Ouaga 2000", "Karpala", "Patte d'Oie", "Dassasgho", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Saaba"]
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# --- SIDEBAR : CONTRÔLE DÉBLOQUÉ ---
with st.sidebar:
    st.title("🔱 MENU EMPIRE")
    mode = st.radio("Choisir un accès", ["Client", "Admin Empire (Blanco)", "Espace Salon Pro"])
    
    if mode == "Admin Empire (Blanco)":
        master_pwd = st.text_input("Code Maître", type="password")
        # On vérifie le code maître AVANT d'afficher les onglets
        if master_pwd == "Blanco.10":
            st.success("Accès Maître Confirmé")
            # Les onglets sont placés à l'intérieur de la condition de succès
            tab_add, tab_fin, tab_ia = st.tabs(["➕ Nouveau", "💰 Caisse", "🤖 IA"])
            
            with tab_add:
                with st.form("add_salon_form"):
                    v_a = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
                    q_a = st.selectbox("Quartier", secteurs_bobo if v_a == "BOBO-DIOULASSO" else quartiers_ouaga)
                    n_a = st.text_input("Nom du Salon")
                    w_a = st.text_input("WhatsApp")
                    p_a = st.text_input("Lien Photo")
                    c_a = st.text_input("Code Secret Salon")
                    if st.form_submit_button("PUBLIER LE SALON"):
                        # ville, secteur, nom, type, whatsapp, photo, revenus, video, ph2, ph3, avis, nb_avis, certif, menu, pub_ia, horaires, articles, code_secret
                        sheet.append_row([v_a, q_a, n_a, "Institut", w_a, p_a, 0, "", "", "", 5, 1, "NON", "", "", "", "", c_a])
                        st.success("C'est en ligne !")
            
            with tab_fin:
                st.write("### Revenus en attente")
                for i, r in df_salons.iterrows():
                    rev = r.get('revenus', 0)
                    if rev > 0:
                        st.write(f"**{r['nom du salon']}** : {rev} F")
                        if st.button(f"Encaisser {r['nom du salon']}", key=f"pay_{i}"):
                            sheet.update_cell(i+2, 7, 0)
                            st.rerun()

            with tab_ia:
                s_ia = st.selectbox("Salon à promouvoir", df_salons['nom du salon'])
                input_ia = st.text_area("Texte brut ou lien à intégrer")
                if st.button("🤖 GÉNÉRER & SAUVEGARDER"):
                    idx_ia = df_salons[df_salons['nom du salon'] == s_ia].index[0] + 2
                    pub_gen = f"✨ Découvrez {s_ia} ! Qualité et prestige garantis. #EmpireBlanco"
                    sheet.update_cell(idx_ia, 15, pub_gen) # Colonne O
                    # Si c'est un lien, on le met aussi en colonne H
                    if "http" in input_ia: sheet.update_cell(idx_ia, 8, input_ia)
                    st.success("Mise à jour effectuée !")

    elif mode == "Espace Salon Pro":
        nom_sel = st.selectbox("Sélectionnez votre Salon", df_salons['nom du salon'])
        user_pwd = st.text_input("Votre Code Secret", type="password")
        
        salon_data = df_salons[df_salons['nom du salon'] == nom_sel].iloc[0]
        if user_pwd != "" and (user_pwd == str(salon_data.get('code_secret', '')) or user_pwd == "Blanco.10"):
            with st.form("pro_form"):
                v_pro = st.text_input("Lien Vidéo TikTok", value=salon_data.get('video_url', ''))
                h_pro = st.text_input("Horaires", value=salon_data.get('horaires', ''))
                a_pro = st.text_area("Articles & Prix", value=salon_data.get('articles', ''))
                if st.form_submit_button("SAUVEGARDER"):
                    idx_p = df_salons[df_salons['nom du salon'] == nom_sel].index[0] + 2
                    sheet.update_cell(idx_p, 8, v_pro)
                    sheet.update_cell(idx_p, 16, h_pro)
                    sheet.update_cell(idx_p, 17, a_pro)
                    st.success("C'est enregistré !")

# --- INTERFACE CLIENT ---
st.markdown("<h1 style='text-align:center; color:#d4af37;'>FASO BEAUTÉ</h1>", unsafe_allow_html=True)

col1, col2 = st.columns(2)
with col1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with col2: q_c = st.selectbox("🏘️ Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

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
            if row.get('articles'):
                with st.expander("🛍️ Boutique"): st.write(row['articles'])

        with col_form:
            st.write(f"🕒 **Horaires :** {row.get('horaires', '08h-20h')}")
            n_cli = st.text_input("Votre Nom", placeholder="Entrez votre nom", key=f"n_{idx}")
            cj, ch = st.columns(2)
            with cj: j_rdv = st.selectbox("Jour", jours_semaine, key=f"j_{idx}")
            with ch: h_rdv = st.text_input("Heure", placeholder="Ex: 15h00", key=f"h_{idx}")

            # Note
            u_note = st.feedback("stars", key=f"note_{idx}")
            if u_note is not None:
                new_avg = round(((raw_avg * nb_v) + (u_note + 1)) / (nb_v + 1), 1)
                sheet.update_cell(sheet_row, 11, new_avg)
                sheet.update_cell(sheet_row, 12, nb_v + 1)
                st.toast("Note enregistrée !")

            if st.button("RÉSERVER", key=f"b_{idx}"):
                if n_cli and h_rdv:
                    sheet.update_cell(sheet_row, 7, int(row.get('revenus', 0)) + 100)
                    msg = urllib.parse.quote(f"RDV pour {n_cli} le {j_rdv} à {h_rdv} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; cursor:pointer;">📲 CONFIRMER</button></a>', unsafe_allow_html=True)
        
        if row.get('pub_ia'):
            st.markdown(f"<div style='background:#fff9e6; padding:10px; border-left:3px solid #d4af37; font-size:13px;'>📣 {row['pub_ia']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
