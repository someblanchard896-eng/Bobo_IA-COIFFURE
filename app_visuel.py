import streamlit as st
import urllib.parse

# --- CONFIGURATION HAUT DE GAMME ---
st.set_page_config(page_title="Faso Beauté - by Blanco", page_icon="✨", layout="centered")

# --- STYLE PRESTIGE ET WHaou (FUSO) ---
st.markdown("""
    <style>
    /* Global */
    .stApp { background-color: #FFFFFF; color: #2c3e50; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Header 'Wahou' */
    .waouh-header { background: linear-gradient(rgba(0,0,0,0.5), rgba(0,0,0,0.7)), url('https://images.unsplash.com/photo-1560066984-138dadb4c035?q=80&w=1000&auto=format&fit=crop'); background-size: cover; background-position: center; padding: 60px 20px; border-radius: 0 0 30px 30px; margin-bottom: 30px; box-shadow: 0 10px 30px rgba(0,0,0,0.1); }
    .waouh-header h1 { color: #f1c40f !important; font-size: 50px !important; font-weight: 900 !important; text-align: center; margin-bottom: 5px; text-shadow: 2px 2px 4px rgba(0,0,0,0.3); }
    .waouh-header p { color: #ecf0f1; font-size: 20px; text-align: center; margin-bottom: 0; font-weight: 300; }
    
    /* Boutons et Éléments */
    .stButton>button { width: 100%; border-radius: 25px; height: 3.5em; background: linear-gradient(45deg, #1e7e34, #28a745); color: white; font-weight: bold; border: none; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: all 0.3s ease; }
    .stButton>button:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(40, 167, 69, 0.4); }
    .stSelectbox, .stTextInput { border-radius: 15px; border: 1px solid #ced4da; }
    
    /* Cartes */
    .welcome-card { background: #f8f9fa; padding: 25px; border-radius: 20px; text-align: center; box-shadow: 0 5px 15px rgba(0,0,0,0.05); margin-bottom: 30px; border: 1px solid #e9ecef; }
    .welcome-card i { font-size: 40px; color: #1e7e34; margin-bottom: 15px; display: block; }
    .caisse-badge { background-color: #f1c40f; color: #2c3e50; padding: 10px 20px; border-radius: 20px; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .salon-card { background: #fdfdfd; padding: 25px; border-radius: 20px; border: 1px solid #eee; margin-bottom: 25px; box-shadow: 0 2px 10px rgba(0,0,0,0.03); }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES DES QUARTIERS (INTÉGRÉE) ---
secteurs_bobo = [f"Secteur {i}" for i in range(1, 26)] + ["Sarfalao", "Yéguéré", "Accart-ville", "Colma", "Sya"]
quartiers_ouaga = [
    "Karpala", "Ouaga 2000", "Patte d'Oie", "Dassasgho", "Zone 1", "Zogona", "Tampouy", 
    "Pissy", "Gounghin", "Somgandé", "Larlé", "Cissin", "Koulouba", "Wemtenga", "Dagnoën", 
    "Zone du Bois", "1200 Logements", "Kamsonghin", "Samandin", "Paspanga", "Ouidi", 
    "Nemnin", "Tanghin", "Zone Industrielle", "Bendogo", "Kalgondin", "Nagrin", "Bassinko", 
    "Kossodo", "Balkuy"
]

# --- MÉMOIRE (SESSION STATE) ---
if 'base_salons' not in st.session_state:
    st.session_state.base_salons = {"BOBO-DIOULASSO": {}, "OUAGADOUGOU": {}}

# ==========================================
# 🛡️ ESPACE ADMIN (CODE : Blanco.10) - CONSERVÉ
# ==========================================
with st.sidebar:
    st.markdown("### 🔐 ACCÈS ADMINISTRATEUR")
    pwd = st.text_input("Code Secret Blanco Connect", type="password")
    is_admin = (pwd == "Blanco.10")
    
    if is_admin:
        st.success("Bonjour, Monsieur Blanco.")
        st.divider()
        st.subheader("➕ Ajouter un Nouveau Partenaire")
        with st.form("form_admin_final"):
            v_a = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
            q_list = secteurs_bobo if v_a == "BOBO-DIOULASSO" else quartiers_ouaga
            q_a = st.selectbox("Secteur / Quartier", q_list)
            
            n_a = st.text_input("Nom de l'établissement", placeholder="Ex: Touche Magique")
            t_a = st.radio("Catégorie", ["Coiffure", "Institut"], horizontal=True)
            w_a = st.text_input("Numéro WhatsApp Salon", placeholder="70000000")
            img_a = st.text_input("Lien Photo Principale (i.ibb.co URL)", placeholder="https://i.ibb.co/...")
            vid_a = st.text_input("Lien Vidéo de présentation (YouTube URL)", placeholder="https://youtube.com/...")
            
            if st.form_submit_button("✅ PUBLIER LE PARTENAIRE"):
                if n_a and w_a:
                    st.session_state.base_salons[v_a][n_a] = {
                        "tel": w_a, "quartier": q_a, "type": t_a,
                        "photo": img_a, "video": vid_a, "gains": 0
                    }
                    st.toast("✅ Nouveau salon ajouté avec succès !", icon="⭐")
                else:
                    st.error("⚠️ Veuillez remplir au moins le Nom et le WhatsApp.")

# ==========================================
# ✨ ACCUEIL CLIENT (LE RÉSEAU FUSO BEAUTÉ) - MAGNIFIÉ
# ==========================================

# HEADER "WAHOU"
st.markdown("""
    <div class="waouh-header">
        <h1>Faso Beauté</h1>
        <p><i>by Blanco</i></p>
    </div>
    """, unsafe_allow_html=True)

# CARTES DE BIENVENUE (WAHOU ADDITION)
st.markdown("""
    <div class="welcome-card">
        <h3>✨ Bienvenue dans l'Excellence</h3>
        <p style="color: gray;">Sélectionnez votre ville et votre quartier ci-dessous pour découvrir l'élite de la coiffure et de l'institut de beauté au Burkina Faso.</p>
    </div>
    """, unsafe_allow_html=True)

# 1. Filtres Clients (CONSERVÉ)
col_v, col_q = st.columns(2)
with col_v:
    v_c = st.selectbox("📍 Choisissez votre ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with col_q:
    q_list_c = secteurs_bobo if v_c == "BOBO-DIOULASSO" else quartiers_ouaga
    q_c = st.selectbox("🏘️ Choisissez votre Quartier", q_list_c)

st.divider()

# 2. Affichage des Salons (CONSERVÉ)
salons_v = st.session_state.base_salons[v_c]
# Filtre intelligent selon quartier
salons_q = {n: s for n, s in salons_v.items() if s['quartier'] == q_c}

if salons_q:
    for nom, info in salons_q.items():
        st.markdown(f'<div class="salon-card">', unsafe_allow_html=True)
        
        c_title, c_type = st.columns([3, 1])
        with c_title:
            st.subheader(f"⭐ {nom.upper()}")
        with c_type:
            st.markdown(f'<span style="color: #1e7e34; font-weight: bold; float: right; padding-top: 5px;">{info["type"]}</span>', unsafe_allow_html=True)
        
        c1, c2 = st.columns([1, 2])
        with c1:
            if info['photo']: st.image(info['photo'], use_container_width=True)
            if info['video']: st.video(info['video'])
            if is_admin: # SEUL LE PATRON VOIT ÇA (CONSERVÉ)
                st.markdown(f'<div class="caisse-badge">💰 Gains : {info["gains"]} F</div>', unsafe_allow_html=True)
        
        with c2:
            st.write(f"📍 **Localisation :** {info['quartier']}")
            st.write(f"📞 **WhatsApp :** {info['tel']}")
            
            st.markdown("---")
            st.write("📝 **Formulaire de Réservation Directe**")
            
            # Formulaire de réservation (CONSERVÉ)
            nom_cli = st.text_input("Votre Nom complet", key=f"n_{nom}", placeholder="Entrez votre nom")
            
            if info['type'] == "Coiffure":
                presta = st.selectbox("Type de prestation", ["Coiffure Simple", "Mariage 💍 / Grand Event", "Tresses/Tissage", "Chignon Luxe"], key=f"p_{nom}")
            else:
                presta = st.selectbox("Type de prestation", ["Maquillage Pro 💄", "Soins de visage Profonds", "Pédicure Luxe / Manucure"], key=f"p_{nom}")
            
            c_d, c_h = st.columns(2)
            with c_d: jour_r = st.text_input("Jour souhaité", key=f"j_{nom}", placeholder="Ex: Samedi")
            with c_h: heure_r = st.text_input("Heure souhaitée", key=f"h_{nom}", placeholder="Ex: 10h30")

            if st.button(f"🚀 RÉSERVER CHEZ {nom.upper()}", key=f"b_{nom}"):
                if nom_cli and jour_r and heure_r:
                    # Gain de 100F automatique (CONSERVÉ)
                    st.session_state.base_salons[v_c][nom]['gains'] += 100
                    
                    # Message WhatsApp Automatique (CONSERVÉ)
                    msg = (f"Bonjour comment allez vous, je veux une réservation pour une {presta} "
                           f"le {jour_r} à {heure_r} pour la cliente {nom_cli} via Faso Beauté.")
                    
                    # Nettoyage numéro
                    num = info['tel'].replace(" ", "").replace("+", "")
                    num_f = f"226{num}" if not num.startswith("226") else num
                    url = f"https://wa.me/{num_f}?text={urllib.parse.quote(msg)}"
                    
                    st.balloons()
                    st.success("Réservation prête ! Cliquez ci-dessous pour l'envoyer instantanément.")
                    st.markdown(f'''<a href="{url}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:15px; border:none; height:50px; cursor:pointer; font-weight:bold; font-size: 16px;">📲 ENVOYER LA DEMANDE SUR WHATSAPP</button></a>''', unsafe_allow_html=True)
                else:
                    st.error("⚠️ Patron, il manque des infos pour valider la réservation et encaisser les 100F !")
        st.markdown('</div>', unsafe_allow_html=True)
else:
    st.markdown(f"""
        <div style="background: white; padding: 40px; border-radius: 20px; text-align: center; border: 1px solid #eee;">
            <p style="font-size: 20px; color: gray;">Bienvenue sur Faso Beauté.</p>
            <p style="color: gray;">Aucun salon n'est encore référencé à {q_c}.</p>
            <p style="color: #6c757d; font-size: 14px;">(L'Administrateur peut ajouter des partenaires via la barre latérale).</p>
        </div>
        """, unsafe_allow_html=True)

# FOOTER FINI (ADDITION DESIGN)
st.markdown("""
    <br><br>
    <div style="text-align: center; border-top: 1px solid #eee; padding-top: 20px;">
        <p style="color: gray; font-size: 14px;">Faso Beauté - Le Réseau de l'Elite</p>
        <p style="color: #6c757d; font-size: 12px;">Une marque by Blanco - Bobo & Ouaga Network © 2026</p>
    </div>
    """, unsafe_allow_html=True)
