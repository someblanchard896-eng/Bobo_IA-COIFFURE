import streamlit as st
import gspread
from google.oauth2.service_account import Credentials
import urllib.parse
import pandas as pd

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

def safe_int(val):
    try: return int(float(str(val).replace(" ", "").replace("F", ""))) if val else 0
    except: return 0

# --- STYLE CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #ffffff; font-family: 'Poppins', sans-serif; }
    .salon-card { border-left: 5px solid #d4af37; padding: 25px; margin-bottom: 30px; box-shadow: 0px 10px 30px rgba(0,0,0,0.05); background: #fff; }
    .badge-elite { background-color: #d4af37; color: white; padding: 4px 10px; font-size: 12px; border-radius: 20px; font-weight: bold; margin-left: 10px; }
    .stButton>button { background-color: #000 !important; color: #d4af37 !important; border: 1px solid #d4af37 !important; font-weight: bold; width: 100%; height: 3.5em; }
    .label-style { font-weight: 600; color: #333; font-size: 14px; margin-bottom: 2px; display: block; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES INTEGRALES DES QUARTIERS ---
secteurs_bobo = ["Sya", "Koko", "Secteur 3", "Secteur 4", "Secteur 5", "Bolomakoté", "Secteur 7", "Secteur 8", "Accart-ville", "Yéguéré", "Colma", "Secteur 12", "Dogona", "Bindougousso", "Secteur 15", "Secteur 16", "Sarfalao", "Secteur 18", "Secteur 19", "Secteur 20", "Secteur 21", "Secteur 22", "Bobo 2010", "Secteur 24", "Belle-Ville", "Ouezzinville"]
quartiers_ouaga = ["Ouaga 2000", "Karpala", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Balkuy", "Cissin", "Larlé", "Tanghin", "Koulouba", "Wemtenga", "Dapoya", "Paspanga", "Hamdalaye", "Saaba", "Nagrin", "Kamsontenga", "Rimkieta", "Boassa", "Kilwin", "Kamboinssin"]
jours_semaine = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]

# --- SIDEBAR : LE CENTRE DE COMMANDE ---
with st.sidebar:
    st.title("🔱 MENU EMPIRE")
    mode = st.radio("Mode d'Accès", ["Client", "Admin Empire (Blanco)", "Espace Salon Pro"])
    
    if mode == "Admin Empire (Blanco)":
        master_pwd = st.text_input("Code Maître", type="password")
        if master_pwd == "Blanco.10":
            st.success("👑 Accès Maître")
            t_add, t_fin, t_ia = st.tabs(["➕ Nouveau", "💰 Finances", "🤖 IA"])
            with t_add:
                with st.form("admin_add"):
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
                        if st.button(f"Encaisser", key=f"p_{i}"):
                            sheet.update_cell(i+2, 7, 0); st.rerun()
            with t_ia:
                s_ia = st.selectbox("Salon", df_salons['nom du salon'])
                if st.button("🤖 PUBLIER PUB IA"):
                    idx_ia = df_salons[df_salons['nom du salon'] == s_ia].index[0] + 2
                    pub = f"✨ {s_ia} : Le luxe et le prestige à votre portée. Réservez sur Faso Beauté !"
                    sheet.update_cell(idx_ia, 15, pub); st.success("Pub publiée !")

    elif mode == "Espace Salon Pro":
        nom_sel = st.selectbox("Votre Salon", df_salons['nom du salon'])
        user_pwd = st.text_input("Code Secret", type="password")
        row_p = df_salons[df_salons['nom du salon'] == nom_sel].iloc[0]
        if user_pwd != "" and (user_pwd == str(row_p.get('code_secret', '')) or user_pwd == "Blanco.10"):
            with st.form("pro_form"):
                v_p = st.text_input("Vidéo", value=row_p.get('video_url', ''))
                h_p = st.text_input("Horaires", value=row_p.get('horaires', ''))
                a_p = st.text_area("Boutique", value=row_p.get('articles', ''))
                if st.form_submit_button("SAUVEGARDER"):
                    idx_p = df_salons[df_salons['nom du salon'] == nom_sel].index[0] + 2
                    sheet.update_cell(idx_p, 8, v_p)
                    sheet.update_cell(idx_p, 16, h_p)
                    sheet.update_cell(idx_p, 17, a_p)
                    st.success("Enregistré !"); st.rerun()

# --- ACCUEIL CLIENT ---
st.markdown("<h1 style='text-align:center; color:#d4af37;'>FASO BEAUTÉ</h1>", unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        sheet_row = idx + 2
        # --- LOGIQUE BADGE SÉCURISÉE ---
        is_cert = str(row.get('certification', '')).strip().upper() == "OUI"
        badge = '<span class="badge-elite">👑 CERTIFIÉ</span>' if is_cert else ""
        
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        st.markdown(f"<h3>{row['nom du salon'].upper()} {badge} <span style='float:right; font-size:16px; color:#d4af37;'>⭐ {row.get('avis_moyenne', 5)}/5</span></h3>", unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 1.2])
        with col_img:
            st.image(row['lien photo'] if row['lien photo'] else "https://via.placeholder.com/200")
            if row.get('video_url'): st.video(row['video_url'])
            if row.get('articles'):
                with st.expander("🛍️ Boutique"): st.write(row['articles'])

        with col_form:
            st.markdown(f"🕒 **Horaires :** {row.get('horaires', '08h-20h')}")
            st.markdown('<span class="label-style">Votre Nom</span>', unsafe_allow_html=True)
            n_cli = st.text_input("", placeholder="Mme/M. ...", key=f"n_{idx}", label_visibility="collapsed")
            st.markdown('<span class="label-style">Heure</span>', unsafe_allow_html=True)
            h_rdv = st.text_input("", placeholder="14h30", key=f"h_{idx}", label_visibility="collapsed")
            j_rdv = st.selectbox("Jour", jours_semaine, key=f"j_{idx}")

            if st.button("🚀 RÉSERVER", key=f"b_{idx}"):
                if n_cli and h_rdv:
                    sheet.update_cell(sheet_row, 7, safe_int(row.get('revenus', 0)) + 100)
                    msg = urllib.parse.quote(f"RDV pour {n_cli} le {j_rdv} à {h_rdv} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}" target="_blank"><button style="width:100%; background:#25D366; color:white; border:none; padding:10px; cursor:pointer; font-weight:bold;">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
                else: st.warning("Remplissez le NOM et l'HEURE.")
        
        if row.get('pub_ia'):
            st.markdown(f"<div style='background:#fff9e6; padding:10px; border-left:4px solid #d4af37; font-size:13px;'>📣 {row['pub_ia']}</div>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
