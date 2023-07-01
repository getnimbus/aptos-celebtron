# Aptos Celebtron

Celebtron explain the transaction of Aptos chain.

**Production Support**: In this version, we currently support explain 4 types of transaction. With other transaction
types haven't been tested yet but only development phase:

- TransferEvent
    + https://explorer.aptoslabs.com/txn/169646501?network=mainnet
- AirdropEvent
    + https://explorer.aptoslabs.com/txn/169470665?network=mainnet
- SwapEvent
    + https://explorer.aptoslabs.com/txn/169707501?network=mainnet
- LiqudityAddedEvent
    + https://explorer.aptoslabs.com/txn/169707427?network=mainnet

## Prequisites

- OpenAI API key
- Python >= 3.11

## How to run

1. Add `.env`

```dotenv
OPENAI_API_KEY=<your-openai-api-key>
```

or set ENV variable

```bash
export OPENAI_API_KEY=<your-openai-api-key>
```

2. Run api server

```bash
python server.py
```
