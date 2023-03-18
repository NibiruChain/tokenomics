
# Nibiru - NIBI Tokenomics

Tags: Blockchain, Cryptocurrency, Cosmos, Stablecoin, Tokenomics 
Description: ""

**Nibiru** will be responsible for deploying new stablecoins, accepting new collateral types for a given stablecoin and protocol upgrades and integrations. 

**NIBI** is the decentralized governance token of the **Matrix Protocol**. In other words, NIBI tokens give hodlers the right to participate in governance votes with the **Nibiru DAO**, which manages the protocol with a **split of 75% to the community, 15% to the core Matrix Protocol development team, and 10% to early backers**. 

| Split (%) | Group | Description |  
| :---: | :----: | ---- | 
| 40 | Community | NIBI Liquidity Mining Program |
| 20 | Community | Treasury controlled through Nibiru DAO | 
| 15 | Community | Strategic partners, project advisors, and community members that contribute a lot to the protocol   | 
| 15 | Core | Core Matrix Team | 
| 10 | Early Backers | Initial DEX offering (IDO), Seed funding | 

#### Utility of NIBI

Governance with NIBI will be crucial to shaping the protocol's tokenomics. The idea here is put most of the voting power into the hands of the Matrix community and allow the token model to be iterated upon and revised in an inclusive, decentralized manner. The intention is ensure the efficient use of the collateral in the protocol through on-chain voting with Nibiru DAO.

Matrix protocol will accumulate surplus in the form of transaction fees from m-stable/Collateral swaps, yield from insurance fund investments, and collateral appreciation. The DAO (and, thus, NIBI) will be responsible for deciding how to best utilize this surplus. Our view is that some of the protocol's surplus should be:
1. Used as a buffer to the collateral's volatility and be reinvested into the protocol's yield aggregation mechanisms. 
2. Allocated to support future development initiatives and extensions to the protocol.
3. Put toward NIBI **buybacks**. Buybacks would transfer some value back to the community and NIBI hodlers, aligning incentives between governance token holders and the rest of the Matrix ecosytem. The Matrix protocol could buy back tokens to burn them, distribute them into the DAO Treasury, or put into the liquidity mining program.

## Token Distribution

The NIBI token distribution has been modeled to ensure both the short and long-term success of the protocol and its community. With an **genesis supply of 355.5 million**, the mission behind NIBI will be make governance for the protocol much more active and decentralized, to help the protocol control a portion of its reserves, and incentivize both users and [Matrix Liquidity Providers](blog-matrix.md). 

<!-- TODO link to post 1 -->
[blog-post-matrix]: example.com

<img src="plots/genesis_supply.svg">

As more tokens are released into the ecosystem, the distribution will eventually rest mostly in the hands of the community.


<img src="plots/final_token_supply.svg">

### Community Liquidity Mining Program

40% of the NIBI supply (400M tokens) will go to liqudity mining incentives over a period of 4 years on Osmosis. These are be distributed to m-stable holders through staking contracts, to Insurance Agents, and to LPs of AMM pools involving whitelisted tokens of the protocol.

The NIBI distribution is modeled after Bitcoin mining, except that instead of halving every 4 years, NIBI's distribution will diminish every week. This is implemented using a multisig held by NIBI's Core Team.

Each week, some tokens will be distributed to each group with an allocation size determined by governance. The objective of this portion of the treasury is to incentize early users and new participants over the long-term while avoiding short-term mercenary capital.

### Treasury

At launch, Nibiru DAO will manage 20% of the NIBI supply, empowering the community to decide where NIBI rewards are allocated. Upon activation of governance, the Core Team will sell large a portion of tokens against m-stables via a **bonding curve** so that the protocol can accumulate surplus, control some of NIBI's reserves, and deflate the total stablecoin supply (in the event of a black swan scenario).

The Core Team's bonding curve is an exponentially increasing function depending on how many tokens have been sold. It has the potential to revolutionize the way protocols fund themselves and own liquidty. Insted of selling tokens against another curve, the bonding curve sells governance tokens against a token of the protocol, giving the Nibiru DAO 

### Core Team

15% of the token supply goes to the Core Team. They will be subject to 3-year vesting, where 2% of this 15% (0.3% of the total supply) will be made available on release, and the remaining tokens will vest linearly. The goal of this scheduling is to keep a meaningfully incentivized yet non-controlling core development team that is still fully commited to the protocol and community long-term.

### Early Backers

The Core Team is expected to raise funding using 10% of the tokens for early backers. This funding goes toward the recruitment of top tier talent and payment for extensive security audits.

<!-- ## Token Utility (paper 2.5) -->

---

*Disclaimer: This content is provided for informational purposes only, and should not be relied upon as legal, business, investment, or tax advice. You should consult your own advisers as to those matters. References to any securities or digital assets are for illustrative purposes only, and do not constitute an investment recommendation or offer to provide investment advisory services. This content is not directed at nor intended for use by any investors or prospective investors, and may not under any circumstances be relied upon when making investment decisions.*

