import streamlit as st

# Configuration de la page
st.set_page_config(page_title="Blanco Coiffure", page_icon="✂️")

# Titre principal
st.title("✂️ Blanco Coiffure - IA")
st.subheader("Votre style, notre expertise.")

# Section de présentation
st.write("---")
st.markdown("### 💇‍♂️ Nos Services")
col1, col2 = st.columns(2)

with col1:
    st.info("*Coupe Homme*\n\nClassique, dégradé, barbe.")
with col2:
    st.success("*Soin Visage*\n\nNettoyage et massage.")

# Un bouton interactif pour tester
if st.button("Prendre rendez-vous"):
    st.balloons()
    st.write("✅ Redirection vers la prise de rendez-vous...")

# Contact
st.sidebar.title("Contact")
st.sidebar.write("📍 Bobo-Dioulasso, secteur 25")
st.sidebar.write("📞 Tél : +226 XX XX XX XX")
