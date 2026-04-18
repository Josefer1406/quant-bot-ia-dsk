import streamlit as st
import requests
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

st.set_page_config(page_title="Quant Dashboard", layout="wide")
st.title("📊 Bot Quant Institucional - Dashboard")

BOT_URL = st.secrets.get("BOT_URL", "https://tu-bot.up.railway.app/data")

@st.cache_data(ttl=5)
def fetch_data():
    try:
        r = requests.get(BOT_URL, timeout=5)
        return r.json() if r.status_code == 200 else None
    except:
        return None

data = fetch_data()
if not data:
    st.error("No se pudo conectar al bot")
    st.stop()

# Métricas principales
col1, col2, col3, col4 = st.columns(4)
col1.metric("Capital Actual", f"${data['capital']:,.2f}", delta=f"${data['pnl']:,.2f}")
col2.metric("PnL %", f"{data['pnl_pct']:.2f}%")
col3.metric("Winrate", f"{data['winrate']:.1f}%")
col4.metric("Total Trades", data['total_trades'])

col1, col2, col3 = st.columns(3)
col1.metric("Promedio Ganador", f"{data['avg_win_pct']:.2f}%")
col2.metric("Promedio Perdedor", f"{data['avg_loss_pct']:.2f}%")
col3.metric("Mejor/Peor Trade", f"{data['best_trade_pct']:.2f}% / {data['worst_trade_pct']:.2f}%")

st.subheader("Posiciones Abiertas")
posiciones = data.get('posiciones', {})
if posiciones:
    df_pos = pd.DataFrame(posiciones).T
    cols_to_show = [c for c in ['entry', 'quantity', 'investment', 'stop_loss', 'take_profit'] if c in df_pos.columns]
    st.dataframe(df_pos[cols_to_show])
else:
    st.info("Sin posiciones")

st.subheader("Últimos Trades")
if data['historial']:
    df_hist = pd.DataFrame(data['historial'])
    if 'pnl' in df_hist.columns:
        df_hist['pnl_pct'] = df_hist['pnl'] * 100
        st.dataframe(df_hist[['symbol', 'entry', 'exit', 'pnl_pct', 'reason']])
    
    # Curva de equity
    equity = [data['capital_inicial']]
    for trade in data['historial']:
        if 'capital' in trade:
            equity.append(trade['capital'])
        else:
            equity.append(equity[-1])
    fig = go.Figure()
    fig.add_trace(go.Scatter(y=equity, mode='lines', name='Capital', line=dict(color='green', width=2)))
    fig.add_hline(y=data['capital_inicial'], line_dash="dash", line_color="gray", annotation_text="Capital Inicial")
    fig.update_layout(title="Evolución del Capital", xaxis_title="Trade #", yaxis_title="USD", height=400)
    st.plotly_chart(fig)
    
    # Distribución de PnL
    fig_hist = px.histogram(df_hist, x='pnl_pct', nbins=20, title="Distribución de PnL por Trade")
    fig_hist.add_vline(x=0, line_dash="dash", line_color="red")
    st.plotly_chart(fig_hist)
else:
    st.info("Aún no hay trades cerrados")