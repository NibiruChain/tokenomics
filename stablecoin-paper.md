# Matrix Stablecoin Stability

Tags: Blockchain, Cryptocurrency, Cosmos, Stablecoin  
Description: TODO: 

#### 2.3 Achieving stability with consistent mining rewards
- [ ] Q: What pressures normalize the price of tokens like USDM and KRWM? 


> "In the short term, miners absorb Terra contraction costs through mining power dilution."
- [ ] Q: Do transaction fees from when Matrix mints and burns stables go only to the Insurance Agents?

Mint and burn tx fees go to both the IAs and the IF (let's say 50/50 split). A super tiny fraction of the tx fees also goes to the validators too.  
- IAs get non-fungible LP tokens and fees. Some liquidity from the IAs is invested to grow their funds.


- [ ] Q: Which forces in the protocol pay the validators?

MTRX has its own staking inflation. 

#### All edge cases should be stress-tested

- What happens in extreme and extended bear markets?
- What happens to IF in different regimes?

> "In the mid to long term, miners are compensated with increased mining rewards."
- [ ] Q: What's the interplay between MTRX, m-stables, and miner rewards?

- San: In our case, the demand for m-stables is assumed to be constant. If demand goes up, validators make more money. TODO: Include model for that in the future.




#### 2.4 Miners absorb short-term Terra volatility
- [ ] Describe how 

**Important point**:
> "Luna also serves as the most immediate defense against Terra price fluctuations. The system uses Luna to make the price for Terra by agreeing to be counter-party to anyone looking to swap Terra and Luna at Terra's target exchange rate. More concretely, 
> - When TerraSDR's price < 1 SDR, users and arbitragers can send 1 TerraSDR to the system and receive 1 SDR's worth of Luna.
> - When TerraSDR's price  > 1 SDR, users and arbitragers can send 1 SDR's worth of Luna to the system and receive 1 TerraSDR."

Baseline: 
1. IAs only receive MTRX.
2. 

Imaging there's OSMO and ATOM whitelisted. Suppose OSMO becomes a shit token.
1. Matrix has \$50 M of ATOM and \$10M of OSMO. 
2. If OSMO goes to shit, the IF can take some of its money (in MTRX) to buy OSMO and give it back.


The LP tokens are unique to every pool. The governing body has MTRX, but if one pool goes to zero, it won't impact the other pools.

```python
# Pools
collaterals =  ["OSMO", "ATOM"]
m-stables = ["USDM", "KRWM", "EURM"]
pools: list[str] = ["MTRX:USDM", "MTRX:KRWM", "MTRX:EURM", 
                    "MTRX:OSMO", "MTRX:ATOM"]
```

v1 → All pools silod  
v2 → Make the protocol interact with swaps b/w certain whitelisted collateral.

Q: What if OsmoLabs doesn't like Matrix? If we have the collateral from a significant proportion of OSMO holders, we can dictate 

- [x] Q: Are we using this mechanism with MTRX and m-stables? → We can use MTRX like collateral in our swap (mint and burn of m-stable) modules.

#### 2.5

> "Stable demand for mining is a core requirement for both security and stability... The protocol has two ways of rewarding miners for their work: 
> 1. Transaction fees: ...
> 2. Seigniorage (Luna burn): When demand for Terra increases, the system mints Terra and earns Luna in return."

- Use Curve governance model instead of Seigniorage. Use veCRV logic. MTRX can be bonded into a governance contract to earn increased rewards. 

--- 

Simulator new features: 
1. Simulated mints-burns of m-stables
2. Variable funding rate

<!-- Make it streamlined b/c crowd is less-quanty -->
Outline for simulator litepaper
- Matrix makes an algo stable, fees from LAs that bring collateral, IAs that try to over-collateralize the protocol in return for fees and LP tokens. Design of the derivatives platform is to help the protocol work through extreme market conditions.
  - Intro: Motivating the problem -> Importance of stability
- Define the problem: What are the factors that influence...
- Eliminate/Ignore certain ones for simplicity.
- 2 to 3 examples: 

Funding rate is designed to keep the retail traders from running away 
- BSC has a strong retail crowd. ATOM, which is listed on BSC is very transparent.

<!-- Want to know what the factors are that influence this problem -->

---

## Matrix Meeting 

The setup of the legal entities is the reason for delay. Everyone will be pro-rated. If people need liquidity more urgently in order to keep momentum, contact Vector Sigma / Optimus Prime. 







---

*Disclaimer: This content is provided for informational purposes only, and should not be relied upon as legal, business, investment, or tax advice. You should consult your own advisers as to those matters. References to any securities or digital assets are for illustrative purposes only, and do not constitute an investment recommendation or offer to provide investment advisory services. This content is not directed at nor intended for use by any investors or prospective investors, and may not under any circumstances be relied upon when making investment decisions.*


<!--
- [ ] TODO | link to whitepaper
- [ ] TODO | link to project's Twitter
  -->
