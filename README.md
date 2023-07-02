# Aptos Celebtron

Celebtron explain the transaction of Aptos chain.

## Production Support:

In this version, we support explain 4 types of transaction below.

- TransferEvent
    + https://explorer.aptoslabs.com/txn/169646501?network=mainnet
- AirdropEvent
    + https://explorer.aptoslabs.com/txn/169470665?network=mainnet
- SwapEvent
    + https://explorer.aptoslabs.com/txn/169707501?network=mainnet
- LiqudityAddedEvent
    + https://explorer.aptoslabs.com/txn/169707427?network=mainnet

**Disclaimer**: For other transaction
types are working right now but we haven't tested yet. This is still in development phase.

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

## References

- https://aptos.dev/concepts/
- https://fullnode.devnet.aptoslabs.com/v1/spec#/
- https://explorer.aptoslabs.com/
