# Two-step binomial option pricer
# Prices a European call when the share can only go up or down twice.

def step_back(p, up, down):
    """Calculates the fair price for the option for the previous step, using the risk-neutral probability, p"""
    return(up*p + down*(1-p))

def two_step_call(S, u, d, K):
    """Calculates the fair price at t=0 of a European call using a two-step binomial tree"""
    # Calculating the risk-neutral probability
    p = (1 - d) / (u - d)
    # Calculating the share prices at t=2
    UpUp = S*(u**2)
    UpDown = S*u*d
    DownDown = S*(d**2)
    # Calculating the call payoffs at t=2
    uuP = max(UpUp - K, 0)
    udP = max(UpDown - K, 0)
    ddP = max(DownDown - K, 0)
    # Calculating the fair prices at t=1
    step1_up = step_back(p, uuP, udP)
    step1_down = step_back(p, udP, ddP)
    # Calculating the fair price at t=0
    step2 = step_back(p, step1_up, step1_down)
    return(step2)

S = float(input("Enter today's price: "))
u = float(input("Enter the up factor: "))
d = float(input("Enter the down factor: "))
K = float(input("Enter the strike price: "))

print("Fair price:", two_step_call(S, u, d, K))