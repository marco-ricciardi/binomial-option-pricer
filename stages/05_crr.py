# n-step binomial option pricer with interest rates and volatility
# Prices a European call when the share can go up or down n times

import math

def step_back(p, up, down, growth):
    """Calculates the option value at the previous step in the binomial tree, given the risk-neutral probability p, the option values up and down, and the growth factor for one time step"""
    return((up*p + down*(1-p))/growth)

def n_step_call(S, K, N, r, T, sigma):
    """Calculates the fair price at t=0 of a European call with continuously compounded interest and volatility, where T is the time to maturity in years, r is the annual, continuously compounded rate, and sigma is the volatility of the underlying asset, annually, as a decimal"""

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
        # Calculating the option value at maturity for a call option
        x = max(x - K, 0)
        l.append(x)

    # Calculating the option value at t=0 by stepping back through the tree
    values = l
    # Loop to step back through the tree N times
    for steps in range(0,N):
        newValues = []
        # Loop to calculate the call prices for the previous step
        for nodes in range(0,len(values)-1):
            newValues.append(step_back(p, values[nodes], values[nodes+1], growth))

        values = newValues

    return(values[0])

# Test
print(f"Call Price: {n_step_call(100, 100, 100, 0.05, 1, 0.2):.4f}")