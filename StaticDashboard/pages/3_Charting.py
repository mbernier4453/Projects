import streamlit as st
import yfinance as yf
import pandas as pd
import mplfinance as mpf
import numpy as np
from matplotlib.lines import Line2D

# ─── Color palettes for moving averages ─────────────────────────────────────────
sma_colors = ["#00ff9f", "#ff1744", "#f8f8f2", "#ff3636", "#8be9fd", "#33ffcc", "#ff6699", "#dddddd", "#ffaa00", "#9999ff"]
ema_colors = ["#ff79c6", "#bd93f9", "#50fa7b", "#ffb86c", "#ff5555", "#66ff66", "#ff3333", "#66ccff", "#ffcc00", "#ff66ff"]
hma_colors = ["#ff00ff", "#00ffff", "#ff8800", "#ff4444", "#ccff00", "#00cccc", "#cc0066", "#ffcc99", "#66ffcc", "#ccff33"]
allowed_periods = [5, 10, 20, 30, 40, 50, 60]

# ─── Helper functions ───────────────────────────────────────────────────────────────
def WMA(series, period):
    weights = np.arange(1, period + 1)
    return series.rolling(period).apply(lambda x: np.dot(x, weights) / weights.sum(), raw=True)

def HMA(series, period):
    half = int(period / 2)
    sq = int(np.sqrt(period))
    wma_half = WMA(series, half)
    wma_full = WMA(series, period)
    diff = 2 * wma_half - wma_full
    return WMA(diff, sq)

st.title("Charting")

# ─── Mode selector ─────────────────────────────────────────────────────────────────
mode = st.sidebar.selectbox("Chart mode", ["Single Ticker", "Watchlist"])

# ─── Initialize session state ─────────────────────────────────────────────────────────
for key in ("active_sma", "active_ema", "active_hma"):  
    if key not in st.session_state:
        st.session_state[key] = []

# ─── Determine tickers based on mode ───────────────────────────────────────────────
tickers = []
if mode == "Single Ticker":
    ticker = st.sidebar.text_input("Ticker (e.g. AAPL)").upper().strip()
    if not ticker:
        st.warning("Please enter a ticker.")
        st.stop()
    tickers = [ticker]
    # Snapshot metric
    snap = yf.download(ticker, period="2d", interval="1d", auto_adjust=False, actions=False)
    if snap.empty:
        st.warning(f"No data for {ticker}.")
        st.stop()
    if isinstance(snap.columns, pd.MultiIndex): snap.columns = snap.columns.droplevel(1)
    snap.dropna(subset=["Open","High","Low","Close"], inplace=True)
    last, prev = snap["Close"].iloc[-1], snap["Close"].iloc[-2]
    ch = last - prev
    pct = (ch / prev) * 100
    st.metric(label=ticker, value=f"{last:.2f} USD", delta=f"{ch:+.2f} ({pct:+.2f}%)")
else:
    watchlists = st.session_state.get("watchlists", {})
    if not watchlists:
        st.warning("No watchlists available.")
        st.stop()
    sel = st.sidebar.selectbox("Select a watchlist", [""] + list(watchlists.keys()))
    if not sel:
        st.warning("Please select a watchlist.")
        st.stop()
    tickers = watchlists.get(sel, [])
    if not tickers:
        st.warning(f"'{sel}' is empty.")
        st.stop()

# ─── Sidebar: Moving Averages via multiselect ───────────────────────────────────────
st.sidebar.header("Moving Averages")
sma = st.sidebar.multiselect("SMA periods", allowed_periods, default=st.session_state.active_sma)
ema = st.sidebar.multiselect("EMA periods", allowed_periods, default=st.session_state.active_ema)
hma = st.sidebar.multiselect("HMA periods", allowed_periods, default=st.session_state.active_hma)
# update session
st.session_state.active_sma = sma
st.session_state.active_ema = ema
st.session_state.active_hma = hma

# ─── Sidebar: Other Indicators Form ────────────────────────────────────────────────
with st.sidebar.form("other_indicator_form"):
    st.subheader("Other Indicators")
    boll = st.checkbox("Bollinger Bands", value=False)
    if boll:
        bb_w = st.selectbox("BB window", [5,10,20,50], index=2)
        bb_s = st.slider("BB stddev", 1.0,3.0,2.0,0.1)
    sr = st.checkbox("Support/Resistance", value=False)
    if st.form_submit_button("Apply Indicators"):
        opts = {"bollinger": boll, "support_resistance": sr}
        if boll:
            opts.update({"bb_window": bb_w, "bb_std": bb_s})
        st.session_state.indicator_options = opts

