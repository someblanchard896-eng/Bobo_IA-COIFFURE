import streamlit as st

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✂️", layout="wide")

# --- STYLE PERSONNALISÉ ---
st.markdown("""
    <style>
    .main { background-color: #f5f5f5; }
    .stButton>button { width: 100%; border-radius: 20px; background-color: #000000; color: white; }
    .salon-card { padding: 20px; border-radius: 15px; border: 1px solid #ddd; background-color: white; margin-bottom: 20px; }
    </style>
    """, unsafe_allow_html=True)

# --- FONCTIONS UTILES ---
def creer_lien_whatsapp(telephone, nom_salon, secteur):
    message = f"Bonjour, je souhaite réserver une séance chez {nom_salon} ({secteur}) via Blanco Beauté Connect."
    tel = str(telephone).replace(" ", "").replace("+", "")
    return f"https://wa.me/{tel}?text={message.replace(' ', '%20')}"

# Initialisation de la base de données dans la session (en attendant ton fichier réel)
if 'salons_db' not in st.session_state:
    st.session_state.salons_db = []

# --- INTERFACE ---
st.sidebar.title("✨ BLANCO BEAUTÉ")
menu = st.sidebar.selectbox("Menu Navigation", ["🏠 Accueil Clients", "🔐 Administration Blanco"])

# ================= PARTIE ACCUEIL (POUR TES CLIENTS) =================
if menu == "🏠 Accueil Clients":
    st.header("Trouvez votre salon de coiffure idéal")
    
    col_v, col_s = st.columns(2)
    with col_v:
        v_nom = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
    
    with col_s:
        if v_nom == "Bobo-Dioulasso":
            options_bobo = [
                "Secteur 1 (Dioulassoba)", "Secteur 2 (Dogona)", "Secteur 4 (Koko)", 
                "Secteur 10 (Yéguéré)", "Secteur 11 (Colma)", "Secteur 15 (Ouezzin-Ville)",
                "Secteur 21", "Secteur 22", "Secteur 25", "Secteur 31"
            ]
            s_nom = st.selectbox("Quartier / Secteur", options=options_bobo, index=None, placeholder="Tapez ou choisissez...")
        else:
            options_ouaga = ["Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Karpala", "Patte d'Oie"]
            s_nom = st.selectbox("Quartier", options=options_ouaga, index=None, placeholder="Tapez le nom...")

    if s_nom:
        filtre = [s for s in st.session_state.salons_db if s['ville'] == v_nom and s['secteur'] == s_nom]
        
        if not filtre:
            st.info(f"📍 Aucun salon n'est encore inscrit au **{s_nom}**. Blanco arrive bientôt !")
        else:
            for salon in filtre:
                with st.container():
                    st.markdown(f"### 💇‍♂️ {salon['nom']}")
                    c1, c2 = st.columns([1, 1])
                    
                    with c1:
                        if salon['photo']:
                            st.image(salon['photo'], caption="Vue du salon", use_container_width=True)
                    
                    with c2:
                        if salon['video']:
                            st.video(salon['video'])
                        else:
                            st.warning("📺 Pas encore de vidéo publicitaire pour ce salon.")
                    
                    st.write(f"📍 **Localisation :** {salon['ville']} - {salon['secteur']}")
                    lien_wa = creer_lien_whatsapp(salon['tel'], salon['nom'], salon['secteur'])
                    st.markdown(f'<a href="{lien_wa}" target="_blank" style="text-decoration:none;"><button style="width:100%; padding:10px; border-radius:10px; background-color:#25D366; color:white; border:none; cursor:pointer; font-weight:bold;">RESERVER SUR WHATSAPP</button></a>', unsafe_allow_html=True)
                    st.divider()

# ================= PARTIE ADMIN (POUR TOI BLANCO) =================
elif menu == "🔐 Administration Blanco":
    st.header("🛠️ Gestion des Salons & Budgets")
    
    with st.expander("➕ Ajouter un nouveau salon partenaire", expanded=True):
        with st.form("form_admin"):
            col_a, col_b = st.columns(2)
            with col_a:
                n_salon = st.text_input("Nom du Salon")
                v_salon = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
                t_salon = st.text_input("Téléphone WhatsApp (ex: 22670000000)")
            with col_b:
                s_salon = st.text_input("Secteur / Quartier précis")
                b_salon = st.number_input("Budget Publicitaire alloué (ex: 100)", min_value=0, value=100)
            
            p_salon = st.file_uploader("Photo du salon (Image)", type=['jpg', 'png', 'jpeg'])
            v_pub = st.file_uploader("Vidéo publicitaire (Vidéo)", type=['mp4', 'mov', 'avi'])
            
            if st.form_submit_button("Enregistrer le Salon"):
                st.session_state.salons_db.append({
                    "nom": n_salon, "ville": v_salon, "secteur": s_salon, 
                    "tel": t_salon, "budget": b_salon, "photo": p_salon, "video": v_pub
                })
                st.success(f"Félicitations ! Le salon {n_salon} est maintenant en ligne.")

    # --- TABLEAU DE BORD DES REVENUS ---
    st.subheader("💰 Suivi de tes Budgets")
    if st.session_state.salons_db:
        total_budget = sum([s['budget'] for s in st.session_state.salons_db])
        st.metric("Total de tes budgets publicitaires", f"{total_budget} F CFA")
        
        # Affichage de la liste des salons pour l'admin
        st.table([{"Salon": s['nom'], "Secteur": s['secteur'], "Budget": f"{s['budget']} F"} for s in st.session_state.salons_db])
    else:
        st.write("Aucun salon enregistré pour le moment.")
