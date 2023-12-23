# NibiruChain/research

This repository produces the mathematics underlying the Nibiru Chain tokenomics,
defining the inflation curve for the community distribution, generating plots,
and verifying correctness on polynomial factors used in the `x/inflation` of the
network's source code.

- [Hacking](#hacking)
- [Run the Tokenomics Dashboard](#run-the-tokenomics-dashboard)

## Hacking

```bash
cargo install just
```

```bash
just
```

## Run the Tokenomics Dashboard

```bash
just i # install
just run
```

This should display "Dash is runnning on http://127.0.0.1:8050/", or another
similar success message.

## Reference Links

- [Public Tokenomics | Nibiru Chain](https://nibiru.fi/docs/learn/tokenomics.html)
- [Internal Tokenomics | Nibiru Chain [NOTION]](https://www.notion.so/nibiru/Tokenomics-Nibiru-Chain-Internal-8150f253bbc14fd2a6f7fcc976b7b07d?pvs=4)

## Task Tracking

- [ ] docs: Explain directory strucutre 
- [ ] feat: add `just` command for generating the tex pdf
- [ ] feat: add latex dependency installation to the `just i`.
