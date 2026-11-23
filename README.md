<div align="center">

# Portfolio Notes

*An investment portfolio dashboard by Debora Barboza*

</div>

I started this project because I wanted to explore how different investments can affect a portfolio over time. I was especially curious about the relationship between returns and risk, and how changing the allocation could change the results.

I built a small interactive dashboard in Python using Streamlit, Pandas, NumPy and Plotly. It lets you adjust the allocation between four fictional funds and explore the results through charts and financial indicators.

<div align="center">

### Tools I used

![Python](https://img.shields.io/badge/Python-E9E4F4?style=flat-square&logo=python&logoColor=62567B)
![Streamlit](https://img.shields.io/badge/Streamlit-F1DFE9?style=flat-square&logo=streamlit&logoColor=805B71)
![Pandas](https://img.shields.io/badge/Pandas-DFEAF2?style=flat-square&logo=pandas&logoColor=526F86)
![NumPy](https://img.shields.io/badge/NumPy-E1EEE5?style=flat-square&logo=numpy&logoColor=456B55)
![Plotly](https://img.shields.io/badge/Plotly-F7EACB?style=flat-square&logo=plotly&logoColor=806A36)

</div>

### What you can explore

The dashboard shows total return, annualized return, annualized volatility and maximum drawdown. It also includes a portfolio growth chart, an allocation chart, a comparison of the fictional funds and a drawdown chart.

The sliders let you try different allocations. The weights are automatically normalized so they add up to 100%.

### Running it on your computer

You will need Python installed. Open a terminal in the project folder and run:

```bash
python -m pip install -r requirements.txt
python -m streamlit run app.py
```

Streamlit will provide a local address to open the dashboard in your browser.

### A note about the data

I used simulated prices rather than live market data so that the project is easy to reproduce. The four funds are fictional. Their daily returns are generated with a fixed random seed, so the example is consistent each time it runs.

The calculations assume daily rebalancing and do not include fees, taxes, inflation or trading costs. This dashboard is an educational exercise, not investment advice.

### What I learned

This project helped me practice working with time series, calculating financial indicators and turning data into interactive visualizations. It also gave me a better understanding of how allocation decisions can affect both returns and risk.

<div align="center">

[LinkedIn](https://www.linkedin.com/in/deborajbarboza)

</div>
