import pandas as pd
import os

FILE_DB = "gestionale_vendite.csv"

def carica_dati():
    """Carica i dati o crea il file se manca."""
    if not os.path.exists(FILE_DB):
        print("File non trovato. Creazione di un nuovo database...")
        # Creiamo un DataFrame vuoto con le colonne corrette
        df_nuovo = pd.DataFrame(columns=["Data", "Prodotto", "Categoria", "Quantita", "Prezzo_Unitario"])
        df_nuovo.to_csv(FILE_DB, index=False)
        return df_nuovo
    
    return pd.read_csv(FILE_DB)

def aggiungi_riga(data, prodotto, categoria, qta, prezzo):
    """Aggiunge una nuova vendita al database."""
    df = carica_dati()
    if df is not None:
        # Creiamo la nuova riga
        nuova_vendita = {
            "Data": data,
            "Prodotto": prodotto,
            "Categoria": categoria,
            "Quantita": qta,
            "Prezzo_Unitario": prezzo
        }
        # La aggiungiamo al DataFrame
        df = pd.concat([df, pd.DataFrame([nuova_vendita])], ignore_index=True)
        # Salviamo su file
        df.to_csv(FILE_DB, index=False)
        print(f"Ottimo! {prodotto} aggiunto con successo.")

def mostra_report():
    """Mostra un riepilogo veloce."""
    df = carica_dati()
    if df is not None:
        # Creiamo una colonna calcolata al volo
        df["Totale"] = df["Quantita"] * df["Prezzo_Unitario"]
        print("\n--- STATO ATTUALE DEL GESTIONALE ---")
        print(df)
        print(f"\nIncasso Totale: {df['Totale'].sum()}€")
        
def filtra_per_categoria(categoria_cercata):
    """Mostra solo i prodotti di una specifica categoria."""
    df = carica_dati()
    if df is not None:
        # Filtriamo i dati (case-insensitive per evitare errori tra Hardware e hardware)
        risultato = df[df['Categoria'].str.lower() == categoria_cercata.lower()]
        
        if risultato.empty:
            print(f"\nNessun dato trovato per la categoria: {categoria_cercata}")
        else:
            print(f"\n--- RISULTATI PER {categoria_cercata.upper()} ---")
            print(risultato)

# --- TEST DELLE FUNZIONI ---
# Proviamo ad aggiungere qualcosa e vedere se il totale si aggiorna
aggiungi_riga("2026-03-05", "Tastiera Meccanica", "Accessori", 2, 90)
mostra_report()
while True:
    print("\n--- MENU GESTIONALE AI ---")
    print("1. Visualizza Report")
    print("2. Aggiungi Nuova Vendita")
    print("3. Filtra per categoria")
    print("4. Esci")
    
    scelta = input("Seleziona un'opzione: ")
    
    if scelta == "1":
        mostra_report()
    elif scelta == "2":
        # Chiediamo i dati all'utente
        p = input("Nome Prodotto: ")
        c = input("Categoria: ")
        q = int(input("Quantità: "))
        pr = float(input("Prezzo Unitario: "))
        # Usiamo la data di oggi (puoi anche scriverla a mano per ora)
        aggiungi_riga("2026-03-05", p, c, q, pr)
    elif scelta == "3":
        cat = input("Quale categoria vuoi filtrare? ")
        filtra_per_categoria(cat)
    elif scelta == "4":
        print("Chiusura del gestionale. Arrivederci!")
        break
    else:
        print("Opzione non valida, riprova.")

