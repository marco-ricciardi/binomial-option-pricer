# One-step binomial option pricer
# Prices a European call when the share can only go up or down once.

def one_step_call(S, up, down, K):
    p = (S - down) / (up - down)
    upPayoff = max(up - K, 0)
    downPayoff = max(down - K, 0)
    premium = upPayoff*p + (1-p)*downPayoff
    print()
    print("Risk-neutral probability: ",p)
    print("Up payoff: ",upPayoff)
    print("Down payoff: ",downPayoff)
    print("Premium: ",premium)

S = float(input("Enter today's price: "))
up = float(input("Enter tomorrow's up price: "))
down = float(input("Enter tomorrow's down price: "))
K = float(input("Enter the strike price: "))

one_step_call(S, up, down, K)
