import math

def step_back(p, up, down, growth):
    """Calculates the option value at the previous step in the binomial tree, given the risk-neutral probability p, the option values up and down, and the growth factor for one time step"""
    return((up*p + down*(1-p))/growth)

def n_step_price(S, K, N, r, T, sigma, kind):
    """Calculates the fair price at t=0 of a European put"""

    dt = T/N

    u = math.exp(sigma * math.sqrt(dt))
    d = 1/u

    growth = math.exp(r*dt)

    if not (d < growth < u):
        raise ValueError(f"No-arbitrage condition d < e^(r*dt) < u failed: d = {d}, e^(r*dt) = {growth}, u = {u}")
    
    p = (growth - d) / (u - d)

    l = []
    for j in range(N, -1, -1):
        x = S*(u**j)*(d**(N-j))
        # Calculating the option value at maturity for a put option
        if kind == "call":
            x = max(x - K, 0)
            l.append(x)
        elif kind == "put":
            x = max(K - x, 0)
            l.append(x)

    values = l
    for steps in range(0,N):
        newValues = []
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
kind = "put"

# Test depending on kind
if kind == "call":
    call_price = n_step_price(S, K, N, r, T, sigma, kind)
    put_price = n_step_price(S, K, N, r, T, sigma, "put")
elif kind == "put":
    call_price = n_step_price(S, K, N, r, T, sigma, "call")
    put_price = n_step_price(S, K, N, r, T, sigma, kind)

# Printing the prices
print(f"Call Price: {call_price:.4f}")
print(f"Put Price: {put_price:.4f}")
print()

# Parity check: making sure that the difference in put and call prices is the same as the difference between the stock's initial price and the strike price multiplied by the growth factor
print(f"C - P = {(call_price - put_price):.4f}")
print(f"S - Ke^(-rT) = {(S - K * math.exp(-r * T)):.4f}")