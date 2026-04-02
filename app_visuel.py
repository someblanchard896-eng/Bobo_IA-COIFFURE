import streamlit as st

# --- CONFIGURATION ET STYLE ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✂️", layout="wide")

st.markdown("""
    <style>
    .stButton>button { width: 100%; border-radius: 10px; background-color: #25D366; color: white; font-weight: bold; height: 50px; }
    .main { background-color: #fafafa; }
    </style>
    """, unsafe_allow_html=True)

# --- LISTES DES SECTEURS (COMMUNES CLIENT/ADMIN) ---
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
    "Karpala", "Secteur 30", "Larlé", "Bilbalogo", "Saint Léon", "Zanguettin"
]

# --- FONCTION WHATSAPP ---
def creer_lien_wa(tel, nom_s, quartier):
    msg = f"Bonjour, je souhaite réserver une séance chez {nom_s} ({quartier}) via Blanco Beauté."
    numero = str(tel).replace(" ", "").replace("+", "")
    if not numero.startswith("226"): numero = "226" + numero
    return f"https://wa.me/{numero}?text={msg.replace(' ', '%20')}"

# --- BASE DE DONNÉES TEMPORAIRE ---
if 'salons_db' not in st.session_state:
    st.session_state.salons_db = []

# --- NAVIGATION ---
menu = st.sidebar.radio("MENU", ["🏠 ACCUEIL CLIENTS", "🔐 GESTION BLANCO"])

# ================= PARTIE CLIENTS =================
if menu == "🏠 ACCUEIL CLIENTS":
    st.header("✨ Trouvez votre Salon de Coiffure")
    col_v, col_q = st.columns(2)
    with col_v:
        v_nom = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
    with col_q:
        liste = sorted(options_bobo) if v_nom == "Bobo-Dioulasso" else sorted(options_ouaga)
        s_nom = st.selectbox("Quartier / Secteur", options=liste, index=None, placeholder="Tapez pour chercher...")

    if s_nom:
        filtre = [s for s in st.session_state.salons_db if s['ville'] == v_nom and s['secteur'] == s_nom]
        if not filtre:
            st.info(f"📍 Aucun salon disponible au **{s_nom}**.")
        else:
            for i, salon in enumerate(filtre):
                st.subheader(f"💇‍♂️ {salon['nom']}")
                c1, c2 = st.columns([1, 1])
                with c1:
                    if salon['photo']: st.image(salon['photo'], use_container_width=True)
                with c2:
                    if salon['video']: st.video(salon['video'])
                if st.button(f"PRENDRE RENDEZ-VOUS (WhatsApp)", key=f"btn_{i}"):
                    salon['revenu'] += 100
                    link = creer_lien_wa(salon['tel'], salon['nom'], s_nom)
                    st.markdown(f'<meta http-equiv="refresh" content="0;URL={link}">', unsafe_allow_html=True)
                st.divider()

# ================= PARTIE ADMIN (SÉCURISÉE) =================
elif menu == "🔐 GESTION BLANCO":
    st.header("🔐 Espace Administrateur")
    pwd = st.text_input("Entrez votre code secret :", type="password")
    
    if pwd == "Blanco.10":
        st.success("Accès autorisé")
        with st.expander("Ajouter un nouveau Salon Partenaire", expanded=True):
            with st.form("add_form"):
                n = st.text_input("Nom du Salon")
                v = st.selectbox("Ville du salon", ["Bobo-Dioulasso", "Ouagadougou"])
                
                # --- LA SAISIE ASSISTÉE POUR TOI AUSSI ---
                liste_admin = sorted(options_bobo) if v == "Bobo-Dioulasso" else sorted(options_ouaga)
                s = st.selectbox("Sélectionnez le Secteur exact", options=liste_admin)
                
                t = st.text_input("WhatsApp (ex: 70000000)")
                p = st.file_uploader("Photo du Salon", type=['jpg','png','jpeg'])
                vid = st.file_uploader("Vidéo Pub", type=['mp4'])
                if st.form_submit_button("Enregistrer le salon"):
                    st.session_state.salons_db.append({"nom":n,"ville":v,"secteur":s,"tel":t,"photo":p,"video":vid,"revenu":0})
                    st.success(f"Le salon {n} a été ajouté au {s} !")

        if st.session_state.salons_db:
            st.subheader("💰 Suivi des Revenus (100 F / clic)")
            total_b = sum([s['revenu'] for s in st.session_state.salons_db])
            st.metric("TOTAL COLLECTÉ", f"{total_b} F CFA")
            res = [{"Salon": s['nom'], "Quartier": s['secteur'], "Clics": s['revenu']//100, "Gains": f"{s['revenu']} F"} for s in st.session_state.salons_db]
            st.table(res)
    elif pwd != "":
        st.error("Code incorrect.")
