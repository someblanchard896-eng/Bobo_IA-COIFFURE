import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# --- CONFIGURATION ---
st.set_page_config(page_title="Blanco Beauté Connect", page_icon="✨", layout="wide")

# --- CONNEXION ---
# On utilise la connexion définie dans tes Secrets Streamlit
conn = st.connection("gsheets", type=GSheetsConnection)

def charger_donnees():
    try:
        # On lit les 7 colonnes exactes depuis l'onglet Salons
        data = conn.read(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", ttl=0)
        return data
    except:
        # Si le tableau est vide ou inaccessible, on crée la structure parfaite
        return pd.DataFrame(columns=['nom', 'type', 'ville', 'secteur', 'tel', 'photo_url', 'revenus'])

def enregistrer_donnees(df):
    try:
        # On met à jour le Google Sheets
        conn.update(spreadsheet="Base_Blanco_Beaute", worksheet="Salons", data=df)
        st.success("✅ Enregistré avec succès dans le Cloud !")
    except Exception as e:
        st.error(f"⚠️ Erreur de connexion : {e}")

# --- CHARGEMENT DES DONNÉES ---
df_actuel = charger_donnees()

# --- INTERFACE ---
st.title("✂️ Administration Blanco")

with st.expander("➕ Ajouter un nouveau Salon"):
    with st.form("ajout_salon"):
        n = st.text_input("Nom du Salon")
        t = st.selectbox("Type", ["Coiffure Homme", "Coiffure Femme", "Institut Beauté", "Mariage"])
        v = st.selectbox("Ville", ["Bobo-Dioulasso", "Ouagadougou"])
        
        # Liste des secteurs pour Bobo (tu peux compléter la liste)
        s = st.selectbox("Secteur", ["Secteur 1", "Secteur 2", "Secteur 10 (Yéguéré)", "Secteur 21 (Colma)", "Secteur 22"])
        tel = st.text_input("WhatsApp (ex: 70000000)")
        
        if st.form_submit_button("Enregistrer"):
            if n and tel:
                # On prépare la ligne avec les 7 colonnes EXACTES du Google Sheets
                nouveau = pd.DataFrame([{
                    "nom": n, 
                    "type": t, 
                    "ville": v, 
                    "secteur": s, 
                    "tel": tel, 
                    "photo_url": "", 
                    "revenus": 0
                }])
                
                # Fusion des données
                df_final = pd.concat([df_actuel, nouveau], ignore_index=True)
                
                # Envoi vers Google
                enregistrer_donnees(df_final)
                st.balloons()
                st.rerun()
            else:
                st.warning("Veuillez remplir au moins le nom et le téléphone.")

# --- AFFICHAGE DU TABLEAU ---
if not df_actuel.empty:
    st.divider()
    st.subheader("📊 Suivi de tes salons")
    
    # Calcul du total (on s'assure que 'revenus' est bien un nombre)
    df_actuel['revenus'] = pd.to_numeric(df_actuel['revenus'], errors='coerce').fillna(0)
    total = df_actuel['revenus'].sum()
    
    st.metric("TOTAL COLLECTÉ", f"{total} F CFA")
    st.table(df_actuel[['nom', 'secteur', 'tel', 'revenus']])
