import streamlit as st

st.set_page_config(page_title="Calcolo Scala ADI 2025", layout="wide")
st.title("📊 Calcolo Scala di Equivalenza ADI - 2025")

st.markdown("""
<style>
    .stDataFrame thead tr th {
        background-color: #f0f2f6;
    }
</style>
""", unsafe_allow_html=True)

st.markdown("""
Questa applicazione permette di calcolare la **Scala ADI** 2025 secondo i criteri indicati, tenendo conto di:
- Età del componente
- Presenza di disabilità grave / non autosufficienza
- Carichi di cura
- Disagio bio-psico-sociale
""")

# --- Funzioni di supporto ---
def calcola_punteggio(componente_index, eta, disabile, cura, disagio, minori_count):
    punteggio = 0
    descrizione = []

    if componente_index == 0:
        punteggio += 1.0
        descrizione.append("Adulto principale (1.00)")

    if disabile:
        punteggio += 0.5
        descrizione.append("Disabile grave (+0.50)")

    if eta == "Over 60":
        punteggio += 0.4
        descrizione.append("Over 60 (+0.40)")

    if cura:
        punteggio += 0.4
        descrizione.append("Carichi di cura (+0.40)")

    if disagio:
        punteggio += 0.3
        descrizione.append("Disagio bio-psico-sociale (+0.30)")

    if eta in ["Minore < 3 anni", "Minore (3-17)"]:
        if minori_count < 2:
            punteggio += 0.15
            descrizione.append("Minore (fino a 2) (+0.15)")
        else:
            punteggio += 0.10
            descrizione.append("Minore (oltre il 2°) (+0.10)")

    return punteggio, descrizione

# --- Componenti famiglia ---
with st.form("adi_form"):
    n_componenti = st.number_input("Numero componenti familiari", min_value=1, max_value=10, value=1)
    componenti = []

    for i in range(n_componenti):
        with st.expander(f"Componente #{i+1}", expanded=True):
            eta = st.selectbox("Età", ["Adulto (<60)", "Over 60", "Minore < 3 anni", "Minore (3-17)"], key=f"eta_{i}")
            disabile = st.checkbox("Disabile grave / Non autosufficiente", key=f"disabile_{i}")
            cura = st.checkbox("Con carichi di cura", key=f"cura_{i}")
            disagio = st.checkbox("Disagio bio-psico-sociale", key=f"disagio_{i}")
            componenti.append((eta, disabile, cura, disagio))

    submitted = st.form_submit_button("Calcola scala ADI")

if submitted:
    totale = 0
    minori_count = 0
    disabile_grave_presente = False
    riepilogo = []

    for i, (eta, disabile, cura, disagio) in enumerate(componenti):
        if eta in ["Minore < 3 anni", "Minore (3-17)"]:
            minori_count += 1

    minori_tmp = 0
    for i, (eta, disabile, cura, disagio) in enumerate(componenti):
        punteggio, descrizione = calcola_punteggio(i, eta, disabile, cura, disagio, minori_tmp)
        totale += punteggio
        if eta in ["Minore < 3 anni", "Minore (3-17)"]:
            minori_tmp += 1
        if disabile:
            disabile_grave_presente = True

        riepilogo.append({
            "Componente": i + 1,
            "Dettagli": ", ".join(descrizione),
            "Punteggio": round(punteggio, 2)
        })

    massimo = 2.3 if disabile_grave_presente else 2.2
    totale = min(totale, massimo)

    st.success(f"Scala ADI calcolata: {totale:.2f} (massimo consentito: {massimo})")

    st.markdown("### 🔍 Riepilogo componenti")
    st.dataframe(riepilogo, use_container_width=True)
