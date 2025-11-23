# CostOptima 360 - Toolkit Analisi Costi

Applicazione Streamlit per l'analisi dei costi basata sui **15 Essential Cost Analytics Tools**.

## 🚀 Installazione e Avvio

### 1. Installa le dipendenze
```bash
pip install -r requirements.txt
```

### 2. Avvia l'applicazione
```bash
streamlit run costoptima_app.py
```

L'app si aprirà automaticamente nel browser all'indirizzo `http://localhost:8501`

## 📊 Moduli Disponibili

### 1. Descriptive Analytics (Stato Attuale)
- **Tool #1**: Cost Structure Analysis - Analisi della struttura dei costi (fissi vs variabili)
- **Tool #2**: Variance Analysis - Confronto budget vs actual con calcolo varianze

### 2. Exploratory Analytics (Pattern)
- **Tool #5**: Regression Analysis - Analisi di regressione per identificare costi fissi e variabili
- **Tool #7**: Correlation Matrix - Matrice di correlazione tra variabili di costo

### 3. Predictive Analytics (Futuro)
- **Tool #12**: Break-Even Calculator - Calcolatore del punto di pareggio interattivo
- **Tool #10**: Scenario & Sensitivity Analysis - Analisi di scenario con proiezioni

### 4. Prescriptive Analytics (Decisioni)
- **Tool #15**: Decision Tree Analysis - Analisi decisionale con Expected Monetary Value (EMV)

## 💡 Caratteristiche

- **Interfaccia interattiva** con navigazione modulare
- **Grafici dinamici** creati con Plotly
- **Dati simulati** basati sullo stile Bang & Olufsen
- **Calcoli in tempo reale** per Break-Even Point e analisi di scenario
- **Visualizzazioni professionali** per ogni tipo di analisi

## 🎯 Utilizzo

1. Seleziona un modulo dalla sidebar
2. Esplora gli strumenti disponibili per quella fase analitica
3. Interagisci con i parametri (nel modulo Predictive)
4. Analizza i risultati visualizzati nei grafici

## 📝 Note

L'applicazione utilizza dati simulati per scopi dimostrativi. Per utilizzare dati reali, modifica la sezione di generazione dati nel codice sorgente.
