"""A small portfolio dashboard built with reproducible example data."""

import numpy as np
import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Portfolio Notes | Debora Barboza", page_icon="📈", layout="wide")

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=EB+Garamond:wght@400;500;600&family=Inter:wght@400;500&display=swap');
html, body, [class*="css"], [data-testid="stApp"] {font-family: 'Inter', sans-serif;}
h1, h2, h3, [data-testid="stMetricLabel"] {font-family: 'EB Garamond', Georgia, serif !important; font-weight: 500 !important;}
h1 {text-align: center; color: #6E5D77; font-size: 2.65rem !important;}
h2, h3 {color: #756781;}
[data-testid="stApp"] {background-color: #FCFAF8;}
[data-testid="stMetric"] {background: #F1EDF4; border-radius: 12px; padding: 14px;}
.subtitle {text-align: center; color: #857C84; margin-bottom: 2rem;}
.note {background: #EAF1EC; padding: 12px 16px; border-radius: 8px; color: #455F50;}
</style>
""", unsafe_allow_html=True)

st.title("Portfolio Notes")
st.markdown('<p class="subtitle">An exploration of returns, risk and portfolio allocation · Debora Barboza</p>', unsafe_allow_html=True)
st.markdown('<div class="note">This is a learning project. All prices are simulated, not real market data or investment advice.</div>', unsafe_allow_html=True)

@st.cache_data
def make_prices():
    rng = np.random.default_rng(42)
    dates = pd.bdate_range('2023-01-02', periods=520)
    assets = {
        'Aurora Fund': (0.00035, 0.009),
        'Sage Fund': (0.00022, 0.006),
        'Lavender Fund': (0.00045, 0.013),
        'Cedar Fund': (0.00016, 0.004),
    }
    prices = pd.DataFrame(index=dates)
    for name, (mean, sigma) in assets.items():
        daily_returns = rng.normal(mean, sigma, len(dates))
        prices[name] = 100 * np.cumprod(1 + daily_returns)
    return prices

prices = make_prices()
st.sidebar.header('Build your portfolio')
st.sidebar.caption('Adjust the weights. They will be normalized to 100%.')
raw_weights = {asset: st.sidebar.slider(asset, 0, 100, 25, 5) for asset in prices.columns}
total_weight = sum(raw_weights.values())
if total_weight == 0:
    st.warning('Choose a weight above zero for at least one fund.')
    st.stop()
weights = pd.Series(raw_weights, dtype=float) / total_weight
st.sidebar.caption('Current allocation: ' + ', '.join(f'{name} {weight:.0%}' for name, weight in weights.items() if weight > 0))

returns = prices.pct_change().dropna()
portfolio_daily = returns.dot(weights)
portfolio_growth = (1 + portfolio_daily).cumprod()
portfolio_growth.iloc[0] = 1 + portfolio_daily.iloc[0]

cumulative_return = portfolio_growth.iloc[-1] - 1
annual_return = portfolio_growth.iloc[-1] ** (252 / len(portfolio_daily)) - 1
annual_volatility = portfolio_daily.std() * np.sqrt(252)
drawdown = portfolio_growth / portfolio_growth.cummax() - 1
max_drawdown = drawdown.min()

st.subheader('At a glance')
cols = st.columns(4)
for col, label, value in zip(cols, ['Total return', 'Annualized return', 'Annualized volatility', 'Maximum drawdown'], [cumulative_return, annual_return, annual_volatility, max_drawdown]):
    col.metric(label, f'{value:.2%}')

st.subheader('How the portfolio changed')
chart = pd.DataFrame({'Date': portfolio_growth.index, 'Portfolio value': portfolio_growth.values * 100})
fig = px.line(chart, x='Date', y='Portfolio value', color_discrete_sequence=['#9B86AA'])
fig.update_layout(plot_bgcolor='#FCFAF8', paper_bgcolor='#FCFAF8', yaxis_title='Value of an initial 100', xaxis_title='')
st.plotly_chart(fig, use_container_width=True)

left, right = st.columns(2)
with left:
    st.subheader('Your allocation')
    allocation = pd.DataFrame({'Fund': weights.index, 'Weight': weights.values})
    pie = px.pie(allocation[allocation.Weight > 0], names='Fund', values='Weight', hole=0.55, color_discrete_sequence=['#B5A3C7', '#A9C6B1', '#E7C6CD', '#C7D8E7'])
    pie.update_layout(paper_bgcolor='#FCFAF8')
    st.plotly_chart(pie, use_container_width=True)
with right:
    st.subheader('Individual funds')
    normalized = prices.div(prices.iloc[0]).mul(100).reset_index().rename(columns={'index': 'Date'})
    long_data = normalized.melt(id_vars='Date', var_name='Fund', value_name='Indexed value')
    comparison = px.line(long_data, x='Date', y='Indexed value', color='Fund', color_discrete_sequence=['#9B86AA', '#86AD9B', '#D6A9B7', '#91B6CF'])
    comparison.update_layout(plot_bgcolor='#FCFAF8', paper_bgcolor='#FCFAF8')
    st.plotly_chart(comparison, use_container_width=True)

st.subheader('Drawdown over time')
drawdown_chart = pd.DataFrame({'Date': drawdown.index, 'Drawdown (%)': drawdown.values * 100})
drawdown_fig = px.area(drawdown_chart, x='Date', y='Drawdown (%)', color_discrete_sequence=['#D6A9B7'])
drawdown_fig.update_layout(plot_bgcolor='#FCFAF8', paper_bgcolor='#FCFAF8')
st.plotly_chart(drawdown_fig, use_container_width=True)

with st.expander('How I calculated the numbers'):
    st.write('Daily returns are the percentage change between consecutive simulated prices. The portfolio daily return is the weighted sum of the funds’ daily returns. Total return is the compounded change over the sample. Annualized return uses 252 trading days per year. Annualized volatility is the standard deviation of daily portfolio returns multiplied by the square root of 252. Maximum drawdown is the largest percentage fall from a previous portfolio peak.')
    st.write('This model assumes daily rebalancing to the selected weights. It excludes fees, taxes, inflation and transaction costs. Simulated fund paths are independent and reproducible using a fixed random seed.')

st.caption('Made as a personal learning project by Debora Barboza. Example data only.')
