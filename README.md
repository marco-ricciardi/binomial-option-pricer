# Binomial Option Pricer
A Python option pricer built from scratch with the binomial model, starting from a one-step tree and adding one concept per stage. *(Work in progress.)*
 
## Why I built this
As a first-year Financial Mathematics student, I wanted to understand how options are actually priced by building a model myself, not just by learning the formulas.

The binomial model was a natural place to start. The first step can be worked out by hand with pen and paper, and each stage adds one new idea on top, so I could check every step as I built it.
 
## How it works
The model assumes that the price of a stock will either go up or down over each time step. After an up move, the price becomes $S \times u$, and after a down move, $S \times d$, where $u$ and $d$ are set by the volatility $\sigma$ as follows:
 
```math
\Delta t = \frac{T}{N}, \qquad u = e^{\sigma\sqrt{\Delta t}}, \qquad d = \frac{1}{u} = e^{-\sigma\sqrt{\Delta t}}
```
<br>

Where $T$ is the time to maturity in years and $N$ is the number of steps. $\sigma$ is the annual volatility, written as a decimal (so 20% is 0.2): the standard deviation of the stock's log-returns over one year, i.e. how widely the stock's returns spread out.

Scaling by $\sqrt{\Delta t}$ means the log-price has the same total variance, $\sigma^2 T$, no matter how many steps the tree has, so adding steps makes the option price converge towards the Black-Scholes price rather than changing how much the stock moves.

Setting $d = 1/u$ means an up move followed by a down move returns the price exactly to $S$, so the tree stays centred on today's price and each step moves the log-price by the same amount up or down. (For example, with $u = 1.2$ and $d = 0.8$, an up then down move takes 100 to 96, but with $d = 1/u \approx 0.833$ it returns to exactly 100.)

We calculate the risk-neutral probability $p$: the probability of an up move that makes the stock grow, on average, at exactly the risk-free rate. The formula for $p$ is:

```math
p = \frac{e^{r\Delta t} - d}{u - d}
```
<br>

Where $r$ is the annual risk-free interest rate (continuously compounded), so $e^{r\Delta t}$ is how much £1 grows over one step.

For $p$ to be a valid probability (between 0 and 1), we need $d < e^{r\Delta t} < u$. This is the no-arbitrage condition: if the stock were guaranteed to beat the risk-free rate (or guaranteed to lose to it), you could make a risk-free profit. The code checks this condition and raises an error if it fails.
 
When we reach the final column of the tree, we can calculate what the option is worth if you exercise it, using:
 
```math
V = \max(S_T - K, 0)
```
<br>

Where $S_T$ is the stock price at the final point and $K$ is the strike price, the price at which the option lets you buy the stock. Therefore, if the stock price ends below the strike price, the call would simply not be exercised, meaning the value of the final payoff never drops below 0.
 
Finally, we calculate the fair price of the option today $(t = 0)$ using backward induction. At each point, the option's calculated value is the p-weighted average of the two points after it, divided by $e^{r\Delta t}$ to account for interest.

We repeat this process column by column, taking in each newly calculated fair price as the input for the next price, until we reach today:
 
```math
V = \frac{pV_{\text{up}} + (1-p)V_{\text{down}}}{e^{r\Delta t}}
```
<br>

We divide by $e^{r\Delta t}$ because £1 received one step from now is worth less than £1 today.
 
## How I built it
1. [One-step tree](stages/01_one_step.py): priced a call with a single up/down move, using the risk-neutral probability.
2. [Two-step tree](stages/02_two_step.py): scaled up to two up/down moves, and introduced backward induction.
3. [N-step tree](stages/03_n_step.py): scaled up to an n-step tree, using loops to build the tree and step back through it for any number of steps.
4. [Interest rates](stages/04_interest_rates.py): added a continuously compounded annual rate $r$ over time to maturity $T$, which changes $p$ and discounts each step back by $e^{r\Delta t}$, plus a no-arbitrage check.
5. [Cox-Ross-Rubinstein](stages/05_crr.py): replaced manually assigned $u$ and $d$ with ones calculated from volatility, so the option price converges towards the Black-Scholes price as $N$ grows.

## How to run it
Requires Python 3. No extra libraries needed.
 
    python stages/05_crr.py
 
## Roadmap
- [x] One-step tree
- [x] Two-step tree (backward induction)
- [x] N-step tree
- [x] Interest rates
- [x] Volatility-based u and d (Cox-Ross-Rubinstein)
- [ ] Puts and put-call parity
- [ ] American options (early exercise)
- [ ] Black-Scholes comparison and convergence chart
- [ ] Implied volatility (bisection and Newton's method)
- [ ] Delta and hedging
