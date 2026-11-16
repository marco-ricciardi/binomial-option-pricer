# n-step binomial pricer for European calls and puts
# Adds puts and checks them against calls with put-call parity

import math

def step_back(p, up, down, growth):
    """Calculates the option value at the previous step in the binomial tree, given the risk-neutral probability p, the option values up and down, and the growth factor for one time step"""
    return((up*p + down*(1-p))/growth)

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

# Declare test values
S = 100
K = 100
N = 1
r = 0.05
T = 1
sigma = 0.2

# Pricing the call and put options
call_price = n_step_price(S, K, N, r, T, sigma, "call")
put_price = n_step_price(S, K, N, r, T, sigma, "put")

# Printing the prices
print(f"Call Price: {call_price:.4f}")
print(f"Put Price: {put_price:.4f}")
print()

# Parity check: C - P should equal the share price today minus the strike discounted back to today, S - Ke^(-rT)
print(f"C - P = {(call_price - put_price):.4f}")
print(f"S - Ke^(-rT) = {(S - K * math.exp(-r * T)):.4f}")
