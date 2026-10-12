# Binomial Option Pricer
A Python option pricer built from scratch with the binomial model, starting from a one-step tree and building up to an N-step tree with interest rates. *(Work in progress.)*

## Why I built this
As a first-year Financial Mathematics student, I wanted to understand how options are actually priced by building a model myself, not just by learning the formulas. The binomial model was a natural place to start. The first step can be worked out by hand with pen and paper, and each stage adds one new idea on top, so I could check every step as I built it.

## How it works
The model assumes that the price of a stock will either go up or down over each time step. After an up move, the price becomes S\*u and after a down move, S\*d. We calculate the risk-neutral probability, where "p" is the probability of an up move that makes the stock grow, on average, at exactly the risk-free rate. Including interest, the formula for "p" is:

```math
p = \frac{1 + r - d}{u - d}
```



## How I built it

## How to run it

## Roadmap
- [x] One-step tree
- [x] Two-step tree (backward induction)
- [x] N-step tree
- [x] Interest rates
- [ ] Volatility-based u and d (Cox-Ross-Rubinstein)
- [ ] Puts and American options
- [ ] Comparison with Black-Scholes