opts = st.session_state.get("indicator_options", {})

# ─── Timeframe / Interval ───────────────────────────────────────────────────────────
interval_map = {
    "5Y / Monthly":("5y","1mo"), "2Y / Weekly":("2y","1wk"), "1Y / Daily":("1y","1d"),
    "3M / Daily":("3mo","1d"),   "6M / 4H": ("6mo","4h"),  "1M / 4H": ("1mo","4h"),
    "1M / 1H": ("1mo","1h"),    "5D / 30m":("5d","30m"), "1D / 15m":("1d","15m"),
    "1D / 5m": ("1d","5m")
}
period, interval = interval_map[st.sidebar.selectbox("Timeframe / Interval", list(interval_map.keys()))]

# ─── Plot function ──────────────────────────────────────────────────────────────────
def plot_chart(tkr, per, intr, opts, sma_list, ema_list, hma_list):
    df = yf.download(tkr, period=per, interval=intr, auto_adjust=False, actions=False)
    if df.empty:
        st.warning(f"No data for {tkr}.")
        return
    if isinstance(df.columns, pd.MultiIndex): df.columns = df.columns.droplevel(1)
    df.dropna(subset=["Open","High","Low","Close"], inplace=True)
    addplots, lines, labs = [], [], []
    for idx, p in enumerate(sma_list):
        s = df["Close"].rolling(p).mean(); c = sma_colors[idx % len(sma_colors)]
        addplots.append(mpf.make_addplot(s, color=c, width=0.5)); lines.append(Line2D([0],[0],linewidth=0.5,color=c)); labs.append(f"SMA({p})")
    for idx, p in enumerate(ema_list):
        e = df["Close"].ewm(span=p, adjust=False).mean(); c = ema_colors[idx % len(ema_colors)]
        addplots.append(mpf.make_addplot(e, color=c, width=0.5)); lines.append(Line2D([0],[0],linewidth=0.5,color=c)); labs.append(f"EMA({p})")
    for idx, p in enumerate(hma_list):
        h = HMA(df["Close"], p); c = hma_colors[idx % len(hma_colors)]
        addplots.append(mpf.make_addplot(h, color=c, width=0.5)); lines.append(Line2D([0],[0], linewidth=0.5, color=c)); labs.append(f"HMA({p})")
    if opts.get("bollinger"):
        w, sd = opts.get("bb_window",20), opts.get("bb_std",2)
        ma = df["Close"].rolling(w).mean(); stdev = df["Close"].rolling(w).std()
        ub, lb = ma + sd*stdev, ma - sd*stdev
        addplots.extend([mpf.make_addplot(ub, color="purple", linestyle="--", width=0.5), mpf.make_addplot(ma, color="grey", linestyle="--", width=0.5), mpf.make_addplot(lb, color="purple", linestyle="--", width=0.5)])
        lines.extend([Line2D([0],[0], linewidth=0.5, color="purple", linestyle="--"), Line2D([0],[0], linewidth=0.5, color="grey", linestyle="--")]); labs.extend(["BB Upper/Lower","BB SMA"])
    if opts.get("support_resistance"):
        w=30; sup, res = df["Close"].rolling(w).min().iloc[-1], df["Close"].rolling(w).max().iloc[-1]
        sup_s, res_s = pd.Series(sup, index=df.index), pd.Series(res, index=df.index)
        addplots.extend([mpf.make_addplot(sup_s, color="green", linestyle="--", width=0.5), mpf.make_addplot(res_s, color="red", linestyle="--", width=0.5)])
        lines.extend([Line2D([0],[0],color="green", linestyle="--", linewidth=0.5), Line2D([0],[0],color="red", linestyle="--", linewidth=0.5)]); labs.extend(["Support","Resistance"])
    mc = mpf.make_marketcolors(up="#00ff9f", down="#ff1744", edge="#ffffff", wick="#aaaaaa", inherit=True)
    style = mpf.make_mpf_style(base_mpl_style="dark_background", marketcolors=mc)
    fig, ax = mpf.plot(df, type="candle", style=style, addplot=addplots, volume=True, returnfig=True)
    if len(ax)>2:
        for bar in ax[2].patches: bar.set_edgecolor("none")
    ax[0].legend(lines, labs, loc='best', fontsize='small')
    st.pyplot(fig)

# ─── Render for each ticker ─────────────────────────────────────────────────────────
for tkr in tickers:
    st.subheader(tkr)
    plot_chart(tkr, period, interval, st.session_state.get("indicator_options", {}), st.session_state.active_sma, st.session_state.active_ema, st.session_state.active_hma)
