# MementoMori X-to-Discord Bridge

A lightweight GitHub Action that polls the MementoMori (JP) X feed via Nitter and pushes updates to Discord using vxtwitter embeds.

## How It Works

* Source: Polls the @mementomori_boi RSS feed via Nitter.
* Link Conversion: Automatically converts X/Twitter links to vxtwitter.com to ensure video and image previews render correctly in Discord.
* Automation: Runs entirely on GitHub Actions—no local hosting or 24/7 PC required.
* Time Window: Specifically configured to check for posts within a 125-minute window to match the 2-hour cron schedule.

## Setup

### 1. Discord Webhook
1. In Discord, go to Server Settings > Integrations > Webhooks.
2. Create a new webhook and copy the URL.

### 2. GitHub Secrets
1. Go to your GitHub Repository Settings.
2. Navigate to Secrets and variables > Actions.
3. Click New repository secret.
4. Name: DISCORD_WEBHOOK
5. Value: (Paste your webhook URL)

### 3. Deployment
Simply push the tweet_poster.py and .github/workflows/main.yml files to your repository. The action is set to run automatically every 2 hours.

## Manual Trigger
If you want to test the script immediately:
1. Go to the Actions tab in your GitHub repo.
2. Select Run X Feed Filter on the left.
3. Click Run workflow > Run workflow.

## Technical Notes
* Dependencies: Uses requests, beautifulsoup4, and lxml for robust RSS parsing.
* Redundancy: The script uses vxtwitter redirection to bypass Discord's native embed limitations for X.
* Version: 1.0.
