import streamlit as st
import datetime
import pandas as pd
import yfinance as yf
import os

# Initialize session state for watchlists
def init_watchlists():
    if 'watchlists' not in st.session_state:
        st.session_state.watchlists = {}

init_watchlists()

st.title("Watchlists")

# Create new watchlist
st.header("Create New Watchlist")
with st.form("create_watchlist"):
    name = st.text_input("Watchlist Name")
    tickers_raw = st.text_area("Tickers (comma-separated, e.g. AAPL, MSFT)")
    if st.form_submit_button("Save"):
        tickers = [t.strip().upper() for t in tickers_raw.split(',') if t.strip()]
        if not name:
            st.warning("Enter a name.")
        elif not tickers:
            st.warning("Enter tickers.")
        else:
            st.session_state.watchlists[name] = tickers
            st.success(f"Saved '{name}' with {len(tickers)} tickers.")

st.markdown("---")

st.header("My Watchlists")
if not st.session_state.watchlists:
    st.info("No watchlists yet.")
else:
    for wl_name, tickers in list(st.session_state.watchlists.items()):
        st.subheader(wl_name)
        rows = []
        for symbol in tickers:
            date_str = None
            o = c = v = None
            delta = None
            try:
                # Fetch last 2 days of data
                hist = yf.Ticker(symbol).history(period='2d')
                if len(hist) >= 2:
                    # Get latest session and previous close
                    latest = hist.iloc[-1]
                    prev = hist.iloc[-2]
                    date_str = latest.name.date().isoformat()
                    o = latest['Open']
                    c = latest['Close']
                    v = latest['Volume']
                    # % change from yesterday's close
                    prev_close = prev['Close']
                    if prev_close:
                        delta = round((c - prev_close) / prev_close * 100, 2)
                elif len(hist) == 1:
                    # Only one day available
                    latest = hist.iloc[-1]
                    date_str = latest.name.date().isoformat()
                    o = latest['Open']
                    c = latest['Close']
                    v = latest['Volume']
            except Exception:
                # If any error, leave values as None
                pass
            # Fallback date if none
            if not date_str:
                date_str = datetime.date.today().isoformat()
            rows.append({
                'Ticker': symbol,
                'Date': date_str,
                'Open': o,
                'Close': c,
                '% Change': delta,
                'Volume': v
            })
        df = pd.DataFrame(rows)
        st.dataframe(df)

        # Management controls
        with st.expander(f"Manage {wl_name}"):
            if tickers:
                rem = st.selectbox("Remove ticker", tickers, key=f"rem_{wl_name}")
                if st.button("Remove", key=f"btn_rem_{wl_name}"):
                    st.session_state.watchlists[wl_name] = [t for t in tickers if t != rem]
                    st.success(f"Removed {rem} from '{wl_name}'")
                    st.experimental_rerun()
            if st.button("Delete watchlist", key=f"del_{wl_name}"):
                del st.session_state.watchlists[wl_name]
                st.success(f"Deleted '{wl_name}'")
                st.experimental_rerun()
