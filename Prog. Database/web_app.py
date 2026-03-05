import streamlit as st
import pandas as pd
import os
import google.generativeai as genai
from fpdf import FPDF

# --- 1. FUNZIONI UTILI ---
def genera_pdf(testo_ia):   
    pdf = FPDF()
    pdf.add_page()
    
    # Intestazione Professionale
    pdf.set_font("helvetica", "B", 16)
    pdf.cell(0, 10, "REPORT AZIENDALE ANALISI DATI", ln=True, align='C')
    pdf.line(10, 25, 200, 25) 
    pdf.ln(10)

    # Corpo del Report e formattazione stile Excel
    pdf.set_font("helvetica", size=11)
    
    for riga in testo_ia.split('\n'):
        riga = riga.strip()
        if not riga: 
            continue
            
        if '|' in riga: # Se la riga contiene i dati, disegna la tabella
            pdf.set_font("helvetica", "B", 11)
            pdf.cell(0, 8, riga, border=1, ln=True) 
        else: # Altrimenti testo normale
            pdf.set_font("helvetica", size=11)
            pdf.multi_cell(0, 7, riga)
            
    return pdf.output()

# --- 2. CONFIGURAZIONE ---
# Inserisci qui la tua API KEY reale
genai.configure(api_key="AIzaSyAvOgEprihX-ynw14z7ci-zP0xdhG8f3Gk")
model = genai.GenerativeModel('models/gemma-3-12b-it')

st.title("📊 Dashboard Vendite Aziendali")

# --- 3. CARICAMENTO DATI E INTERFACCIA ---
if os.path.exists("gestionale_vendite.csv"):
    df = pd.read_csv("gestionale_vendite.csv")
    df["Totale"] = df["Quantita"] * df["Prezzo_Unitario"]
    
    st.subheader("I tuoi dati attuali")
    st.dataframe(df, use_container_width=True)

    st.divider()
    st.subheader("🤖 Chiedi all'Assistente AI")
    
    domanda = st.text_input("Fai una domanda sui tuoi dati (es: Qual è il prodotto che rende di più?)")

    # Tutto il processo AI parte SOLO se l'utente fa una domanda
    if domanda:
        dati_testo = df.to_string(index=False)
        
        prompt = f"""
        Agisci come un analista dati. Genera un report professionale basato su questi dati:
        {dati_testo}
        
        Domanda dell'utente: {domanda}

        REGOLE RIGIDE:
        1. Inizia direttamente con le analisi. NON scrivere introduzioni.
        2. Per i dati tabellari usa questo formato esatto:
        PRODOTTO: [Nome] | QTA: [Qta] | TOTALE: [Valore] €
        """
        
        # Mostra il caricamento
        with st.spinner("L'IA sta elaborando la risposta..."):
            try:
                # Chiamata in streaming
                response = model.generate_content(prompt, stream=True)
                
                # Contenitore per l'effetto scrittura in tempo reale
                placeholder = st.empty()
                full_text = ""
                
                for chunk in response:
                    full_text += chunk.text
                    placeholder.info(full_text) 
                
                # Generazione PDF e Bottone (appaiono solo a fine scrittura)
                pdf_output = genera_pdf(full_text)
                st.download_button(
                    label="📄 Scarica Report in PDF",
                    data=bytes(pdf_output),
                    file_name="Report_Analisi.pdf",
                    mime="application/pdf"
                )
                    
            except Exception as e:
                errore_str = str(e)
                if "429" in errore_str:
                    st.warning("⚠️ **I server sono carichi o hai esaurito la quota.** Attendi un minuto e riprova.")
                elif "404" in errore_str:
                    st.error("🚫 **Errore 404: Modello non trovato.** Verifica il nome del modello nel codice.")
                else:
                    st.error(f"Si è verificato un errore imprevisto: {e}")
else:
    st.error("File 'gestionale_vendite.csv' non trovato. Assicurati di aver salvato dei dati dal programma principale.")