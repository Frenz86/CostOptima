import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from sklearn.linear_model import LinearRegression

# Configurazione Pagina
st.set_page_config(page_title="CostOptima 360", layout="wide")

# --- TITOLO E SIDEBAR ---
st.title("📊 CostOptima 360 - Toolkit Analisi Costi")
st.markdown("Basato sul documento *15 Essential Cost Analytics Tools*")

st.sidebar.header("Navigazione Moduli")

def main():
    module = st.sidebar.radio(
                                "Scegli la Fase Analitica:",
                                ["1. Descriptive (Stato Attuale)", 
                                "2. Exploratory (Pattern)", 
                                "3. Predictive (Futuro)", 
                                "4. Prescriptive (Decisioni)"]
                            )

    # --- GENERAZIONE DATI SIMULATI (B&O Style) ---
    np.random.seed(42)
    dates = pd.date_range(start="2023-01-01", periods=12, freq="ME")
    sales = np.array([100, 120, 130, 150, 160, 180, 200, 210, 230, 250, 270, 300]) * 1000
    cogs = sales * 0.45 + np.random.normal(0, 5000, 12)  # 45% COGS
    opex = sales * 0.21 + 20000 # Costi fissi base + variabili
    total_costs = cogs + opex

    df = pd.DataFrame({
                        'Date': dates,
                        'Sales': sales,
                        'COGS': cogs,
                        'OpEx': opex,
                        'Total_Costs': total_costs
                        })

    # ==============================================================================
    # MODULO 1: DESCRIPTIVE ANALYTICS
    # ==============================================================================
    if "1. Descriptive" in module:
        st.header("1. Descriptive Analytics: Dove vanno i soldi?")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Tool #1: Cost Structure Analysis")
            # Calcolo simulato come da PDF
            fixed_part = df['Total_Costs'].sum() * 0.31
            variable_part = df['Total_Costs'].sum() * 0.69
            
            fig_pie = px.pie(
                names=['Fixed Costs (31%)', 'Variable Costs (69%)'],
                values=[fixed_part, variable_part],
                title="Struttura Costi (Fissi vs Variabili)",
                color_discrete_sequence=['#EF553B', '#636EFA']
            )
            st.plotly_chart(fig_pie, width='stretch')

        with col2:
            st.subheader("Tool #2: Variance Analysis")
            # Simulazione Budget vs Actual
            budget_cogs = 1000000
            actual_cogs = 1150000
            variance = actual_cogs - budget_cogs
            var_pct = (variance / budget_cogs) * 100
            
            st.metric(label="COGS Actual", value=f"${actual_cogs:,.0f}")
            st.metric(label="COGS Budget", value=f"${budget_cogs:,.0f}")
            st.metric(
                label="Varianza (Sfavorevole)", 
                value=f"${variance:,.0f}", 
                delta=f"{var_pct:.1f}%",
                delta_color="inverse" # Rosso se positivo (costi più alti)
            )
            st.info("⚠️ I costi sono superiori al budget del 15%. Indagare 'Price Variance'.")

    # ==============================================================================
    # MODULO 2: EXPLORATORY ANALYTICS
    # ==============================================================================
    elif "2. Exploratory" in module:
        st.header("2. Exploratory Analytics: Relazioni e Driver")
        
        tab1, tab2 = st.tabs(["Tool #5: Regressione", "Tool #7: Correlazione"])
        
        with tab1:
            st.subheader("Regression Analysis (Costi vs Vendite)")
            st.write("Identifichiamo la parte fissa e variabile dei costi usando i dati storici.")
            
            # Modello di Regressione Lineare
            X = df[['Sales']]
            y = df['Total_Costs']
            model = LinearRegression()
            model.fit(X, y)
            
            fixed_cost_calc = model.intercept_
            var_rate = model.coef_[0]
            r2 = model.score(X, y)
            
            c1, c2, c3 = st.columns(3)
            c1.metric("Costi Fissi (Intercept)", f"${fixed_cost_calc:,.0f}")
            c2.metric("Costo Variabile per $1 Vendita", f"${var_rate:.2f}")
            c3.metric("R-Squared (Precisione)", f"{r2:.2%}")
            
            # Grafico Scatter + Trendline
            fig_reg = px.scatter(df, x='Sales', y='Total_Costs', trendline="ols",
                                title="Analisi di Regressione: Forte relazione lineare")
            st.plotly_chart(fig_reg, width='stretch')
            
        with tab2:
            st.subheader("Correlation Matrix")
            corr = df[['Sales', 'COGS', 'OpEx', 'Total_Costs']].corr()
            fig_corr = px.imshow(corr, text_auto=True, aspect="auto", color_continuous_scale='RdBu_r',
                                title="Matrice di Correlazione (Heatmap)")
            st.plotly_chart(fig_corr, width='stretch')

    # ==============================================================================
    # MODULO 3: PREDICTIVE ANALYTICS
    # ==============================================================================
    elif "3. Predictive" in module:
        st.header("3. Predictive Analytics: Prevedere il Futuro")
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            st.subheader("Tool #12: Break-Even Calculator")
            # Input interattivi
            price = st.number_input("Prezzo Medio Unitario", value=100.0)
            var_cost = st.number_input("Costo Variabile Unitario", value=60.0)
            fixed_cost_input = st.number_input("Costi Fissi Totali", value=50000.0)
            
            if price > var_cost:
                bep_units = fixed_cost_input / (price - var_cost)
                st.success(f"📍 Break-Even Point: {int(bep_units)} unità")
            else:
                st.error("Il prezzo deve essere maggiore del costo variabile!")

        with col2:
            st.subheader("Break-Even Visualizer")
            # Generazione grafico BEP dinamico
            if price > var_cost:
                x_vals = np.linspace(0, bep_units * 2, 100)
                rev_vals = x_vals * price
                cost_vals = fixed_cost_input + (x_vals * var_cost)
                
                fig_be = go.Figure()
                fig_be.add_trace(go.Scatter(x=x_vals, y=rev_vals, name='Ricavi', line=dict(color='green')))
                fig_be.add_trace(go.Scatter(x=x_vals, y=cost_vals, name='Costi Totali', line=dict(color='red')))
                fig_be.add_vline(x=bep_units, line_dash="dash", annotation_text="BEP")
                
                st.plotly_chart(fig_be, width='stretch')

        st.markdown("---")
        st.subheader("Tool #10: Scenario & Sensitivity Analysis")
        growth = st.slider("Scenario Crescita Vendite (%)", min_value=-20, max_value=30, value=10)
        
        projected_sales = df['Sales'].iloc[-1] * (1 + growth/100)
        projected_cost = (projected_sales * 0.67) + 965000 # Formula presa dall'esempio del PDF
        projected_margin = projected_sales - projected_cost
        
        c_s1, c_s2, c_s3 = st.columns(3)
        c_s1.metric("Vendite Previste", f"${projected_sales:,.0f}")
        c_s2.metric("Costi Previsti", f"${projected_cost:,.0f}")
        c_s3.metric("Margine Stimato", f"${projected_margin:,.0f}", 
                    delta_color="normal" if projected_margin > 0 else "inverse")

    # ==============================================================================
    # MODULO 4: PRESCRIPTIVE ANALYTICS
    # ==============================================================================
    elif "4. Prescriptive" in module:
        st.header("4. Prescriptive Analytics: Cosa dovremmo fare?")
        
        st.subheader("Tool #15: Decision Tree Analysis (EMV)")
        st.markdown("Valutazione delle opzioni basata sul Valore Monetario Atteso (EMV - Expected Monetary Value).")
        
        # Dati dall'esempio del PDF
        col_a, col_b, col_c = st.columns(3)
        
        with col_a:
            st.info("Opzione A: Investire Subito")
            st.write("Alto rischio, alto potenziale.")
            emv_a = 140000
            st.metric("EMV", f"${emv_a:,.0f}")
            
        with col_b:
            st.warning("Opzione B: Non Investire")
            st.write("Nessun rischio, guadagno basso.")
            emv_b = 45000
            st.metric("EMV", f"${emv_b:,.0f}")
            
        with col_c:
            st.success("Opzione C: Test First (Consigliata)")
            st.write("Fare un test pilota prima.")
            emv_c = 195000
            st.metric("EMV", f"${emv_c:,.0f}", delta="Best Choice")

        # Visualizzazione Grafica
        decisions = ['Investire', 'Non Investire', 'Test Pilot (Winner)']
        values = [140000, 45000, 195000]
        
        fig_tree = px.bar(x=decisions, y=values, color=decisions, 
                        title="Confronto Decisionale (EMV)",
                        labels={'y': 'Expected Monetary Value ($)', 'x': 'Opzioni'})
        st.plotly_chart(fig_tree, width='stretch')
        
        st.markdown("""
        **Prescrizione Automatica:**  
        Il sistema suggerisce di procedere con l'opzione **Test First**. Sebbene ritardi il lancio completo, riduce l'incertezza e massimizza il valore atteso di $55k rispetto all'investimento diretto.
        """)

if __name__ == "__main__":
    main()