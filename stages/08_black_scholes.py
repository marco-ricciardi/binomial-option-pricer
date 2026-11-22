# n-step binomial pricer for European calls and puts, compared with Black-Scholes
# Shows that the tree's price converges towards the Black-Scholes price as N grows

import math
import matplotlib.pyplot as plt

def step_back(p, up, down, growth):
    """Calculates the option value at the previous step in the binomial tree, given the risk-neutral probability p, the option values up and down, and the growth factor for one time step"""
    return((up*p + down*(1-p))/growth)

def norm_cdf(x):
    """Calculates N(x), the probability that a standard normal random number is below x, using the error function from the math module"""
    return (1.0 + math.erf(x / math.sqrt(2.0))) / 2.0

def n_step_price(S, K, N, r, T, sigma, kind):
    """Calculates the fair price at t=0 of a European call or put with continuously compounded interest and volatility, where T is the time to maturity in years, r is the annual, continuously compounded rate, sigma is the volatility of the underlying asset, annually, as a decimal, and kind is "call" or "put", which only changes the payoff at maturity"""

    # Length of each time step in years
    dt = T/N

    # Up and down factors from volatility (Cox-Ross-Rubinstein): u = e^(sigma * sqrt(dt)), d = 1/u
    # Scaling by sqrt(dt) keeps the total variance at T*sigma^2 for any N
    # d = 1/u means an up move followed by a down move returns the price to S
    u = math.exp(sigma * math.sqrt(dt))
    d = 1/u

    # Growth factor for each time step
    growth = math.exp(r*dt)

    # Checking the no-arbitrage condition so that p is a valid probability
    if not (d < growth < u):
        raise ValueError(f"No-arbitrage condition d < e^(r*dt) < u failed: d = {d}, e^(r*dt) = {growth}, u = {u}")

    # Calculating the risk-neutral probability, using e^(r*dt) as the growth of £1 over one step
    p = (growth - d) / (u - d)

    # Creating the list of option values at maturity
    l = []
    for j in range(N, -1, -1):
        # Calculating the share price at maturity after j steps up and N-j steps down
        x = S*(u**j)*(d**(N-j))
        # Calculating the option value at maturity (call or put payoff)
        if kind == "call":
            x = max(x - K, 0)
            l.append(x)
        elif kind == "put":
            x = max(K - x, 0)
            l.append(x)

    # Calculating the option value at t=0 by stepping back through the tree
    values = l
    # Loop to step back through the tree N times
    for steps in range(0,N):
        newValues = []
        # Loop to calculate the option values for the previous step
        for nodes in range(0,len(values)-1):
            newValues.append(step_back(p, values[nodes], values[nodes+1], growth))

        values = newValues

    return(values[0])

def bs_call(S, K, r, T, sigma):
    """Calculates the Black-Scholes price at t=0 of a European call, with no tree and no N. The inputs are the same as n_step_price: T is the time to maturity in years, r is the annual, continuously compounded rate, and sigma is the annual volatility as a decimal"""

    # Calculating d1 and d2, which are plugged into N(x)
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)

    # Call price: value of the share received minus the discounted strike paid, each weighted by N(x)
    return(S*norm_cdf(d1) - K*math.exp(-r*T)*norm_cdf(d2))

def bs_put(S, K, r, T, sigma):
    """Calculates the Black-Scholes price at t=0 of a European put, with no tree and no N. The inputs are the same as bs_call"""

    # Calculating d1 and d2, the same as for the call
    d1 = (math.log(S/K) + (r + 0.5*sigma**2)*T) / (sigma*math.sqrt(T))
    d2 = d1 - sigma*math.sqrt(T)

    # Put price: the call formula flipped, using N(-d2) and N(-d1) for finishing below K
    return(K*math.exp(-r*T)*norm_cdf(-d2) - S*norm_cdf(-d1))

# Test values for convergence check
S = 100
K = 100
N_values = [1, 2, 5, 10, 20, 50, 100, 101, 500, 1000]  # Different number of steps for testing
r = 0.05
T = 1
sigma = 0.2

# Black-Scholes price of the call, worked out once since it doesn't depend on N
bs_price = bs_call(S, K, r, T, sigma)

# Pricing the call with the tree for each N and printing the gap to Black-Scholes
for N in N_values:
    call_price = n_step_price(S, K, N, r, T, sigma, "call")
    gap = call_price - bs_price
    print(f"N: {N}, Call Price: {call_price:.4f}, Gap to Black-Scholes: {gap:+.4f}")

# Plotting the convergence of the binomial price to the Black-Scholes price as N increases
N_chart = []
prices = []

for i in range(1,201):
    N_chart.append(i)
    prices.append(n_step_price(S, K, i, r, T, sigma, "call"))

plt.plot(N_chart, prices, label='Binomial Price')
plt.axhline(y=bs_price, color='r', linestyle='--', label='Black-Scholes Price')
plt.legend()
plt.xlabel('Number of Steps (N)')
plt.ylabel('Call Price')
plt.title('Convergence of Binomial to Black-Scholes')
plt.savefig("images/convergence.png")
plt.show()