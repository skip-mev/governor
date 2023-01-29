<p align="center">
<a href="https://skip.money/#gh-light-mode-only">
<img width="75" src="https://raw.githubusercontent.com/skip-mev/governor/main/assets/light.svg#gh-dark-mode-only" align="right">
</a>
<a href="https://skip.money/#gh-dark-mode-only">
<img width="75" src="https://raw.githubusercontent.com/skip-mev/governor/main/assets/dark.svg#gh-dark-mode-only" align="right">
</a>
</p>

# Governor

Governor is a watcher that checks for upcoming upgrades in Cosmos SDK blockchains and notifies you about them in a Slack channel

## Example usage

Generate a Slack webhook token as shown in their [docs](https://api.slack.com/messaging/webhooks) and put it in the config file. 

```bash
cp ./config.yaml ./config.yaml.example
docker compose up -d
```

## How it works

Governor spins up a chain monitor per every chain and queries the `/cosmos/upgrade/v1beta1/current_plan` and checks if there is
an upcoming upgrade. If there is an upcoming upgrade, it stores it in the local database and sends a request to the Slack webhook.
