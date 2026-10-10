# n-step binomial option pricer with interest rates
# Prices a European call when the share can go up or down n times.

def step_back(p, up, down, r):
    """Calculates the fair price for the option for the previous step, using the risk-neutral probability, p, as well as applying the interest discount"""
    return((up*p + down*(1-p))/(1 + r))

def n_step_call(S, u, d, K, N, r):
    """Calculates the fair price at t=0 of a European call using added interest"""

    # Calculating the risk-neutral probability with interest rates
    p = (1 + r - d) / (u - d)

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
            newValues.append(step_back(p, values[nodes], values[nodes+1], r))

        values = newValues

    return(values[0])


print(n_step_call(100, 1.1, 0.9, 100, 10, 0.01))