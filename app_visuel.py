import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✨", layout="wide")

# --- STYLE ---
st.markdown("""
    <style>
    .main { background-color: #fafafa; }
    .stButton>button { width: 100%; border-radius: 10px; font-weight: bold; }
    .reservation-card { border: 1px solid #ddd; padding: 15px; border-radius: 10px; background: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES DES SECTEURS ---
options_bobo = [
    "Secteur 1 (Dioulassoba)", "Secteur 2 (Dogona)", "Secteur 2 (Accart-ville)", 
    "Secteur 3 (Tounouma)", "Secteur 4 (Koko)", "Secteur 5 (Kyé)", "Secteur 6 (Koua)", 
    "Secteur 7 (Bolomakoté)", "Secteur 8 (Sikasso-Cira)", "Secteur 9 (Sya/Kuin-Nima)", 
    "Secteur 10 (Accart-ville Nord)", "Secteur 10 (Yéguéré)", "Secteur 11 (Colma)", 
    "Secteur 12 (Bolomakoté)", "Secteur 13 (Saint-Étienne)", "Secteur 14 (Bindougousso)", 
    "Secteur 15 (Ouezzin-Ville)", "Secteur 17 (Sarfalao)", "Secteur 21 (Colma)", 
    "Secteur 22 (Belle-Ville)", "Secteur 24", "Secteur 25", "Secteur 31"
]

options_ouaga = [
    "Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Patte d'Oie", "Gounghin", 
    "Karpala", "Secteur 30", "Larlé", "Bilbalogo", "Saint Léon"
]

# --- FONCTION WHATSAPP ---
def obtenir_lien_wa(tel, nom_s, quartier, type_reservation):
    msg = f"Bonjour, je souhaite effectuer une Réservation {type_reservation} chez {nom_s} ({quartier}) via Blanco Beauté Connect."
    numero = str(tel).replace(" ", "").replace("+", "")
    if not numero.startswith("226"): numero = "226" + numero
    return f"https://wa.me/{numero}?text={msg.replace(' ', '%20')}"

# --- BASE DE DONNÉES ---
if 'salons_db' not in st.session_state:
    st.session_state.salons_db = []

# --- NAVIGATION ---
menu = st.sidebar.radio("MENU", ["🏠 ACCUEIL CLIENTS", "🔐 GESTION BLANCO"])

# ================= PARTIE CLIENTS =================
if menu == "🏠 ACCUEIL CLIENTS":
    st.header("✨ Salons de Coiffure & Beauté")
    
    col_v, col_q = st.columns(2)
    with col_v:
        v_nom = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
    with col_q:
        liste = sorted(options_bobo) if v_nom == "Bobo-Dioulasso" else sorted(options_ouaga)
        s_nom = st.selectbox("Quartier / Secteur", options=liste, index=None, placeholder="Cherchez votre quartier...")

    if s_nom:
        filtre = [s for s in st.session_state.salons_db if s['ville'] == v_nom and s['secteur'] == s_nom]
        if not filtre:
            st.info(f"📍 Aucun établissement disponible au *{s_nom}*.")
        else:
            for i, salon in enumerate(filtre):
                with st.container():
                    st.markdown(f"### {salon['nom']} — {salon['type']}")
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        if salon['photo']: st.image(salon['photo'], use_container_width=True)
                    with c2:
                        if salon['video']: st.video(salon['video'])
                    
                    # Choix du type de réservation par le client
                    type_res = st.radio(f"Type de prestation pour {salon['nom']} :", ["Simple", "Mariage"], key=f"type_{i}", horizontal=True)
                    
                    link = obtenir_lien_wa(salon['tel'], salon['nom'], s_nom, type_res)
                    
                    # BOUTON WHATSAPP
                    st.markdown(f'''
                        <a href="{link}" target="_blank" style="text-decoration: none;">
                            <div style="background-color: #25D366; color: white; text-align: center; padding: 12px; border-radius: 10px; font-weight: bold;">
                                💬 RÉSERVER ({type_res.upper()})
                            </div>
                        </a>
                    ''', unsafe_allow_html=True)
                    
                    if st.button(f"Confirmer réservation chez {salon['nom']}", key=f"conf_{i}"):
                        salon['revenu'] += 100
                        st.balloons()
                    st.divider()

# ================= PARTIE ADMIN =================
elif menu == "🔐 GESTION BLANCO":
    st.header("🔐 Administration")
    pwd = st.text_input("Code secret :", type="password")
    
    if pwd == "Blanco.10":
        st.success("Bienvenue Blanco")
        with st.expander("Ajouter un Établissement Coiffure & Beauté"):
            with st.form("add_form"):
                n = st.text_input("Nom de l'établissement")
                t_cat = st.selectbox("Catégorie", ["Salon de Coiffure", "Institut de Beauté", "Espace Mariage & Esthétique", "Mixte"])
                v = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
                liste_admin = sorted(options_bobo) if v == "Bobo-Dioulasso" else sorted(options_ouaga)
                s = st.selectbox("Secteur exact", options=liste_admin)
                tel = st.text_input("Numéro WhatsApp")
                p = st.file_uploader("Image", type=['jpg','png','jpeg'])
                vid = st.file_uploader("Vidéo Pub", type=['mp4'])
                
                if st.form_submit_button("Enregistrer"):
                    st.session_state.salons_db.append({"nom":n,"type":t_cat,"ville":v,"secteur":s,"tel":tel,"photo":p,"video":vid,"revenu":0})
                    st.success("Salon ajouté !")

        if st.session_state.salons_db:
            st.subheader("💰 Revenus des Clics")
            total = sum([s['revenu'] for s in st.session_state.salons_db])
            st.metric("TOTAL GAIN", f"{total} F CFA")
            st.table([{"Nom": s['nom'], "Gains": f"{s['revenu']} F"} for s in st.session_state.salons_db])
