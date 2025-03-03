import matplotlib.pyplot as plt


def bond_price(face, coupon, freq, years, dcc, yld):
    """
    Calculates bond price as % of face value.
    Assumes bullet structure, no accrued interest.
    """
    n = int(years * freq)
    c = face * coupon / freq
    pv = 0.0

    for t in range(1, n+1):
        # Simple daycount handling
        if dcc == "30/360":
            df = 1 / (1 + yld/freq)**t  # Standard compounding
        else:  # Actual/Actual approximation
            df = 1 / (1 + yld * (t/freq))  # Simple interest for irregular periods

        pv += c * df
        if t == n:
            pv += face * df

    return pv / face  # Price as decimal percentage

# -- Quick sensitivity analysis --
rates = [0.07, 0.08, 0.09, 0.10, 0.11, 0.12, 0.13]
params = {
    'face': 200,
    'coupon': 0.10,
    'freq': 4,
    'dcc': "30/360"
}

maturities = [2, 3, 4]  # Years to maturity to plot
colors = ['blue', 'green', 'red']  # Colors for each line

for years, color in zip(maturities, colors):
    prices = []
    params['years'] = years  # Update years in params
    for r in rates:
        px = bond_price(yld=r, **params)
        prices.append(px * params['face'])

    plt.plot(rates, prices, marker='o', label=f'{years} Years', color=color)

plt.title("Bond Price vs. Yield to Maturity (YTM)")
plt.xlabel("YTM")
plt.ylabel("Bond Price ($)")
plt.legend()  # Add a legend to identify the lines
plt.grid(True)
plt.show()