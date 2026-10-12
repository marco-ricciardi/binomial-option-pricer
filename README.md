# Binomial Option Pricer
A Python option pricer built from scratch with the binomial model, starting from a one-step tree and building up to an N-step tree with interest rates. *(Work in progress.)*

## Why I built this
As a first-year Financial Mathematics student, I wanted to understand how options are actually priced by building a model myself, not just by learning the formulas. The binomial model was a natural place to start. The first step can be worked out by hand with pen and paper, and each stage adds one new idea on top, so I could check every step as I built it.

## How it works
The model assumes that the price of a stock will either go up or down over each time step. After an up move, the price becomes $S \times u$, and after a down move, $S \times d$. We calculate the risk-neutral probability $p$: the probability of an up move that makes the stock grow, on average, at exactly the risk-free rate. Including interest, the formula for $p$ is:

```math
p = \frac{1 + r - d}{u - d}
```

Where $r$ is the risk-free interest rate per step.

When we reach the final column of the tree, we can calculate what the option is worth if you exercise it, using:

```math
V = \max(S - K, 0)
```

Where $S$ is the stock price at the final point and $K$ is the strike price, the price at which the option lets you buy the stock. Therefore, if the stock price ends below the strike price, the call would simply not be exercised, meaning the value of the final payoff never drops below 0.

Finally, we calculate the fair price of the option today $(t = 0)$ using backward induction. At each point, the option's calculated value is the p-weighted average of the two points after it, divided by $(1 + r)$ to account for interest. 
We repeat this process column by column, taking in each newly calculated fair price as the input for the next price, until we reach today:

```math
V = \frac{pV_{\text{up}} + (1-p)V_{\text{down}}}{1 + r}
```

We divide by $(1 + r)$ because £1 received one step from now is worth less than £1 today.

## How I built it
1. [One-step tree](stages/01_one_step.py): priced a call with a single up/down move, using the risk-neutral probability.
2. [Two-step tree](stages/02_two_step.py): scaled up to two up/down moves, and introduced backward induction.
3. [N-step tree](stages/03_n_step.py): scaled up to an n-step tree, using loops to build the tree and step back through it for any number of steps.
4. [Interest rates](stages/04_interest_rates.py): added risk-free rate $r$, which changes $p$ and discounts each step back by $(1 + r)$.

## How to run it
Requires Python 3. No extra libraries needed.

    python stages/04_interest_rates.py

## Roadmap
- [x] One-step tree
- [x] Two-step tree (backward induction)
- [x] N-step tree
- [x] Interest rates
- [ ] Volatility-based u and d (Cox-Ross-Rubinstein)
- [ ] Puts and American options
- [ ] Comparison with Black-Scholes
