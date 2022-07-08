


def risk_money_management():
    ''' After performing backtest, the overal performance of the strategy is
    defined laying the groundwork for a better money and risk management in
    the sense that the overal historical trend of the asset gains becomes
    rising.'''
    cap = 1000
    risk = [0.03, 0.05, 0.1, 0.3]
    r_p = [0.9, 0.65, 0.5]
    win_loss = [0]*45 + [1]*55
    random.shuffle(win_loss)
    x = range(0, 101)
    # print(win_loss)
    lst = []
    lst.append(cap)
    for i in win_loss:
        if i == 0:
            cap = cap-risk[1]*cap
            lst.append(cap)
        else:
            cap = cap + cap*risk[1]/r_p[1]
            lst.append(cap)

    plt.plot(x, lst)
    plt.show()

