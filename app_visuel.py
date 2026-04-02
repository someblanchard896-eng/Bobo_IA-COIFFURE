import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✂️", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #000000; color: white; font-weight: bold; }
    .salon-card { padding: 15px; border-radius: 10px; border: 1px solid #eee; margin-bottom: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTION WHATSAPP ---
def creer_lien_whatsapp(telephone, nom_salon, quartier):
    message = f"Bonjour, je souhaite réserver une séance chez {nom_salon} ({quartier}) via Blanco Beauté Connect."
    tel = str(telephone).replace(" ", "").replace("+", "")
    if not tel.startswith("226"): tel = "226" + tel
    return f"https://wa.me/{tel}?text={message.replace(' ', '%20')}"

# Initialisation DB
if 'salons_db' not in st.session_state:
    st.session_state.salons_db = []

# --- NAVIGATION ---
st.sidebar.title("✨ BLANCO BEAUTÉ")
menu = st.sidebar.selectbox("Menu", ["🏠 Accueil Clients", "🔐 Admin Blanco"])

# ================= PARTIE CLIENTS =================
if menu == "🏠 Accueil Clients":
    st.header("Réservez votre salon au Burkina")
    
    c_v, c_q = st.columns(2)
    with c_v:
        v_nom = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
    
    with c_q:
        if v_nom == "Bobo-Dioulasso":
            # LISTE COMPLÈTE BOBO (Sans parenthèses pour le 10)
            options_bobo = [
                "Secteur 1 (Dioulassoba)", "Secteur 2 (Dogona)", "Secteur 2 (Accart-ville)", 
                "Secteur 3 (Tounouma)", "Secteur 4 (Koko)", "Secteur 5 (Kyé)", 
                "Secteur 6 (Koua)", "Secteur 7 (Bolomakoté)", "Secteur 8 (Sikasso-Cira)", 
                "Secteur 9 (Sya/Kuin-Nima)", "Secteur 10 (Accart-ville Nord)", "Secteur 10 (Yéguéré)", 
                "Secteur 11 (Colma)", "Secteur 12 (Bolomakoté)", "Secteur 13 (Saint-Étienne)", 
                "Secteur 14 (Bindougousso)", "Secteur 15 (Ouezzin-Ville)", "Secteur 16 (Zone industrielle)",
                "Secteur 17 (Sarfalao)", "Secteur 20", "Secteur 21 (Colma)", "Secteur 22 (Belle-Ville)", 
                "Secteur 23", "Secteur 24", "Secteur 25", "Secteur 26", "Secteur 27", 
                "Secteur 30", "Secteur 31", "Secteur 32", "Secteur 33"
            ]
            s_nom = st.selectbox("Quartier / Secteur", options=sorted(options_bobo), index=None, placeholder="Cherchez votre secteur...")
        else:
            # LISTE COMPLÈTE OUAGA
            options_ouaga = [
                "Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Patte d'Oie", "Gounghin", 
                "Somgandé", "Karpala", "Cissin", "Larlé", "Koulouba", "Zogona", "Wemtenga", 
                "Kalgondin", "Rimkiéta", "Nagrin", "Saaba", "Hamdalaye", "Balkuy", "Secteur 30",
                "Bilbalogo", "Saint Léon", "Zanguettin", "Kamsonghin", "Samandin", "Ouidi"
            ]
            s_nom = st.selectbox("Quartier", options=sorted(options_ouaga), index=None, placeholder="Tapez le nom du quartier...")

    if s_nom:
        filtre = [s for s in st.session_state.salons_db if s['ville'] == v_nom and s['secteur'] == s_nom]
        
        if not filtre:
            st.info(f"📍 Aucun salon disponible au **{s_nom}** pour le moment.")
        else:
            for salon in filtre:
                st.markdown(f"### {salon['nom']}")
                col1, col2 = st.columns([1, 1])
                with col1:
                    if salon['photo']: st.image(salon['photo'], use_container_width=True)
                with col2:
                    if salon['video']: st.video(salon['video'])
                
                lien_wa = creer_lien_whatsapp(salon['tel'], salon['nom'], s_nom)
                st.markdown(f'''<a href="{lien_wa}" target="_blank"><button style="width:100%; height:50px; background-color:#25D366; color:white; border:none; border-radius:10px; cursor:pointer; font-weight:bold;">RESERVER VIA WHATSAPP</button></a>''', unsafe_allow_html=True)
                st.divider()

# ================= PARTIE ADMIN =================
# ================= PARTIE ADMIN (SÉCURISÉE) =================
elif menu == "🔐 Admin Blanco":
    st.header("🔐 Accès Restreint")
    
    # Demande du code secret
    code_entre = st.text_input("Entrez votre code d'accès :", type="password")
    
    if code_entre == "Blanco.10":
        st.success("Accès autorisé, Bienvenue Blanco !")
        
        # --- TON CONTENU ADMIN COMMENCE ICI ---
        with st.form("ajout"):
            c1, c2 = st.columns(2)
            with c1:
                n = st.text_input("Nom du Salon")
                v = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
                t = st.text_input("WhatsApp (ex: 70000000)")
            with c2:
                s = st.text_input("Secteur précis")
                b = st.number_input("Budget (F CFA)", value=100)
            
            p = st.file_uploader("Photo", type=['jpg','png','jpeg'])
            vid = st.file_uploader("Vidéo Pub", type=['mp4'])
            
            if st.form_submit_button("Valider l'ajout"):
                st.session_state.salons_db.append({"nom":n, "ville":v, "secteur":s, "tel":t, "budget":b, "photo":p, "video":vid})
                st.success("Salon ajouté avec succès !")

        # Affichage du budget total
        if st.session_state.salons_db:
            total = sum([s['budget'] for s in st.session_state.salons_db])
            st.metric("Total des Budgets collectés", f"{total} F CFA")
            st.table([{"Nom": x['nom'], "Quartier": x['secteur'], "Budget": x['budget']} for x in st.session_state.salons_db])
            
    elif code_entre != "" :
        st.error("Code incorrect. L'accès à la gestion des budgets est réservé.")
