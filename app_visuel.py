import streamlit as st
import urllib.parse

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Connect", page_icon="✨", layout="centered")

# --- DESIGN ÉLÉGANT ---
st.markdown("""
    <style>
    .stApp { background-color: #0e1117; color: white; }
    .stButton>button { width: 100%; border-radius: 12px; height: 3.5em; background: linear-gradient(45deg, #27ae60, #2ecc71); color: white; font-weight: bold; border: none; }
    .footer { text-align: center; color: gray; font-size: 12px; margin-top: 50px; }
    </style>
    """, unsafe_allow_html=True)

# --- BASE DE DONNÉES (ADMIN) ---
if 'base_salons' not in st.session_state:
    st.session_state.base_salons = {"BOBO-DIOULASSO": {}, "OUAGADOUGOU": {}}

# ==========================================
# 🛡️ ZONE ADMIN (ACCÈS DISCRET)
# ==========================================
with st.sidebar:
    st.header("⚙️ Gestion Blanco")
    code_admin = st.text_input("Code Secret", type="password")
    if code_admin == "Blanco.10":
        st.success("Accès Admin Activé")
        st.divider()
        with st.form("Ajout Salon"):
            v_adm = st.selectbox("Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
            n_adm = st.text_input("Nom de l'établissement")
            t_adm = st.radio("Type", ["Coiffure", "Institut"])
            q_adm = st.text_input("Secteur / Quartier")
            w_adm = st.text_input("WhatsApp (ex: 70000000)")
            p_adm = st.text_input("Lien Photo (URL)")
            v_adm_link = st.text_input("Lien Vidéo (URL)")
            
            if st.form_submit_button("✅ PUBLIER LE SALON"):
                if n_adm and w_adm and q_adm:
                    st.session_state.base_salons[v_adm][n_adm] = {
                        "tel": w_adm, "quartier": q_adm, "type": t_adm,
                        "photo": p_adm, "video": v_adm_link, "gains": 0
                    }
                    st.toast(f"Salon {n_adm} ajouté au réseau !")
                else:
                    st.error("Veuillez remplir les champs obligatoires.")
        
        # Affichage des gains (Seul l'admin voit ça ici)
        st.divider()
        st.subheader("📊 Comptabilité")
        for v in st.session_state.base_salons:
            for s, info in st.session_state.base_salons[v].items():
                st.write(f"**{s}** : {info['gains']} F CFA")

# ==========================================
# ✨ ZONE CLIENT (ACCUEIL)
# ==========================================
st.title("✨ BLANCO CONNECT ✨")
st.markdown("### *Réservez votre séance de beauté*")

# 1. Choix du Client
col1, col2 = st.columns(2)
with col1:
    v_cl = st.selectbox("📍 Votre Ville", ["BOBO-DIOULASSO", "OUAGADOUGOU"])
with col2:
    salons_v = st.session_state.base_salons[v_cl]
    quartiers = sorted(list(set([s['quartier'] for s in salons_v.values()]))) if salons_v else ["Aucun"]
    q_cl = st.selectbox("🏘️ Votre Quartier/Secteur", quartiers)

st.divider()

# 2. Liste des Salons filtrée
if salons_v:
    salons_q = {n: s for n, s in salons_v.items() if s['quartier'] == q_cl}
    
    if not salons_q:
        st.info("Sélectionnez votre quartier pour voir les salons disponibles.")
    
    for nom, info in salons_q.items():
        with st.container():
            st.markdown(f"#### ⭐ {nom}")
            # Affichage médias en "petit" comme demandé
            c_m1, c_m2 = st.columns([1, 2])
            with c_m1:
                if info['photo']: st.image(info['photo'], use_container_width=True)
                if info['video']: st.video(info['video'])
            
            with c_m2:
                st.write(f"📍 {info['quartier']} | 📞 WhatsApp associé : {info['tel']}")
                
                # Formulaire de réservation automatique
                nom_res = st.text_input("Votre Nom complet", key=f"n_{nom}")
                
                if info['type'] == "Coiffure":
                    pres_res = st.selectbox("Prestation", ["Coiffure Simple", "Mariage 💍", "Tresses"], key=f"p_{nom}")
                else:
                    pres_res = st.selectbox("Prestation", ["Maquillage 💄", "Soins de visage", "Manucure"], key=f"p_{nom}")
                
                col_d, col_h = st.columns(2)
                with col_d: d_res = st.text_input("Jour (ex: Samedi)", key=f"d_{nom}")
                with col_h: h_res = st.text_input("Heure (ex: 14h)", key=f"h_{nom}")

                if st.button(f"🚀 RÉSERVER CHEZ {nom.upper()}", key=f"b_{nom}"):
                    if nom_res and d_res and h_res:
                        # Enregistrement des 100F (invisible pour le client)
                        st.session_state.base_salons[v_cl][nom]['gains'] += 100
                        
                        # Message WhatsApp Automatique
                        texte = (f"Bonjour comment allez vous, je veux une réservation pour une {pres_res} "
                                 f"le {d_res} à {h_res} pour la cliente {nom_res} via Beauté Connect.")
                        
                        num = info['tel'].replace(" ", "").replace("+", "")
                        num_f = f"226{num}" if not num.startswith("226") else num
                        url = f"https://wa.me/{num_f}?text={urllib.parse.quote(texte)}"
                        
                        st.success("Réservation prête ! Cliquez pour envoyer.")
                        st.markdown(f'''<a href="{url}" target="_blank"><button style="background-color:#25D366; color:white; width:100%; border-radius:10px; border:none; height:45px; cursor:pointer; font-weight:bold;">📲 ENVOYER SUR WHATSAPP</button></a>''', unsafe_allow_html=True)
                    else:
                        st.error("⚠️ Veuillez remplir tous les champs du formulaire !")
            st.divider()
else:
    st.warning("Bienvenue ! Le Patron n'a pas encore ajouté de salons dans cette ville.")

st.markdown('<div class="footer">Blanco Connect © 2026 - Bobo & Ouaga Network</div>', unsafe_allow_html=True)
