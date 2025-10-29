import streamlit as st
import gspread
from datetime import date

# === AUTENTICAZIONE GOOGLE ===
gc = gspread.service_account_from_dict(st.secrets["google"])

# === CONFIGURAZIONE GOOGLE SHEETS ===
GOOGLE_SHEET_NAME = "Spese_Ponte"
sheet = gc.open(GOOGLE_SHEET_NAME).sheet1

# === LISTE A TENDINA ===
fonti = ["", "CONTANTI", "BBVA", "ISYBANK", "REVOLUT", "PAYPAL"]
causali = [
    "Salute", "Spesa", "Affitto", "Benzina", "Bollette",
    "Manutenzione auto", "Abbonamenti", "Casa", "Cibo d'asporto", "Mobilità",
    "Tabacco", "Tempo libero", "Università", "Regali", "Ristorante",
    "Sport", "Gioco", "Investimenti", "Abbigliamento", "Vacanze",
    "Varie", "Voli"
]

# === UI ===
st.set_page_config(page_title="Gestione Spese", page_icon="💰", layout="centered")
st.title("💰 Gestione Entrate e Uscite (Google Sheet)")
st.markdown("Compila i campi per aggiungere una nuova riga nel foglio collegato.")

with st.form("form_spese"):
    col1, col2 = st.columns(2)
    data = col1.date_input("📅 Data", value=date.today())
    descrizione = col2.text_input("📝 Descrizione")

    col3, col4 = st.columns(2)
    entrate = col3.number_input("💰 Entrate (€)", min_value=0.0, format="%.2f")
    uscite = col4.number_input("💸 Uscite (€)", min_value=0.0, format="%.2f")

    col5, col6, col7 = st.columns(3)
    fonte = col5.selectbox("🏦 Fonte (opzionale)", fonti)
    storno = col6.selectbox("🔁 Storno (opzionale)", fonti)
    causale = col7.selectbox("📂 Causale", causali)

    submitted = st.form_submit_button("💾 Salva")

    if submitted:
        try:
            nuova_riga = [
                data.strftime("%d/%m/%Y"),
                entrate,
                uscite,
                descrizione,
                fonte,
                storno,
                causale
            ]
            sheet.append_row(nuova_riga)
            st.success("✅ Riga aggiunta correttamente su Google Sheets!")

        except Exception as e:
            st.error(f"❌ Errore durante il salvataggio: {e}")
