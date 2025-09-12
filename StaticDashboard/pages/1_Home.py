import streamlit as st
import yfinance as yf
import pandas as pd
import datetime
import mplfinance as mpf

# ─── Layout ─────────────────────────────────────────────────────────────────────
st.title("Intraday Market Overview")

# ─── Index ETFs to Display ──────────────────────────────────────────────────────
INDICES = {
    "S&P 500": "SPY",
    "Nasdaq": "QQQ",
    "Dow Jones": "DIA"
}

# ─── mplfinance Dark Style ──────────────────────────────────────────────────────
mc = mpf.make_marketcolors(
    up   = "#00ff9f",
    down = "#ff1744",
    edge = "#ffffff",
    wick = "#aaaaaa",
    volume="in",
    inherit=True
)
style = mpf.make_mpf_style(
    base_mpl_style="dark_background",
    marketcolors=mc,
    gridcolor="#444444",
    gridstyle="-",
    facecolor="000000",
    edgecolor="000000",
    figcolor="black",
    rc={"grid.linewidth": 0.4}
)

# ─── Display Helpers ─────────────────────────────────────────────────────────────
def display_metric(ticker: str, name: str):
    hist = yf.Ticker(ticker).history(period='2d')
    if len(hist) < 2:
        st.write(f"Not enough data for {name}")
        return
    prev = hist['Close'].iloc[-2]
    last = hist['Close'].iloc[-1]
    ch = last - prev
    pct = ch / prev * 100
    st.metric(label=name, value=f"{last:.2f}", delta=f"{ch:+.2f} ({pct:+.2f}%)")


def plot_intraday(ticker: str, name: str, container):
    df = yf.Ticker(ticker).history(period='1d', interval='15m')
    if df.empty:
        container.write(f"No intraday data for {name}")
        return
    # Prepare DataFrame for mplfinance
    df = df.rename(columns={'Open':'Open','High':'High','Low':'Low','Close':'Close','Volume':'Volume'})
    fig, _ = mpf.plot(df, type='candle', style=style, title=f"{name} (15m)", returnfig=True)
    container.pyplot(fig)

# ─── Display ────────────────────────────────────────────────────────────────────
cols = st.columns(len(INDICES))
for col, (name, ticker) in zip(cols, INDICES.items()):
    with col:
        display_metric(ticker, name)
        plot_intraday(ticker, name, col)
