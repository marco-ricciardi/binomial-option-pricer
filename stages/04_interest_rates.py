# n-step binomial option pricer with interest rates
# Prices a European call when the share can go up or down n times.

def step_back(p, up, down, r):
    """Calculates the fair price for the option for the previous step, using the risk-neutral probability, p, as well as applying the interest discount"""
    return((up*p + down*(1-p))/(1 + r))

def n_step_call(S, u, d, K, N, r):
    """Calculates the fair price at t=0 of a European call using added interest"""
    p = (1 + r - d) / (u - d)

    l = []
    for j in range(N, -1, -1):
        x = S*(u**j)*(d**(N-j))
        x = max(x - K, 0)
        # Removed rounding for more accurate final values
        l.append(x)

    values = l
    for i in range(0,N):
        newValues = []
        for i in range(0,len(values)-1):
            newValues.append(step_back(p, values[i], values[i+1], r))

        values = newValues

    return(values)

print(n_step_call(100, 1.1, 0.9, 100, 10, 0.01) )