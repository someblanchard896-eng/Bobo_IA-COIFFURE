import streamlit as st
from streamlit_gsheets import GSheetsConnection
import urllib.parse
import pandas as pd

# --- CONFIGURATION PRESTIGE ---
st.set_page_config(page_title="Faso Beauté - by Blanco", page_icon="✨", layout="centered")

# --- CONNEXION GOOGLE SHEETS ---
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    try:
        # Lit le fichier en temps réel
        return conn.read(ttl="0m")
    except:
        # Structure de secours basée sur ton image si le Sheet est vide
        return pd.DataFrame(columns=["ville", "secteur", "nom du salon", "type", "whatsapp", "lien photo", "revenus", "video_url"])

df_salons = charger_donnees()

# --- STYLE WAHOU (FASO BEAUTÉ by BLANCO) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; }
    .waouh-header { background: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1562322140-8baeececf3df?q=80&w=1000&auto=format&fit=crop'); background-size: cover; padding: 50px; border-radius: 0 0 30px 30px; text-align: center; color: #f1c40f; }
    .salon-card { background: #f9f9f9; padding: 20px; border-radius: 20px; border: 1px solid #eee; margin-bottom: 20px; box-shadow: 0 4px 6px rgba(0,0,0,0.05); }
    .stButton>button { border-radius: 25px; background: #1e7e34; color: white; font-weight: bold; border: none; height: 3.5em; width: 100%; }
    .admin-box { background: #fff3cd; padding: 15px; border-radius: 10px; border: 1px solid #ffeeba; margin-top: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES DES QUARTIERS (CONSERVÉES) ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma"]
quartiers_ouaga = ["Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", "Pissy", "Gounghin", "Somgandé"]

# ==========================================
# 🛡️ ESPACE ADMIN (CODE : Blanco.10)
# ==========================================
with st.sidebar:
    st.markdown("### 🛡️ ESPACE BLANCO")
    pwd = st.text_input("Code Secret", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
        st.success("Accès Patron Autorisé")
        
        tab1, tab2 = st.tabs(["➕ Ajouter", "⚙️ Gérer"])
        
        with tab1:
            with st.form("ajout_salon"):
                v = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
                q_list = secteurs_bobo if v == "BOBO-DIOULASSO" else quartiers_ouaga
                q = st.selectbox("Secteur / Quartier", q_list)
                n = st.text_input("Nom du Salon")
                t = st.radio("Type", ["Coiffure", "Institut"], horizontal=True)
                w = st.text_input("WhatsApp (ex: 70000000)")
                ph = st.text_input("Lien Photo")
                vid = st.text_input("Lien Vidéo")
                
                if st.form_submit_button("✅ ENREGISTRER DÉFINITIVEMENT"):
                    new_line = pd.DataFrame([{"ville": v, "secteur": q, "nom du salon": n, "type": t, "whatsapp": w, "lien photo": ph, "revenus": 0, "video_url": vid}])
                    df_updated = pd.concat([df_salons, new_line], ignore_index=True)
                    conn.update(data=df_updated)
                    st.success("Salon enregistré !")
                    st.rerun()

        with tab2:
            st.subheader("Liste des Salons")
            for idx, row in df_salons.iterrows():
                with st.expander(f"{row['nom du salon']} ({row['secteur']})"):
                    st.write(f"💰 Revenus : {row['revenus']} F")
                    c_r1, c_r2 = st.columns(2)
                    if c_r1.button("🔄 Reset Gains", key=f"res_{idx}"):
                        df_salons.at[idx, 'revenus'] = 0
                        conn.update(data=df_salons)
                        st.rerun()
                    if c_r2.button("🗑️ Supprimer", key=f"del_{idx}"):
                        df_salons = df_salons.drop(idx)
                        conn.update(data=df_salons)
                        st.rerun()

# ==========================================
# ✨ ACCUEIL CLIENT (FASO BEAUTÉ by BLANCO)
# ==========================================
st.markdown('<div class="waouh-header"><h1>Faso Beauté</h1><p style="color:white;">by Blanco</p></div>', unsafe_allow_html=True)

c1, c2 = st.columns(2)
with c1: v_c = st.selectbox("📍 Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with c2: 
    q_list_c = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Quartier / Secteur", q_list_c)

# Filtrage dynamique
results = df_salons[(df_salons['ville'] == v_c) & (df_salons['secteur'] == q_c)]

if not results.empty:
    for idx, row in results.iterrows():
        st.markdown('<div class="salon-card">', unsafe_allow_html=True)
        st.subheader(f"⭐ {row['nom du salon'].upper()}")
        
        col_img, col_form = st.columns([1, 2])
        
        with col_img:
            if row['lien photo']: st.image(row['lien photo'])
            if row['video_url']: st.video(row['video_url'])
            if is_admin: st.markdown(f"**💰 Revenus : {row['revenus']} F**")

        with col_form:
            st.write(f"**{row['type']}** | WhatsApp : {row['whatsapp']}")
            n_cli = st.text_input("Votre Nom", key=f"n_{idx}")
            presta_list = ["Simple", "Mariage 💍", "Tresses"] if row['type'] == "Coiffure" else ["Maquillage", "Soins de visage", "Manucure"]
            presta = st.selectbox("Prestation", presta_list, key=f"p_{idx}")
            rdv = st.text_input("Jour et Heure (ex: Samedi 10h)", key=f"t_{idx}")

            if st.button(f"🚀 RÉSERVER CHEZ {row['nom du salon']}", key=f"b_{idx}"):
                if n_cli and rdv:
                    # Mise à jour des gains (Revenus)
                    df_salons.at[idx, 'revenus'] = int(row['revenus']) + 100
                    conn.update(data=df_salons)
                    
                    # WhatsApp
                    msg = urllib.parse.quote(f"Bonjour, réservation {presta} le {rdv} pour la cliente {n_cli} via Faso Beauté.")
                    st.markdown(f'<a href="https://wa.me/226{row["whatsapp"]}?text={msg}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:45px; cursor:pointer; font-weight:bold;">📲 ENVOYER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
                else:
                    st.error("Remplissez le nom et l'heure !")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info("Aucun salon disponible ici pour le moment. Blanco peut en ajouter.")
