import streamlit as st
from streamlit_gsheets import GSheetsConnection
import urllib.parse
import pandas as pd

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté - by Blanco", page_icon="✨", layout="centered")

# --- CONNEXION GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

# Lecture des données existantes
try:
    df_salons = conn.read(ttl="0m") # On lit en temps réel sans cache
except:
    # Si le fichier est vide, on crée la structure
    df_salons = pd.DataFrame(columns=["ville", "nom", "type", "quartier", "tel", "photo", "video", "gains"])

# --- STYLE PRESTIGE ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #2c3e50; }
    .waouh-header { background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1560066984-138dadb4c035?q=80&w=1000&auto=format&fit=crop'); background-size: cover; background-position: center; padding: 60px 20px; border-radius: 0 0 30px 30px; margin-bottom: 30px; }
    .waouh-header h1 { color: #f1c40f !important; font-size: 50px !important; text-align: center; font-weight: 900; }
    .waouh-header p { color: white; text-align: center; font-size: 20px; }
    .salon-card { background: #f8f9fa; padding: 25px; border-radius: 20px; border: 1px solid #eee; margin-bottom: 25px; }
    .stButton>button { border-radius: 25px; background: linear-gradient(45deg, #1e7e34, #28a745); color: white; font-weight: bold; border: none; height: 3.5em; }
    </style>
    """, unsafe_allow_html=True)

# --- QUARTIERS ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin"]

# ==========================================
# 🛡️ ESPACE ADMIN (Blanco.10)
# ==========================================
with st.sidebar:
    st.markdown("### 🔐 ACCÈS BLANCO")
    pwd = st.text_input("Code Secret", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
        st.success("Mode Gestionnaire Activé")
        with st.form("ajout_salon"):
            v_a = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
            q_list = secteurs_bobo if v_a == "BOBO-DIOULASSO" else quartiers_ouaga
            q_a = st.selectbox("Secteur / Quartier", q_list)
            n_a = st.text_input("Nom du Salon")
            t_a = st.radio("Type", ["Coiffure", "Institut"], horizontal=True)
            w_a = st.text_input("WhatsApp (70000000)")
            p_a = st.text_input("Lien Photo")
            vid_a = st.text_input("Lien Vidéo")
            
            if st.form_submit_button("✅ ENREGISTRER DÉFINITIVEMENT"):
                new_row = pd.DataFrame([{
                    "ville": v_a, "nom": n_a, "type": t_a, "quartier": q_a, 
                    "tel": w_a, "photo": p_a, "video": vid_a, "gains": 0
                }])
                df_updated = pd.concat([df_salons, new_row], ignore_index=True)
                conn.update(data=df_updated)
                st.success("Salon enregistré dans Google Sheets !")
                st.rerun()

# ==========================================
# ✨ ACCUEIL CLIENT (FASO BEAUTÉ)
# ==========================================
st.markdown('<div class="waouh-header"><h1>Faso Beauté</h1><p>by Blanco</p></div>', unsafe_allow_html=True)

col_v, col_q = st.columns(2)
with col_v:
    v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with col_q:
    q_list_c = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Quartier", q_list_c)

# Filtrage des données Google Sheets
salons_filtrés = df_salons[(df_salons['ville'] == v_c) & (df_salons['quartier'] == q_c)]

if not salons_filtrés.empty:
    for index, row in salons_filtrés.iterrows():
        with st.container():
            st.markdown('<div class="salon-card">', unsafe_allow_html=True)
            st.subheader(f"⭐ {row['nom'].upper()}")
            c1, c2 = st.columns([1, 2])
            
            with c1:
                if row['photo']: st.image(row['photo'])
                if row['video']: st.video(row['video'])
                if is_admin: st.info(f"💰 Gains : {row['gains']} F")
            
            with c2:
                st.write(f"**{row['type']}** | WhatsApp : {row['tel']}")
                nom_cli = st.text_input("Nom cliente", key=f"n_{index}")
                jour = st.text_input("Jour", key=f"j_{index}")
                heure = st.text_input("Heure", key=f"h_{index}")
                
                if st.button(f"🚀 RÉSERVER CHEZ {row['nom']}", key=f"b_{index}"):
                    # Mise à jour des gains dans le Google Sheet
                    df_salons.at[index, 'gains'] += 100
                    conn.update(data=df_salons)
                    
                    # WhatsApp
                    msg = urllib.parse.quote(f"Réservation pour {row['type']} le {jour} à {heure} pour {nom_cli} via Faso Beauté.")
                    url = f"https://wa.me/226{row['tel']}?text={msg}"
                    st.success("100 F ajoutés ! Cliquez pour WhatsApp.")
                    st.markdown(f'<a href="{url}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:45px; cursor:pointer;">📲 ENVOYER WHATSAPP</button></a>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
else:
    st.write("Aucun salon ici. Blanco peut en ajouter via l'Admin.")
