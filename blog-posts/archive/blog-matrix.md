# Vision for Nibiru Protocol

Tags: Blockchain, Cryptocurrency, Cosmos, Stablecoin  
Description: Insights on the Nibiru protocol taken from the official whitepaper.

## What is the Nibiru protocol?

Nibiru is a capital efficient, decentralized protocol for creating stable crypto assets that can be traded on the blockchain using the Cosmos SDK. It allows **stable seekers** to swap between collateral and stable assets.

## Cosmos-native stablecoin

Nibiru will mint **NUSD**, a stablecoin backed by collateral in the form of OSMO. Eventually, the protocol will allow for other tokens to be used as collateral from a governance-made whitelist. These tokens are priced at [Chainlink](https://chain.link/) oracle value and swap with a minimal amount of transaction fees, which go to the protocol. Collateral can always be swapped with NUSD at oracle value.

<img src="img/user-protocol-price-feed.png">

Stables assets are minted whenever whitelisted collateral is sent to the protocol. Whenever stable assets are instead sent to the protocol in exchange for collateral, the stablecoins are burned. These transactions are always executed without price slippage but with a small transaction fee to prevent front-running and flash loan attacks, support the robustness of the protocol, and compensate liquidity providers.

## Nibiru Liquidity Providers

### Minting and Redeeming

**Leverage Agents (LAs)** insure the protocol against drops in collateral price, making sure that there are always reserves for stable holders. Similar to the liquidity positions of Uniswap, liquidity agent positions are implemented as NFTs. These positions are transferable between addresses and cover fixed amounts of liquidity ($c_{\text{cover}}$).

**LAs choose how much collateral they want to cover** for stable seekers and essentially take a long investment on the underlying collateral. A leverage agent's position can be redeemed in the form of collateral (token) it covers based on the following equation:

$$
\text{position\_value} = c_{\text{cover}}\cdot \left( 1 - \frac{\text{price\_initial}}{\text{price\_current}}  \right) + c_{LA},
$$
where $c_{LA}$ is the collateral the agent brings to the protocol, and $c_{\text{cover}}$ is the amount of collateral the agent chooses to cover.

Investments from LAs absorb the volatility of the amount they are backing by enabling the protocol to use their collateral in the case of price drops, effectively reducing the exposure of Nibiru to price variations. From the perspective of an agent, one gets great earnings in the case of a price increase and suffers substantial losses if price decreases because a leverage agent has a long, leveraged position with multiplier $\ell = \dfrac{c_{\text{cover}}}{c_{LA}}$.  

For example, suppose that an LA brings $c_{LA}=10$ OSMO and covers $c_{\text{cover}}=60$ OSMO. This LA is taking the variation of $c_{\text{cover}}$.

#### Case: Price increase
 If the price of OSMO goes from $p_i = \$10$ to $p_f = \$12$, the percentage change in the price is $\Delta_{\text{pct\_p}} = \dfrac{p_f - p_i}{p_f}$ is $\dfrac{1}{6}$. The unrealized value of the LA's position will then be   

$$ \boxed{ \text{position\_value} = c_{LA} \left( \ell \cdot \Delta_{\text{pct\_p}} + 1\right) } = 10\text{ OSMO} \left(6 \cdot \frac{1}{6} + 1 \right) = 20\text{ OMSO} .$$

#### Case: Price decrease

If the $\text{position\_value}$ equation decreases to 0, the LA gets liquidated and the protocol absorbs $c_{LA}$.
Thus, if price instead decreases from $p_i = \$10$ to 

$$ \text{price\_initial} \cdot \dfrac{ c_{\text{cover}} }{ c_{\text{cover}} + c_{LA} }  = \$10 \cdot \frac{ 60 }{60 + 10} =  \$8.57, $$
Nibiru will liquidate the LA position.

##### Constraints on leverage agents:

- There's a one-hour lock on an LA's position after each update. This prevents LAs from taking advantage of unfair advantages from knowledge surrounding price movements.
- LAs pay small transaction fees when entering and exiting positions with the protocol based on coverage curves. If more collateral is covered, it becomes more expensive to provide liquidity as an LA but less expensive to exit a position.

In the case the protocol's stable seekers are entirely covered by LAs, there would be perfect convertibility between Nibiru stablecoins and their corresponding collateral. BAut what happens in the case that LAs' positions and protocol's insured reserves can't cover the collateral brought by users? You can imagine a scenario where the LAs all get liquidated and the protocol gets under-collateralized. Nibiru makes use of another type of liquidity provider known as an Insurance Agent in order to prevent this.

### Insurance Agents

**Insurance Agents (IAs)** ensure the collateralization of the protocol when there's a mismatch between user demand and the liquidity provided by Leverage Agents. Insurance agents provide extra liquidity to the protocol and accrue interest on the assets they bring. 

There are several revenue streams for providing liquidity as an Insurance Agent:
1. **Transaction fees**: In proportion to their position size, IAs receive a cut of the transaction fees when stablecoins are minted and burned.
2. **Staking**: IAs can stake their liquidity positions to receive governance tokens.
3. **Reserve pool investments:** Stable seekers bring collateral to the Nibiru protocol and this will often result in an under-utilization of the assets. In similar fashion to how the surplus from Curve pools are used on yield aggregation protocols or lending protocols like Compound and Aave, **Nibiru will automatically invest some its extra reserves** on platforms like Umee and Osmosis. IAs earn interest from this too. 

Suppose the protocol owns 15 OSMO (collateral), of which 10 comes from stable seekers and 5 comes from liquidity providers. Insurance Agents can earn interest from all of this. This interest depends on what proportion of the protocol funds are invested in strategies and what proportion of the liquidity is supplied by other IAs.

To be clear, IAs are in competition with each other. The less liquidity there is coming from IAs in the protocol, the more a single agent earns from each revenue stream: transaction fees, staking governance tokens, and investment yields.

An IA providing OSMO liquidity for the NUSD stablecoin receives sNEO, a tokens that quantify the rewards. sNEO represents the "share" of pool for which the IA provides liquidity. When issued sNEO, IAs can interest/rewards through the token's underlying exchange rate, which increases as (1) transaction fees collect for the pool and (2) as interest is collected from collateral being lent.

**Risks for Insurance Agents**: The risk for an Insurance Agent is incurring slippage when the protocol is under-collateralized, i.e. not being able to reclaim assets with the same value they put in.  

## How will the token stability be guaranteed? 

#### Nibiru DAO

In order for users of Nibiru protocol to be guaranteed the option of swapping between collateral and stablecoins, the protocol must remain **over-collateralized**. This problem is addressed through Nibiru DAO's **Incentive Pendulum**, a system designed to incentivize liquidity providers (LPs) and drive the utility of the NIBI token. 

Nibiru gets its liquidity from two places: LPs and the **Insurance Fund (IF)**, a reserve fund for the protocol. At genesis, Nibiru DAO's assets are divided between LPs and the IF. From that moment on, the DAO splits profits from wagering based on an imbalance factor $\Xi^{-1}$:

$$\Xi^{-1} = \frac{\text{LP} - \text{IF}}{\text{LP} + \text{IF}},$$

where $LP$ and $IF$ are the asset contributions from the liquidity providers and Insurance Fund, respectively. The value of $\Xi^{-1}$ determines the state of the protocol. For example, 
<!-- 
- **Optimal**, $\Xi^{-1} = \frac{1}{3}$: The desired state, where 67% of the assets are provided by LPs and 33% are provided by the IF. The rewards from the protocol are split with the same proportions.
- **Under-utilized**, $\Xi^{-1}=0$ : An unsafe state. Here, both LPs and the IF provide 50% of the assets each. 100% of the rewards go to the IF (i.e. no rewards go to LPs). If the protocol is under-utilized, stakers have no incentive to validate the block-chain.
- **Inefficient**, $\Xi^{-1}=1$: LPs provide 100% of the assets and receive 100% of the protocol rewards. When the protocol becomes inefficient, capital and rewards are re-allocated by the DAO between LPs and the IF to bring about additional investment yields, moving the protocol closer to optimality. 
-->

| State | $\Xi^{-1}$ | Description |
| :--: | :--: | -- | 
| **Optimal** | $\frac{1}{3}$ | The desired state, where 67% of the assets are provided by LPs and 33% are provided by the IF. The rewards from the protocol are split with the same proportions. |
| **Under-utilized** | $0$ | An unsafe state. Here, both LPs and the IF provide 50% of the assets each. 100% of the rewards go to the IF (i.e. no rewards go to LPs). If the protocol is under-utilized, stakers have no incentive to validate the block-chain. |
| **Inefficient** | $1$ | LPs provide 100% of the assets and receive 100% of the protocol rewards. When the protocol becomes inefficient, capital and rewards are re-allocated by the DAO between LPs and the IF to bring about additional investment yields, moving the protocol closer to optimality. |

<!-- ## Partners (ask if this should be included) -->

*Disclaimer: This content is provided for informational purposes only, and should not be relied upon as legal, business, investment, or tax advice. You should consult your own advisers as to those matters. References to any securities or digital assets are for illustrative purposes only, and do not constitute an investment recommendation or offer to provide investment advisory services. This content is not directed at nor intended for use by any investors or prospective investors, and may not under any circumstances be relied upon when making investment decisions.*


<!--
- [ ] TODO | link to whitepaper
- [ ] TODO | link to project's Twitter
  -->