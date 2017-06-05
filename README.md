
# LunchPlejs (Slack bot)

![](https://s23.postimg.org/kvdvoj3wr/hungrybunny.png)

Recommends (by randomizing) a lunch place in central Stockholm by parsing HTML from http://www.kvartersmenyn.se/.


## Install

Install Python 2.x (developed with Python 2.7.13).

Install used libraries:

`pip install SlackClient`

`pip install beautifulsoup4`


Create a new bot in the Slack admin console and export the token:

`
export SLACK_BOT_TOKEN=[my-token]
`

Find the bot id and export it as well:

`
export BOT_ID=[my-bot-id]
`

How to perform the above steps is nicely described here:

https://www.fullstackpython.com/blog/build-first-slack-bot-python.html


## Run

`
python lunch_plejs.py
`

Invite the bot to a Slack channel.

Get a lunch recommendation by writing:

`@lunchplejs tips`

Print usage:

`@lunchplejs hjälp`
