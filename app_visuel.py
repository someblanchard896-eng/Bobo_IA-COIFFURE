import streamlit as st
from streamlit_gsheets import GSheetsConnection
import urllib.parse
import pandas as pd

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté | L'Excellence par Blanco", page_icon="✨", layout="centered")

# --- TON ANCIENNE CONNEXION (CELLE QUI MARCHE) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    try:
        # On utilise ton URL de Sheet comme avant
        url = "https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJIY3s/edit#gid=0"
        return conn.read(spreadsheet=url, ttl="0m")
    except:
        return pd.DataFrame(columns=["ville", "secteur", "nom du salon", "type", "whatsapp", "lien photo", "revenus", "video_url"])

df_salons = charger_donnees()

# --- DESIGN "WAHOU" BLACK & GOLD (INJECTÉ) ---
st.markdown("""
    <style>
    .stApp { background-color: #0b0d11; color: #ffffff; }
    .hero-section {
        background: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1560066984-138dadb4c035?q=80&w=1000&auto=format&fit=crop');
        background-size: cover; background-position: center;
        padding: 60px 20px; border-radius: 0 0 40px 40px; text-align: center;
        border-bottom: 3px solid #d4af37; margin-bottom: 30px;
    }
    .hero-section h1 { color: #d4af37 !important; font-size: 50px !important; font-weight: 900 !important; }
    .salon-card {
        background: rgba(255, 255, 255, 0.05); padding: 25px; border-radius: 20px;
        border: 1px solid rgba(214, 175, 55, 0.3); margin-bottom: 25px;
    }
    .stButton>button {
        border-radius: 30px; background: linear-gradient(45deg, #d4af37, #b8860b);
        color: #000 !important; font-weight: bold; border: none; height: 3.5em;
    }
    /* Sidebar */
    [data-testid="stSidebar"] { background-color: #161b22; border-right: 1px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- QUARTIERS ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin"]

# ==========================================
# 🛡️ ADMINISTRATION (Blanco.10)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#d4af37;'>🔱 Bureau Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Clé d'accès", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
        tab_a, tab_g = st.tabs(["Ajouter", "Gérer"])
        with tab_a:
            with st.form("add"):
                v = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
                q = st.selectbox("Secteur", secteurs_bobo if v == "BOBO-DIOULASSO" else quartiers_ouaga)
                n = st.text_input("Nom du Salon")
                t = st.radio("Type", ["Coiffure", "Institut"], horizontal=True)
                w = st.text_input("WhatsApp")
                ph = st.text_input("Lien Photo")
                vid = st.text_input("Lien Vidéo")
                if st.form_submit_button("PUBLIER"):
                    new_row = pd.DataFrame([{"ville": v, "secteur": q, "nom du salon": n, "type": t, "whatsapp": w, "lien photo": ph, "revenus": 0, "video_url": vid}])
                    df_updated = pd.concat([df_salons, new_row], ignore_index=True)
                    conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJIY3s/edit#gid=0", data=df_updated)
                    st.rerun()
        with tab_g:
            for idx, row in df_salons.iterrows():
                st.write(f"{row['nom du salon']} ({row['revenus']} F)")
                if st.button("Supprimer", key=f"del_{idx}"):
                    df_new = df_salons.drop(idx)
                    conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJIY3s/edit#gid=0", data=df_new)
                    st.rerun()

# ==========================================
# ✨ ACCUEIL FASO BEAUTÉ
# ==========================================
st.markdown("""
    <div class="hero-section">
        <h1>FASO BEAUTÉ</h1>
        <p style="color:#d4af37;">by Blanco</p>
        <p>L'excellence de la beauté burkinabè à votre portée.</p>
    </div>
    """, unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: q_c = st.selectbox("🏘️ Secteur / Quartier", secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga)

# Filtrage
results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        st.markdown(f"<h3 style='color:#d4af37; text-align:center;'>✨ {row['nom du salon'].upper()}</h3>", unsafe_allow_html=True)
        
        col_m, col_f = st.columns([1, 1.5])
        with col_m:
            if row['lien photo']: st.image(row['lien photo'], use_container_width=True)
            if is_admin: st.metric("Gains", f"{row['revenus']} F")
        with col_f:
            st.write(f"**{row['type']}** | WhatsApp : {row['whatsapp']}")
            n_cli = st.text_input("Nom", key=f"n_{idx}")
            rdv = st.text_input("Jour / Heure", key=f"t_{idx}")
            
            if st.button(f"🚀 RÉSERVER VIP", key=f"b_{idx}"):
                if n_cli and rdv:
                    df_salons.at[idx, 'revenus'] = int(row['revenus']) + 100
                    conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJIY3s/edit#gid=0", data=df_salons)
                    msg = urllib.parse.quote(f"Bonjour, réservation pour {n_cli} à {rdv} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:45px; cursor:pointer; font-weight:bold;">📲 WHATSAPP</button></a>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun salon trouvé dans ce secteur.")
