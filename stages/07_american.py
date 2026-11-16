# n-step binomial pricer for European and American options
# Adds early exercise: an American option can be exercised at any step, not just at maturity

import math

def step_back(p, up, down, growth):
    """Calculates the option value at the previous step in the binomial tree, given the risk-neutral probability p, the option values up and down, and the growth factor for one time step"""
    return((up*p + down*(1-p))/growth)

def european_price(S, K, N, r, T, sigma, kind):
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

def american_price(S, K, N, r, T, sigma, kind):
    """Calculates the fair price at t=0 of an American call or put, which can be exercised at any step up to maturity. At each point in the tree the holder either keeps the option, getting the continuation value (the discounted, risk-neutral average of the next two values), or exercises it now, getting the exercise value (the payoff using the share price at that point). The option is worth the bigger of the two. Inputs are the same as european_price"""

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
        # Time step of the new list: it has n+1 points, n moves from today
        n = N - steps - 1
        newValues = []
        # Loop over each point at time step n, from the top (most up moves) down
        for nodes in range(0,len(values)-1):
            # Calculating the share price at this point after n-nodes steps up and nodes steps down
            share_price = S*(u**(n-nodes))*(d**nodes)
            # Calculating the exercise value: the payoff if the option is used now
            if kind == "put":
                exercise_value = max(K - share_price, 0)
            elif kind == "call":
                exercise_value = max(share_price - K, 0)
            # Calculating the continuation value: the value if the option is kept
            step_back_value = step_back(p, values[nodes], values[nodes+1], growth)
            # The holder picks whichever is bigger
            newValues.append(max(step_back_value, exercise_value))

        values = newValues

    return(values[0])

# Setting test values
S = 100
K = 100
N = 2
r = 0.05
T = 1
sigma = 0.2

# Pricing the American call and put options
call_price = american_price(S, K, N, r, T, sigma, "call")
put_price = american_price(S, K, N, r, T, sigma, "put")

# Printing the prices
print(f"American Call Price: {call_price:.4f}")
print(f"American Put Price: {put_price:.4f}")
print()

# Put-call parity doesn't hold for American options: this gap should equal the put's early-exercise premium below
print(f"(S - Ke^(-rT)) - (C - P) = {(S - K * math.exp(-r * T)) - (call_price - put_price):.4f}")
# Early-exercise premium of the put: American minus European
print(f"Difference between American and European Put Price: {put_price - european_price(S, K, N, r, T, sigma, 'put'):.4f}")
# The American call should equal the European call: early exercise never pays without dividends
print(f"Difference between American and European Call Price: {call_price - european_price(S, K, N, r, T, sigma, 'call'):.4f}")