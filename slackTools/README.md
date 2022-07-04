
# Getting Started...
**CONFIGURE YOUR KEYS** in the file __slack.keys__. <br>
To make it global (to your system), it is suggested to copy the file to __~/.slack/slack.keys__.

# Installing slackTools
## Installing slackTools using pip
```Bash
python3 setup.py check
python3 setup.py sdist
pip3 install .
```
**OR** (if you have an existing install)
```Bash
python3 setup.py check
python3 setup.py sdist
pip3 install --upgrade .
```

To Uninstall:
```Bash
pip3 uninstall slackTools
```
**See install.sh**

## Installing slackTools as an executible

### Create executible
```Bash
python3 setup.py check
python3 setup.py sdist
pyinstaller --name slackTools --onefile slackTools/__main__.py 
```
### Install to user
```Bash
cp ./dist/slackTools ~/.local/bin/.
```
**<!> CHECK** that local user programs are added to PATH in `~/.bashrc` by adding:
```Bash
export PATH="$HOME/.local/bin:$PATH"
```
And then reload bashrc:
```Bash
source ~/.bashrc
```
**See install.sh**

## What keys do I need?
You need a webhook key (easy, but text only) or a bot Token (__*slightly*__ harder, but can post <u>*messages* **and** *files</u>* to *any channel*). <br>
for webhooks, see: https://api.slack.com/messaging/webhooks <br>
for bot tokens, see: https://api.slack.com/authentication/basics <br>

## Should I leave JF as the default person to notify?
**Absolutely**. JF is deeply invested in your success and would appreciate regular updates on progress (be it a success or failure). <br>

## Mentioning a User in markdown
It's silly, but to annoy JF, you can't just to `@JF`. <br>
Instead, you must look up his _member ID_ on slack (click his profile, *U0141TNJ5UH*) and then you simply abuse as needed: <br>
`HEY! <@U0141TNJ5UH>! I can now bug you directly from my app!`

# How do I make super Markdown (__mrkdwn__) blocks for slack?
See https://api.slack.com/reference/block-kit/blocks#image <br>
See https://api.slack.com/messaging/composing/layouts#when-to-use-attachments <br>

# What are some usage examples?
## Pipe stdin using bash
```Bash
printf "hello \n there \n general \n kenobe \n my score acc=98 \n which is good" | python3 slackTools -e general "acc=[5-9]\d|\d{3,}" -n ian
```
which outputs (['jf'] will appear as @jf in slack):
```
-- START stdin pipe --
hello 
there 
general 
Event!['jf'] Regex "general" was triggered
kenobe 
my score acc=98 
Event!['jf'] Regex "[5-9]\d|\d{3,}" was triggered
which is good
-- END stdin pipe -
```

## In a python project
See __slackTools.py__

### Using a webhook
```python
'''Uses generic SLACK_WEBHOOK_TOKEN, which can post messages (text and markdown ONLY, through blocks and attachments)'''

import slackTools
slack = slackTools.SlackTools_webhook()

slack.sendMessage(message="Hello World Message!!", webhook_key='SLACK_WEBHOOK_TOKEN')
slack.sendMarkdown(message="~Hello~ \n> *Markdown* _world_`!!`", header="My Title",  webhook_key='SLACK_WEBHOOK_TOKEN')
```

### Using a bot token
```python
'''Uses SLACK_BOT_TOKEN which has more universal access (can post to different channels)'''
import slackTools
slack = slackTools.= SlackTools_bot()

# Danger! Must use SLACK_BOT_TOKEN with OAuth Scope set for chat:write
slack.sendMessage(message="Hello World Message!!", channel_id=None, bot_key='SLACK_BOT_TOKEN')
slack.sendMarkdown(message="~Hello~ \n> *Markdown* _world_`!!`", header="My Title",  channel_id=None, bot_key='SLACK_BOT_TOKEN')

# Danger! Must use SLACK_BOT_TOKEN with OAuth Scope set for files:write
slack.sendFile(filePath="avatar.png", title="my file name", message="Here is my file", channel_id=None, bot_key='SLACK_BOT_TOKEN')
```