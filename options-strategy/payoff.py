import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import matplotlib
import mibian
import pandas as pd
#matplotlib.rc('font', family='AppleGothic')
matplotlib.rc('font', family='NanumGothic')

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
    ax.plot(st, values, label=label, linestyle=style, linewidth=3)
    ax.plot(strike, 0, 'ro')
    ax.legend(loc="best")
    ax.grid(True)
    ax.set_xlabel('stock price')
    ax.set_ylabel('P & L')
    
def ironCondor(put_long, put_short, call_short, call_long, st_range):
    
    st = np.arange(st_range[0], st_range[1], st_range[2])
    total_payoff = np.zeros(st.shape)
    fig, ax = plt.subplots(figsize=(12,6))
    premium_sold = 0
    premium_bought = 0

    put_strike1, premium, contracts, multiplier = put_long
    
    payoff = long_put_payoff(st, put_strike1, premium, contracts, multiplier)
    plot_spread(st, payoff, put_strike1, fig, ax, 
                     'Strike {} put_long'.format(put_strike1),'--')
    total_payoff += payoff
    premium_bought += premium * contracts * multiplier

    put_strike2, premium, contracts, multiplier  = put_short

    payoff = short_put_payoff(st, put_strike2, premium, contracts, multiplier)
    plot_spread(st, payoff, put_strike2, fig, ax, 
                    'Strike {} put_short'.format(put_strike2),'--')
    total_payoff += payoff
    premium_sold += premium * contracts * multiplier

    call_strike1, premium, contracts, multiplier = call_short

    payoff = short_call_payoff(st, call_strike1, premium, contracts, multiplier)
    plot_spread(st, payoff, call_strike1, fig, ax, 
                    'Strike {} call_short'.format(call_strike1),'--')
    total_payoff += payoff
    premium_sold += premium * contracts * multiplier

    call_strike2, premium, contracts, multiplier = call_long

    payoff = long_call_payoff(st, call_strike2, premium, contracts, multiplier)
    plot_spread(st, payoff, call_strike2, fig, ax, 
                    'Strike {} call_long'.format(call_strike2),'--')
    total_payoff += payoff
    premium_bought += premium * contracts * multiplier
    
    net_premium = premium_sold - premium_bought
            
    for price, payoff in zip(st, total_payoff):
        if np.abs(payoff) < 0.5:
            if price < put_strike2:
                print("** break-even lower price ** : {:.01f}".format(price - payoff))
            if price > call_strike1:
                print("** break-even higher price ** : {:.01f}".format(price + payoff))
    
    plot_spread(st, total_payoff, call_strike2, fig, ax, 
                'Net Spread','-')

    plt.title('Iron Condor');

    print('Max Profit = {:,.2f}'.format(max(total_payoff)))
    print('Max Loss = {:,.2f}'.format(min(total_payoff)))
    print('Net Premium = {:,.2f}'.format(net_premium)) 
    print('    Premium sold = {:,.2f}'.format(premium_sold))
    print('    Premium bought = {:,.2f}'.format(premium_bought))

    strike_difference = call_strike2 - call_strike1
    #win_probability = 100 - net_premium / strike_difference * 100
    
    #print('Win Probability = {:.2f} %'.format(win_probability))

def DougleIronCondor(put_long, put_short, call_short, call_long, put_long2, put_short2, call_short2, call_long2, st_range):
    
    st = np.arange(st_range[0], st_range[1], st_range[2])
    total_payoff = np.zeros(st.shape)
    fig, ax = plt.subplots(figsize=(20,10))
    premium_sold = 0
    premium_bought = 0

    put_strike1, premium, contracts, multiplier = put_long
    
    payoff = long_put_payoff(st, put_strike1, premium, contracts, multiplier)
    plot_spread(st, payoff, put_strike1, fig, ax, 
                     'Strike {} put_long'.format(put_strike1),'--')
    total_payoff += payoff
    premium_bought += premium

    put_strike2, premium, contracts, multiplier = put_short

    payoff = short_put_payoff(st, put_strike2, premium, contracts, multiplier)
    plot_spread(st, payoff, put_strike2, fig, ax, 
                    'Strike {} put_short'.format(put_strike2),'--')
    total_payoff += payoff
    premium_sold += premium

    call_strike1, premium, contracts, multiplier = call_short

    payoff = short_call_payoff(st, call_strike1, premium, contracts, multiplier)
    plot_spread(st, payoff, call_strike1, fig, ax, 
                    'Strike {} call_short'.format(call_strike1),'--')
    total_payoff += payoff
    premium_sold += premium

    call_strike2, premium, contracts, multiplier = call_long

    payoff = long_call_payoff(st, call_strike2, premium, contracts, multiplier)
    plot_spread(st, payoff, call_strike2, fig, ax, 
                    'Strike {} call_long'.format(call_strike2),'--')
    total_payoff += payoff
    premium_bought += premium 
    
    #-------------------- on top of the 1st Iron Condor
    put_strike1, premium, contracts, multiplier = put_long2
    
    payoff = long_put_payoff(st, put_strike1, premium, contracts, multiplier)
    plot_spread(st, payoff, put_strike1, fig, ax, 
                     'Strike {} put_long'.format(put_strike1),'--')
    total_payoff += payoff
    premium_bought += premium

    put_strike2, premium, contracts, multiplier = put_short2

    payoff = short_put_payoff(st, put_strike2, premium, contracts, multiplier)
    plot_spread(st, payoff, put_strike2, fig, ax, 
                    'Strike {} put_short'.format(put_strike2),'--')
    total_payoff += payoff
    premium_sold += premium

    call_strike1, premium, contracts, multiplier = call_short2

    payoff = short_call_payoff(st, call_strike1, premium, contracts, multiplier)
    plot_spread(st, payoff, call_strike1, fig, ax, 
                    'Strike {} call_short'.format(call_strike1),'--')
    total_payoff += payoff
    premium_sold += premium

    call_strike2, premium, contracts, multiplier = call_long2

    payoff = long_call_payoff(st, call_strike2, premium, contracts, multiplier)
    plot_spread(st, payoff, call_strike2, fig, ax, 
                    'Strike {} call_long'.format(call_strike2),'--')
    total_payoff += payoff
    premium_bought += premium
    
    net_premium = premium_sold - premium_bought
            
    for price, payoff in zip(st, total_payoff):
        if np.abs(payoff) < 0.5:
            if price < put_strike2:
                print("** break-even lower price ** : {:.01f}".format(price - payoff))
            if price > call_strike1:
                print("** break-even higher price ** : {:.01f}".format(price + payoff))
    
    plot_spread(st, total_payoff, call_strike2, fig, ax, 
                'Net Spread','-')

    plt.title('Iron Condor');

    print('Max Profit = {:.2f}'.format(max(total_payoff)))
    print('Max Loss = {:.2f}'.format(min(total_payoff)))
    print('Net Premium = {:.2f}'.format(net_premium)) 
    print('    Premium sold = {:.2f}'.format(premium_sold))
    print('    Premium bought = {:.2f}'.format(premium_bought))

    strike_difference = call_strike2 - call_strike1
    #win_probability = 100 - net_premium / strike_difference * 100
    
    #print('Win Probability = {:.2f} %'.format(win_probability))