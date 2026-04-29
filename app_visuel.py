import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd
import time

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté | Empire Blanco", page_icon="✨", layout="centered")

# --- CONNEXION SÉCURISÉE ---
@st.cache_resource
def connect_to_sheet():
    try:
        scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
        if "gcp_service_account" in st.secrets:
            creds = Credentials.from_service_account_info(st.secrets["gcp_service_account"], scopes=scope)
            client = gspread.authorize(creds)
            return client.open("Base_Blanco_Beaute").sheet1
        else: return "SECRET_MISSING"
    except Exception as e: return str(e)

res = connect_to_sheet()

if isinstance(res, str):
    st.error(f"Connexion interrompue : {res}")
    st.stop()
else:
    sheet = res
    try:
        df_salons = pd.DataFrame(sheet.get_all_records())
    except Exception:
        time.sleep(2)
        df_salons = pd.DataFrame(sheet.get_all_records())

# --- INTERFACE RÉVOLUTION ÉBÈNE (CSS) ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700&family=Poppins:wght@300;400;600&display=swap');
    .stApp { background-color: #ffffff; font-family: 'Poppins', sans-serif; }
    .main-title { text-align: center; padding: 40px 0 10px 0; }
    .main-title h1 { font-family: 'Playfair Display', serif; font-size: 55px !important; color: #d4af37 !important; margin-bottom: 0px; }
    .salon-card { background: #ffffff; padding: 25px; border-radius: 0px; border-left: 5px solid #d4af37; margin-bottom: 35px; box-shadow: 10px 10px 30px rgba(0,0,0,0.03); }
    .salon-name { font-family: 'Playfair Display', serif; color: #000; font-size: 30px; border-bottom: 1px solid #f1f1f1; margin-bottom: 15px; padding-bottom: 10px; }
    .badge-elite { background-color: #d4af37; color: white; padding: 3px 10px; font-size: 12px; border-radius: 20px; font-weight: bold; margin-left: 10px; }
    .price-tag { color: #1a1a1a; font-weight: 600; font-size: 14px; background: #f8f8f8; padding: 5px 10px; border-radius: 5px; border: 1px solid #eee; display: inline-block; margin-bottom: 10px; }
    .info-box { background: #fff9e6; padding: 15px; border-radius: 5px; font-size: 14px; margin-top: 15px; border-left: 3px solid #d4af37; font-style: italic; }
    .stButton>button { border-radius: 0px; background: #000; color: #d4af37 !important; font-weight: 600; border: 1px solid #d4af37; height: 3.5em; width: 100%; transition: 0.4s; }
    .stButton>button:hover { background: #d4af37; color: #000 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES QUARTIERS COMPLÈTES ---
secteurs_bobo = ["Sya", "Koko", "Secteur 3", "Secteur 4", "Secteur 5", "Bolomakoté", "Secteur 7", "Secteur 8", "Accart-ville", "Yéguéré", "Colma", "Secteur 12", "Dogona", "Bindougousso", "Secteur 15", "Secteur 16", "Sarfalao", "Secteur 18", "Secteur 19", "Secteur 20", "Secteur 21", "Secteur 22", "Bobo 2010", "Secteur 24", "Belle-Ville", "Ouezzinville"]
quartiers_ouaga = ["Ouaga 2000", "Karpala", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Balkuy", "Cissin", "Larlé", "Tanghin", "Koulouba", "Wemtenga", "Dapoya", "Paspanga", "Hamdalaye", "Saaba", "Nagrin", "Kamsontenga", "Rimkieta", "Boassa", "Kilwin", "Kamboinssin"]
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# --- ADMINISTRATION ---
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>🔱 Empire Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Accès Admin", type="password")
    is_admin = (pwd == "Blanco.10")
    if is_admin:
        tab1, tab2, tab3 = st.tabs(["Ajouter", "Finances", "🤖 IA Pub"])
        with tab1:
            v_admin = st.selectbox("Ville cible", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
            q_list_admin = secteurs_bobo if v_admin == "BOBO-DIOULASSO" else quartiers_ouaga
            with st.form("form_add"):
                n = st.text_input("Nom du Salon")
                q = st.selectbox("Quartier", q_list_admin)
                w = st.text_input("WhatsApp")
                ph = st.text_input("Lien Photo Principale")
                cert = st.checkbox("Certifié par l'Empire ?")
                p1 = st.text_input("Service Star & Prix")
                hor = st.text_input("Horaires (ex: Lun-Sam 08h-20h)")
                art = st.text_area("Articles boutique (Mèches, Huiles...)")
                if st.form_submit_button("PUBLIER"):
                    # ville, secteur, nom, type, whatsapp, photo, revenus, video, ph2, ph3, avis, nb_avis, certif, menu, pub_ia, horaires, articles
                    sheet.append_row([v_admin, q, n, "Institut", w, ph, 0, "", "", "", 5, 0, "OUI" if cert else "NON", p1, "", hor, art])
                    st.success("Salon ajouté !")
                    st.rerun()
        with tab2:
            for idx, row in df_salons.iterrows():
                with st.expander(f"💰 {row['nom du salon']}"):
                    st.write(f"Commission : {row.get('revenus', 0)} F")
                    if st.button(f"Encaisser & Reset", key=f"pay_{idx}"):
                        sheet.update_cell(idx + 2, 7, 0)
                        st.rerun()
        with tab3:
            s_ia = st.selectbox("Générer pour :", df_salons['nom du salon'])
            if st.button("✨ GÉNÉRER & SAUVEGARDER"):
                txt = f"🌟 L'excellence s'installe à votre porte ! Découvrez les prestations haut de gamme de {s_ia}. Réservez sur Faso Beauté ! #EmpireBlanco"
                idx_ia = df_salons[df_salons['nom du salon'] == s_ia].index[0]
                sheet.update_cell(idx_ia + 2, 15, txt) # Colonne O (15)
                st.success("Pub enregistrée définitivement !")

# --- ACCUEIL CLIENT ---
st.markdown("""<div class="main-title"><h1>Faso Beauté</h1><p>by Blanco</p></div>""", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Localité", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: 
    q_list_client = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Quartier", q_list_client)

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        sheet_row = idx + 2
        stars = "⭐" * int(row.get('avis_moyenne', 5))
        badge = '<span class="badge-elite">👑 CERTIFIÉ</span>' if row.get('certification') == "OUI" else ""
        
        st.markdown(f'<div class="salon-card"><div class="salon-name">{row["nom du salon"].upper()} {badge} <span style="float:right; font-size:18px;">{stars}</span></div>', unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 1.5])
        with col_img:
            st.image(row['lien photo'] if row['lien photo'] else "https://via.placeholder.com/300", use_container_width=True)
            if row.get('articles'):
                with st.expander("🛍️ Boutique & Articles"):
                    st.write(row['articles'])
            if is_admin: st.metric("Caisse", f"{row.get('revenus', 0)} F")
        
        with col_form:
            if row.get('menu_prix'): st.markdown(f"<span class='price-tag'>🏷️ {row['menu_prix']}</span>", unsafe_allow_html=True)
            st.markdown(f"🕒 **Horaires :** {row.get('horaires', 'Sur rendez-vous')}")
            
            # --- NOTATION CLIENT (DIRECTE) ---
            user_note = st.feedback("stars", key=f"note_{idx}")
            if user_note is not None:
                new_val = user_note + 1
                old_avg = float(row.get('avis_moyenne', 5))
                old_nb = int(row.get('nb_avis', 0))
                new_avg = ((old_avg * old_nb) + new_val) / (old_nb + 1)
                sheet.update_cell(sheet_row, 11, round(new_avg, 1))
                sheet.update_cell(sheet_row, 12, old_nb + 1)
                st.toast("Note enregistrée ! Merci.")

            n_cli = st.text_input("Votre Nom", key=f"n_{idx}")
            t_rdv = st.selectbox("Prestation", ["Simple", "Mariage"], key=f"t_{idx}")
            
            if st.button(f"RÉSERVER", key=f"b_{idx}"):
                if n_cli:
                    gain = 500 if t_rdv == "Mariage" else 100
                    sheet.update_cell(sheet_row, 7, int(row.get('revenus', 0)) + gain)
                    msg = urllib.parse.quote(f"Réservation {t_rdv} pour {n_cli} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border:none; height:45px; cursor:pointer; font-weight:bold;">📲 CONFIRMER WHATSAPP</button></a>', unsafe_allow_html=True)
        
        # --- PUB IA SAUVEGARDÉE ---
        if row.get('pub_ia'):
            st.markdown(f"<div class='info-box'>📣 **L'Empire annonce :** {row['pub_ia']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun partenaire d'exception trouvé dans cette zone.")
