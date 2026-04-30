import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd

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

def safe_int(val):
    try: return int(float(str(val).replace(" ", "").replace("F", ""))) if val else 0
    except: return 0

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; }
    .salon-card { border-left: 5px solid #d4af37; padding: 20px; margin-bottom: 25px; box-shadow: 0px 5px 15px rgba(0,0,0,0.05); background: white; border-radius: 5px; }
    .btn-wa { background-color: #25D366; color: white !important; padding: 12px; border-radius: 5px; text-align: center; text-decoration: none; display: block; font-weight: bold; margin-top: 10px; border: none; width: 100%; }
    .label-style { font-weight: bold; color: #333; font-size: 14px; margin-bottom: 2px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES (QUARTIERS COMPLETS) ---
secteurs_bobo = ["Sya", "Koko", "Secteur 3", "Secteur 4", "Secteur 5", "Bolomakoté", "Secteur 7", "Secteur 8", "Accart-ville", "Yéguéré", "Colma", "Secteur 12", "Dogona", "Bindougousso", "Secteur 15", "Secteur 16", "Sarfalao", "Secteur 18", "Secteur 19", "Secteur 20", "Secteur 21", "Secteur 22", "Bobo 2010", "Secteur 24", "Belle-Ville", "Ouezzinville"]
quartiers_ouaga = ["Ouaga 2000", "Karpala", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Balkuy", "Cissin", "Larlé", "Tanghin", "Koulouba", "Wemtenga", "Dapoya", "Paspanga", "Hamdalaye", "Saaba", "Nagrin", "Kamsontenga", "Rimkieta", "Boassa", "Kilwin", "Kamboinssin"]

# --- SIDEBAR (ADMIN & PRO) ---
with st.sidebar:
    st.title("🔱 MENU EMPIRE")
    mode = st.radio("Accès", ["Client", "Admin Empire (Blanco)", "Espace Salon Pro"])
    # ... (Garde ton code Admin et Pro d'avant ici, il est bon)

# --- INTERFACE CLIENT ---
st.markdown("<h1 style='text-align:center; color:#d4af37;'>FASO BEAUTÉ</h1>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Secteur", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        sheet_row = idx + 2
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        st.markdown(f"<h3>{row['nom du salon'].upper()} <span style='float:right; font-size:16px; color:#d4af37;'>⭐ {row.get('avis_moyenne', 5)}/5</span></h3>", unsafe_allow_html=True)
        
        col_img, col_info = st.columns([1, 1.2])
        with col_img:
            st.image(row['lien photo'] if row['lien photo'] else "https://via.placeholder.com/300", use_container_width=True)
            if row.get('video_url'): st.video(row['video_url'])

        with col_info:
            st.write(f"🕒 **Horaires :** {row.get('horaires', '08h-20h')}")
            
            # Champs de saisie
            st.markdown('<span class="label-style">Votre Nom</span>', unsafe_allow_html=True)
            n_cli = st.text_input("", placeholder="Mme/M. ...", key=f"n_{idx}", label_visibility="collapsed")
            
            st.markdown('<span class="label-style">Heure du RDV</span>', unsafe_allow_html=True)
            h_rdv = st.text_input("", placeholder="Ex: 15h30", key=f"h_{idx}", label_visibility="collapsed")
            
            j_rdv = st.selectbox("Jour", ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"], key=f"j_{idx}")

            # LE BOUTON DE RÉSERVATION (Toujours présent)
            if st.button(f"🚀 RÉSERVER CHEZ {row['nom du salon']}", key=f"btn_{idx}"):
                if n_cli and h_rdv:
                    # 1. On crédite tes 100 F dans le Sheet
                    current_rev = safe_int(row.get('revenus', 0))
                    sheet.update_cell(sheet_row, 7, current_rev + 100)
                    
                    # 2. On prépare le lien WhatsApp
                    texte_wa = urllib.parse.quote(f"Bonjour {row['nom du salon']}, je réserve pour {n_cli} le {j_rdv} à {h_rdv} via Faso Beauté.")
                    lien_wa = f"https://wa.me/226{row['whatsapp']}?text={texte_wa}"
                    
                    # 3. On affiche le bouton WhatsApp final
                    st.markdown(f'<a href="{lien_wa}" target="_blank" class="btn-wa">✅ CLIQUER ICI POUR ENVOYER SUR WHATSAPP</a>', unsafe_allow_html=True)
                    st.balloons()
                else:
                    st.warning("⚠️ Remplissez votre NOM et l'HEURE avant de réserver.")

        if row.get('pub_ia'):
            st.markdown(f"<div style='background:#fff9e6; padding:10px; border-radius:5px; margin-top:10px; border-left:4px solid #d4af37;'>📣 {row['pub_ia']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
