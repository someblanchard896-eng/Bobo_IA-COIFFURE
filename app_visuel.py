import streamlit as st
from streamlit_gsheets import GSheetsConnection
import urllib.parse
import pandas as pd

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté | L'Excellence par Blanco", page_icon="✨", layout="centered")

# --- CONNEXION GSHEETS D'ORIGINE (NE PAS TOUCHER) ---
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    try:
        # Ton URL de Sheet d'origine
        url = "https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJIY3s/edit#gid=0"
        return conn.read(spreadsheet=url, ttl="0m")
    except:
        return pd.DataFrame(columns=["ville", "secteur", "nom du salon", "type", "whatsapp", "lien photo", "revenus", "video_url"])

df_salons = charger_donnees()

# --- INTERFACE "WAHOU" LUMINEUSE (BLANC & OR) ---
st.markdown("""
    <style>
    /* Fond Clair et Chic */
    .stApp { background-color: #FFFFFF; color: #2c3e50; }
    
    /* Header avec dégradé Vert/Or */
    .hero-section {
        background: linear-gradient(135deg, #1e7e34 0%, #d4af37 100%);
        padding: 50px 20px; border-radius: 0 0 40px 40px; text-align: center;
        color: white; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }
    .hero-section h1 { font-size: 55px !important; font-weight: 900 !important; margin-bottom: 0px; text-shadow: 2px 2px 4px rgba(0,0,0,0.2); }
    .hero-section p { font-size: 18px; opacity: 0.9; font-style: italic; }

    /* Cartes Salons Style "Galerie" */
    .salon-card {
        background: #fdfdfd; padding: 25px; border-radius: 25px;
        border: 1px solid #f1f1f1; margin-bottom: 30px;
        box-shadow: 0 10px 20px rgba(0,0,0,0.05);
    }
    
    /* Boutons Dorés */
    .stButton>button {
        border-radius: 30px; background: linear-gradient(45deg, #d4af37, #b8860b);
        color: white !important; font-weight: bold; border: none; height: 3.5em;
        box-shadow: 0 4px 15px rgba(212, 175, 55, 0.4);
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 6px 20px rgba(212, 175, 55, 0.6); }

    /* Barre Admin */
    [data-testid="stSidebar"] { background-color: #f8f9fa; border-right: 2px solid #d4af37; }
    </style>
    """, unsafe_allow_html=True)

# --- QUARTIERS ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma", "Sya"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé", "Balkuy", "Ouaga Inter"]

# ==========================================
# 🛡️ ESPACE ADMIN (Blanco.10)
# ==========================================
with st.sidebar:
    st.markdown("<h2 style='color:#1e7e34;'>🔱 Bureau Blanco</h2>", unsafe_allow_html=True)
    pwd = st.text_input("Code Secret", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
        st.success("Empire Connecté")
        tab_a, tab_g = st.tabs(["➕ Nouveau Salon", "⚙️ Gestion"])
        with tab_a:
            with st.form("add"):
                v = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
                q = st.selectbox("Secteur", secteurs_bobo if v == "BOBO-DIOULASSO" else quartiers_ouaga)
                n = st.text_input("Nom de l'établissement")
                t = st.radio("Type", ["Coiffure", "Institut"], horizontal=True)
                w = st.text_input("WhatsApp")
                ph = st.text_input("Lien Photo")
                vid = st.text_input("Lien Vidéo")
                if st.form_submit_button("PUBLIER DANS LE RÉSEAU"):
                    # On conserve la structure exacte de ton Sheet
                    new_row = pd.DataFrame([{"ville": v, "secteur": q, "nom du salon": n, "type": t, "whatsapp": w, "lien photo": ph, "revenus": 0, "video_url": vid}])
                    df_updated = pd.concat([df_salons, new_row], ignore_index=True)
                    conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJIY3s/edit#gid=0", data=df_updated)
                    st.rerun()
        with tab_g:
            for idx, row in df_salons.iterrows():
                st.write(f"**{row['nom du salon']}** | {row['revenus']} F")
                if st.button("🗑️ Supprimer", key=f"del_{idx}"):
                    df_new = df_salons.drop(idx)
                    conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJIY3s/edit#gid=0", data=df_new)
                    st.rerun()

# ==========================================
# ✨ ACCUEIL FASO BEAUTÉ
# ==========================================
st.markdown("""
    <div class="hero-section">
        <h1>FASO BEAUTÉ</h1>
        <p>by Blanco</p>
        <div style="margin-top:10px; font-weight:bold; letter-spacing:1px;">L'ÉLITE DE LA BEAUTÉ AU BURKINA FASO</div>
    </div>
    """, unsafe_allow_html=True)

# Filtres
c1, c2 = st.columns(2)
with c1:
    v_c = st.selectbox("📍 Choisissez votre ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2:
    q_list_c = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Choisissez votre Quartier", q_list_c)

st.markdown("<br>", unsafe_allow_html=True)

# Affichage des Salons
results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        st.markdown(f"<h2 style='color:#1e7e34; text-align:center;'>✨ {row['nom du salon'].upper()}</h2>", unsafe_allow_html=True)
        
        col_img, col_form = st.columns([1, 1.4])
        with col_img:
            if row['lien photo']: st.image(row['lien photo'], use_container_width=True)
            if is_admin: st.metric("Caisse (Gains)", f"{row['revenus']} F")
        with col_form:
            st.markdown(f"🖋️ **Prestation : {row['type']}**")
            st.markdown(f"📱 **WhatsApp associé :** {row['whatsapp']}")
            
            n_cli = st.text_input("Votre Nom complet", key=f"n_{idx}", placeholder="Ex: Mme Sanon")
            rdv = st.text_input("Jour et Heure souhaitée", key=f"t_{idx}", placeholder="Ex: Samedi à 15h00")
            
            if st.button(f"🚀 RÉSERVER MON CRÉNEAU VIP", key=f"b_{idx}"):
                if n_cli and rdv:
                    # Enregistrement des 100 F
                    df_salons.at[idx, 'revenus'] = int(row['revenus']) + 100
                    conn.update(spreadsheet="https://docs.google.com/spreadsheets/d/1vmi_lysNR0zqu6z9m2FM6MDHp73EwbeQtY0WiOJIY3s/edit#gid=0", data=df_salons)
                    
                    # Lien WhatsApp
                    msg = urllib.parse.quote(f"Bonjour, je souhaite réserver une séance de {row['type']} le {rdv} pour la cliente {n_cli} via Faso Beauté.")
                    url_wa = f"https://wa.me/226{row['whatsapp']}?text={msg}"
                    
                    st.success("Demande validée ! Cliquez pour envoyer le message.")
                    st.markdown(f'<a href="{url_wa}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:50px; cursor:pointer; font-weight:bold;">📲 CONFIRMER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
                else:
                    st.error("⚠️ Veuillez remplir le nom et l'heure pour réserver.")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun partenaire trouvé dans ce secteur. L'Administrateur peut en ajouter dans la barre de gauche.")

st.markdown("<p style='text-align:center; color:gray; font-size:12px; margin-top:50px;'>Faso Beauté - Le Réseau Premium by Blanco © 2026</p>", unsafe_allow_html=True)
