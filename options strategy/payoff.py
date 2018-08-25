import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import mibian
import pandas as pd
matplotlib.rc('font', family='AppleGothic')
#matplotlib.rc('font', family='NanumGothic')

matplotlib.rcParams['axes.unicode_minus'] = False

def long_call_payoff(sT, strike_price, premium, contracts=1, multiplier=1):
    pnl = np.where(sT > strike_price, sT - strike_price, 0) - premium
    return pnl * contracts * multiplier

def short_call_payoff(sT, strike_price, premium, contracts=1, multiplier=1):
    pnl = np.where(sT > strike_price, strike_price - sT, 0) + premium
    return pnl * contracts * multiplier

def long_put_payoff(sT, strike_price, premium, contracts=1, multiplier=1):
    pnl = np.where(sT < strike_price, strike_price - sT, 0) - premium
    return pnl * contracts * multiplier

def short_put_payoff(sT, strike_price, premium, contracts=1, multiplier=1):
    pnl = np.where(sT < strike_price, sT - strike_price, 0) + premium
    return pnl * contracts * multiplier

def vega_payoff(initial_IV, changed_IV, vega):
    return (initial_IV - changed_IV) * vega

def plot_spread(st, values, strike, fig, ax, label, style):
    ax.spines['bottom'].set_position('zero')
    ax.plot(st, values, label=label, linestyle=style)
    ax.plot(strike, 0, 'ro')
    ax.legend()
    ax.grid(True)
    ax.set_xlabel('stock price')
    ax.set_ylabel('P & L')
