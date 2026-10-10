# Two-step binomial option pricer
# Prices a European call when the share can only go up or down twice.

def step_back(p, up, down):
    return(up*p + down*(1-p))

def two_step_call(S, u, d, K):
    p = (1 - d) / (u - d)
    UpUp = S*(u**2)
    UpDown = S*u*d
    DownDown = S*(d**2)
    uuP = max(UpUp - K, 0)
    udP = max(UpDown - K, 0)
    ddP = max(DownDown - K, 0)
    step1_up = step_back(p, uuP, udP)
    step1_down = step_back(p, udP, ddP)
    step2 = step_back(p, step1_up, step1_down)
    return(step2)

S = float(input("Enter today's price: "))
u = float(input("Enter the up factor: "))
d = float(input("Enter the down factor: "))
K = float(input("Enter the strike price: "))

print("Fair price:", two_step_call(S, u, d, K))