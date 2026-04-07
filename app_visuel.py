import streamlit as st
import urllib.parse

# --- CONFIGURATION LUXE ---
st.set_page_config(page_title="Blanco Connect - Prestige", page_icon="✨", layout="centered")

# --- STYLE PRESTIGE (FINI LE NOIR) ---
st.markdown("""
    <style>
    .stApp { background-color: #FFFFFF; color: #2c3e50; }
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; background: linear-gradient(45deg, #1e7e34, #28a745); color: white; font-weight: bold; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
    .stSelectbox, .stTextInput { border-radius: 15px; }
    h1 { color: #1e7e34; font-family: 'Helvetica Neue', sans-serif; font-weight: 800; text-align: center; }
    .caisse-badge { background-color: #f1c40f; color: #2c3e50; padding: 10px 20px; border-radius: 20px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .salon-card { background: #f8f9fa; padding: 20px; border-radius: 20px; border: 1px solid #e9ecef; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- TA BASE DE DONNÉES DES QUARTIERS (INTÉGRÉE) ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma", "Sya"]
quartiers_ouaga = [
    "Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", 
    "Pissy", "Gounghin", "Somgandé", "Larlé", "Cissin", "Koulouba", "Wemtenga", "Dagnoën", 
    "Zone du Bois", "1200 Logements", "Kamsonghin", "Samandin", "Paspanga", "Ouidi", 
    "Nemnin", "Tanghin", "Zone Industrielle", "Bendogo", "Kalgondin", "Nagrin", "Bassinko", 
    "Kossodo", "Balkuy"
]

# --- MÉMOIRE ---
if 'base_salons' not in st.session_state:
    st.session_state.base_salons = {"BOBO-DIOULASSO": {}, "OUAGADOUGOU": {}}

# ==========================================
# 🛡️ ESPACE ADMIN (CODE : Blanco.10)
# ==========================================
with st.sidebar:
    st.markdown("### 🔐 ACCÈS BLANCO")
    pwd = st.text_input("Code Secret", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
        st.success("Bienvenue, Patron.")
        st.divider()
        st.subheader("➕ Ajouter un Partenaire")
        with st.form("form_admin"):
            v_a = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
            # ICI : On utilise tes listes de quartiers
            q_list = secteurs_bobo if v_a == "BOBO-DIOULASSO" else quartiers_ouaga
            q_a = st.selectbox("Secteur / Quartier", q_list)
            
            n_a = st.text_input("Nom du Salon")
            t_a = st.radio("Type", ["Coiffure", "Institut"])
            w_a = st.text_input("Numéro WhatsApp (ex: 70000000)")
            img_a = st.text_input("Lien Photo URL (i.ibb.co)")
            vid_a = st.text_input("Lien Vidéo URL")
            
            if st.form_submit_button("✅ PUBLIER MAINTENANT"):
                if n_a and w_a:
                    st.session_state.base_salons[v_a][n_a] = {
                        "tel": w_a, "quartier": q_a, "type": t_a,
                        "photo": img_a, "video": vid_a, "gains": 0
                    }
                    st.toast("Salon ajouté au réseau !")

# ==========================================
# ✨ ACCUEIL CLIENT (LE RÉSEAU)
# ==========================================
st.title("✨ BLANCO CONNECT ✨")
st.markdown("<p style='text-align: center; color: #6c757d;'>Votre beauté, notre priorité au Burkina Faso</p>", unsafe_allow_html=True)

# 1. Filtres Clients
col_v, col_q = st.columns(2)
with col_v:
    v_c = st.selectbox("📍 Choisissez votre ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with col_q:
    q_list_c = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Choisissez votre Quartier", q_list_c)

st.divider()

# 2. Affichage des Salons
salons_v = st.session_state.base_salons[v_c]
salons_q = {n: s for n, s in salons_v.items() if s['quartier'] == q_c}

if salons_q:
    for nom, info in salons_q.items():
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        st.subheader(f"⭐ {nom}")
        
        c1, c2 = st.columns([1, 2])
        with c1:
            if info['photo']: st.image(info['photo'], use_container_width=True)
            if info['video']: st.video(info['video'])
            if is_admin: # SEUL LE PATRON VOIT ÇA
                st.markdown(f'<div class="caisse-badge">💰 Gains : {info["gains"]} F</div>', unsafe_allow_html=True)
        
        with c2:
            st.write(f"**{info['type']}** | 📍 {info['quartier']}")
            st.write(f"📞 WhatsApp associé : {info['tel']}")
            
            # Formulaire de réservation
            nom_cli = st.text_input("Votre Nom", key=f"n_{nom}")
            
            if info['type'] == "Coiffure":
                presta = st.selectbox("Prestation", ["Coiffure Simple", "Mariage 💍", "Tresses/Chignon"], key=f"p_{nom}")
            else:
                presta = st.selectbox("Prestation", ["Maquillage 💄", "Soins de visage", "Pédicure/Manucure"], key=f"p_{nom}")
            
            c_d, c_h = st.columns(2)
            with c_d: jour_r = st.text_input("Jour (ex: Samedi)", key=f"j_{nom}")
            with c_h: heure_r = st.text_input("Heure (ex: 15h)", key=f"h_{nom}")

            if st.button(f"🚀 RÉSERVER CHEZ {nom.upper()}", key=f"b_{nom}"):
                if nom_cli and jour_r and heure_r:
                    # Gain de 100F
                    st.session_state.base_salons[v_c][nom]['gains'] += 100
                    
                    # Message WhatsApp
                    msg = (f"Bonjour comment allez vous, je veux une réservation pour une {presta} "
                           f"le {jour_r} à {heure_r} pour la cliente {nom_cli} via Beauté Connect.")
                    
                    num = info['tel'].replace(" ", "").replace("+", "")
                    num_f = f"226{num}" if not num.startswith("226") else num
                    url = f"https://wa.me/{num_f}?text={urllib.parse.quote(msg)}"
                    
                    st.success("Réservation prête !")
                    st.markdown(f'''<a href="{url}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:45px; cursor:pointer; font-weight:bold;">📲 ENVOYER SUR WHATSAPP</button></a>''', unsafe_allow_html=True)
                else:
                    st.error("Remplissez le formulaire de réservation !")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.info(f"Aucun partenaire {v_c} n'est encore enregistré à {q_c}. Patron, utilisez votre code pour en ajouter !")

st.markdown("<br><br><p style='text-align: center; color: gray;'>Blanco Connect © 2026</p>", unsafe_allow_html=True)
