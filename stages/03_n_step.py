# n-step binomial option pricer
# Prices a European call when the share can go up or down n times.

def step_back(p, up, down):
    """Calculates the fair price for the option for the previous step, using the risk-neutral probability, p"""
    return(up*p + down*(1-p))

def n_step_call(S, u, d, K, N):
    """Calculates the fair price at t=0 of a European call using a n-step binomial tree"""
    p = (1 - d) / (u - d)

    l = []
    for j in range(N, -1, -1):
        x = S*(u**j)*(d**(N-j))
        x = max(x - K, 0)
        l.append(round(x))

    values = l
    for i in range(0,N):
        newValues = []
        for i in range(0,len(values)-1):
            newValues.append(step_back(p, values[i], values[i+1]))

        values = newValues

    return(values)


print(n_step_call(100,1.2,0.8,100,3))