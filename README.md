A GitHub Action that polls the MementoMori (JP) X feed via Nitter and pushes updates to Discord using vxtwitter embeds.

## How It Works

* Source: Polls the @mementomori_boi RSS feed via Nitter.
* Link Conversion: Automatically converts X/Twitter links to vxtwitter.com to ensure video and image previews render correctly in Discord.
* Automation: Runs entirely on GitHub Actions—no local hosting or 24/7 PC required.
* Time Window: Specifically configured to check for posts within a set time window to match the automation schedule.

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

## Adjusting Check Intervals

To change how often the script runs and how far back it looks for tweets, you must update two separate files so they remain "in sync."

### A. Changing the Automation Frequency (main.yml)
Open `.github/workflows/main.yml` and locate the `cron` line. GitHub uses standard cron syntax:
* `cron: '0 */2 * * *'` — Runs every 2 hours (Default).
* `cron: '*/30 * * * *'` — Runs every 30 minutes.
* `cron: '0 * * * *'` — Runs every hour on the hour.

**Note:** GitHub Actions scheduled tasks can be delayed by 5–15 minutes depending on system load and for free users the runtime rate limit is 2000 minutes/month. If some tweets do not show up consider raising the time window it looks back, altho that may result in some tweet duplication post occasionally.

### B. Changing the Tweet Search Window (tweet_poster.py)
Open `tweet_poster.py` and locate the `timedelta` setting inside the `run_filter()` function. This tells the script how many minutes of history to check:
* `timedelta(minutes=125)` — Checks the last 2 hours + 15 min buffer (Default).
* `timedelta(minutes=35)` — Use this if you change the cron to run every 30 minutes.

**Rule of Thumb:** Always set the `minutes` in the script to be slightly higher (5–10 minutes) than your cron interval to account for GitHub's startup delays.

## Technical Notes
* Dependencies: Uses requests, beautifulsoup4, and lxml for robust RSS parsing.
* Redundancy: The script uses vxtwitter redirection to bypass Discord's native embed limitations for X.
* Version: 1.0.
