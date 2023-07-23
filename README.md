## How to run
### Install poetry
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

### Install dependencies
```bash
poetry install
```

#### Run the bot
Create `.env` with the discord bot token. The token can be found in the discord developer portal.
You can copy the `.env.example` file and replace the token with your own.
```
$ cp .env.example .env
```

Then run the bot with
```bash
$ poetry run run-revealerbot
```

## Development

### Solidity smart-contracts testing
For testing the solidity contracts, you need to use the ape tool.
```
$ ape plugins install solidity
$ ape test
```

### Automatic code formatting and linting
Install precommit hook
```
$ pre-commit install
```
Now the code will be formatted and linted before every commit.
