import streamlit as st

# Configure the main page
st.set_page_config(page_title="StaticDashboard", layout="wide", page_icon="🎯")
st.title("StaticDashboard")
st.markdown("Static Charting Dashboard.")



# Set up pages
home_page = st.Page("pages/1_Home.py", title="Home")
watchlist_page = st.Page("pages/2_Watchlist.py", title="Watchlist")
charting_page = st.Page("pages/3_Charting.py", title="Charting")
#options_page = st.Page("pages/4_Options.py", title="Options")
#backtesting_page = st.Page("pages/5_Backtesting.py", title="Backtesting")
#paper_trading_page = st.Page("pages/6_Paper_Trading.py", title="Paper Trading")
#live_trading_page = st.Page("pages/7_Live_Trading.py", title="Live Trading")
#data_scraper_page = st.Page("pages/7_Data_Scraper.py", title="Data Scraper/GPT")

# Navigation
pg = st.navigation([
    home_page,
    watchlist_page,
    charting_page,
    #options_page,
    #backtesting_page,
    #paper_trading_page,
    #live_trading_page,
    #data_scraper_page
])
pg.run()
