import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- 1. CONFIGURATION DE LA PAGE ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✨", layout="wide")

# --- 2. CONNEXION SÉCURISÉE À GOOGLE SHEETS ---
# Utilise les secrets 'gsheets' définis dans ton tableau de bord Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    try:
        # Lecture de l'onglet 'Salons' avec le nom du fichier
        data = conn.read(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", ttl=0)
        return data
    except Exception as e:
        # Si erreur, on crée un tableau vide avec les 7 colonnes exactes
        return pd.DataFrame(columns=['nom', 'type', 'ville', 'secteur', 'tel', 'photo_url', 'revenus'])

def enregistrer_donnees(df):
    # Envoi des données vers Google Sheets
    conn.update(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", data=df)

# --- 3. CHARGEMENT INITIAL ---
df_actuel = charger_donnees()

# --- 4. MENU DE NAVIGATION ---
st.sidebar.title("💎 Menu Blanco")
menu = st.sidebar.radio("Navigation", ["🏠 Accueil Clients", "🔐 Gestion Blanco"])

# ================= PAGE ACCUEIL (PUBLIC) =================
if menu == "🏠 Accueil Clients":
    st.title("✨ Bienvenue chez Blanco Beauté")
    st.subheader("Les meilleurs salons de coiffure du Burkina")
    st.divider()
    
    if df_actuel.empty:
        st.info("Aucun salon n'est encore enregistré dans le système.")
    else:
        # Affichage des salons en liste
        for index, row in df_actuel.iterrows():
            with st.container():
                col1, col2 = st.columns([1, 4])
                with col2:
                    st.markdown(f"### 💈 {row['nom']}")
                    st.write(f"📍 **Ville :** {row['ville']} | **Secteur :** {row['secteur']}")
                    st.write(f"📞 **WhatsApp :** {row['tel']}")
                st.divider()

# ================= PAGE ADMIN (GESTION) =================
elif menu == "🔐 Gestion Blanco":
    pwd = st.sidebar.text_input("Code secret :", type="password")
    
    if pwd == "Blanco.10":
        st.header("👨‍💼 Espace Administration")
        
        with st.expander("➕ Ajouter un nouveau Salon"):
            with st.form("ajout_salon"):
                col_left, col_right = st.columns(2)
                with col_left:
                    n = st.text_input("Nom du Salon")
                    v = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
                with col_right:
                    t = st.selectbox("Type", ["Coiffure Homme", "Coiffure Femme", "Institut Beauté", "Mariage"])
                    tel = st.text_input("WhatsApp (ex: 70600000)")
                
                # --- LISTE COMPLÈTE DES SECTEURS ---
                if v == "Bobo-Dioulasso":
                    liste_secteurs = [
                        "Secteur 1 (Dioulassoba)", "Secteur 2 (Dogona)", "Secteur 2 (Accart-ville)", 
                        "Secteur 3 (Tounouma)", "Secteur 4 (Koko)", "Secteur 10 (Accart-ville Nord)", 
                        "Secteur 10 (Yéguéré)", "Secteur 17 (Sarfalao)", "Secteur 21 (Colma)", 
                        "Secteur 22 (Belle-Ville)", "Secteur 25"
                    ]
                else:
                    liste_secteurs = [
                        "Ouaga 2000", "Pissy", "Tampouy", "Dassasgho", "Patte d'Oie", 
                        "Gounghin", "Karpala", "Secteur 15", "Secteur 30"
                    ]
                s = st.selectbox("Choisir le Secteur", liste_secteurs)

                if st.form_submit_button("🚀 Enregistrer dans le Cloud"):
                    if n and tel:
                        # On crée la ligne avec les 7 colonnes pour Google Sheets
                        nouveau_salon = pd.DataFrame([{
                            "nom": n, 
                            "type": t, 
                            "ville": v, 
                            "secteur": s, 
                            "tel": tel, 
                            "photo_url": "", 
                            "revenus": 0
                        }])
                        
                        # Fusion avec les données existantes
                        df_final = pd.concat([df_actuel, nouveau_salon], ignore_index=True)
                        
                        try:
                            # Tentative d'enregistrement
                            enregistrer_donnees(df_final)
                            st.success(f"✅ Succès ! Le salon '{n}' a été ajouté.")
                            st.balloons()
                            st.rerun()
                        except Exception as error:
                            st.error(f"❌ Erreur Google : {error}")
                            st.info("Vérifiez que l'e-mail du robot est bien 'Éditeur' sur le fichier Google Sheets.")
                    else:
                        st.warning("Attention : Le nom et le téléphone sont obligatoires.")

        # --- TABLEAU DE SUIVI ---
        if not df_actuel.empty:
            st.divider()
            st.subheader("📊 Suivi de vos Gains")
            # Conversion sécurisée des revenus en nombres
            df_actuel['revenus'] = pd.to_numeric(df_actuel['revenus'], errors='coerce').fillna(0)
            total_gains = df_actuel['revenus'].sum()
            
            st.metric("TOTAL COLLECTÉ", f"{total_gains} F CFA")
            st.dataframe(df_actuel[['nom', 'ville', 'secteur', 'tel', 'revenus']], use_container_width=True)
    else:
        st.warning("Entrez le mot de passe dans la barre latérale pour accéder à la gestion.")
