# Standard
from datetime import datetime

# Custom
try:
    from . import keys
    from . import send_client, send_webhook
except:
    import keys
    import send_client, send_webhook

''' Slack Class
Encompasses config for interacting with slack and 
encapsulates basic routines
'''
class SlackTools:
    def __init__(self, filePath_slackKeys="~/.slack/slack.key", default_keyName='SLACK_WEBHOOK_TOKEN', default_channelName='SLACK_CHANNEL_ID', strip=True):
        # Copy defaults
        self.default_keyName=default_keyName
        self.default_channelName=default_channelName
        self.notify_init_del = not strip

        # Get hostname (best system ID)
        import socket
        self.hostname=socket.gethostname()

        # Load keys
        self.keys=keys.load(filePath_slackKeys)

        # Notify of initialization
        if self.notify_init_del:
            time = datetime.now().strftime('%d/%m/%Y %a %H:%M:%S %Z')
            self.time_lastMessage = time # Copy to init
            self.sendMessage(time+":: slackTools was initialized on "+self.hostname)
            print(time+":: slackTools was initialized on "+self.hostname)

    def __del__(self):
        # Notify of destruction
        if self.notify_init_del:
            try:
                notify=''
                for user in self.keys['NOTIFY_ON_EVENT']:
                    notify += self.keys['USERS'][user]
                self.sendMessage(self.time_lastMessage+":: "+notify+" slackTools was terminated on "+self.hostname)
                print(self.time_lastMessage+":: slackTools was terminated on "+self.hostname)
            except:
                print("????/??/?? :: slackTools was terminated on "+self.hostname)

    def sendMessage(self, message):
        print("SlackTools (Base) :: " + message)

    # Checks and Retrieves the slack_key from keys
    def checkKey(self, key=None):
        # Set default key (if none provided)
        key = key if key and key is not None else self.default_keyName
        if key not in self.keys:
            raise "<!> Slack ("+key+") is unrecognized"

        # Update time of last message (for __del__)
        try:
            self.time_lastMessage = datetime.now().strftime('%d/%m/%Y %a %H:%M:%S %Z')
        except:
            pass

        return self.keys[key]

    # Checks Retrieves the channel_ID from keys
    def checkChannel(self, key=None):
        # Set default key (if none provided)
        key = key if key and key is not None else self.default_channelName
        if key not in self.keys:
            raise "<!> Slack ("+key+") is unrecognized"
        return self.keys[key]



## WEBHOOK  ##
'''Uses generic SLACK_WEBHOOK_TOKEN, which can post messages (text and markdown ONLY, through blocks and attachments)'''
class SlackTools_webhook(SlackTools):
    def sendMessage(self, message="Hello World Message!!", webhook_key='SLACK_WEBHOOK_TOKEN'):
        send_webhook.sendMessage(webhook=self.checkKey(webhook_key), message=message)

    def sendMarkdown(self, message="~Hello~ \n> *Markdown* _world_`!!`", header="My Title", webhook_key='SLACK_WEBHOOK_TOKEN'):
        send_webhook.sendMarkdown(webhook=self.checkKey(webhook_key), header=header, message=message,)

    def sendBlock(self, blocks=[], attachments=[], text='', webhook_key='SLACK_WEBHOOK_TOKEN'):
        send_webhook.sendBlock(webhook=self.checkKey(webhook_key), blocks=blocks, attachments=attachments, text=text)


## BOT_TOKEN ##
'''Uses SLACK_BOT_TOKEN which has more universal access (can post to different channels)'''
class SlackTools_bot(SlackTools):

    # Danger! Must use SLACK_BOT_TOKEN with OAuth Scope set for chat:write
    def sendMessage(self, message="Hello World Message!!", channel_id=None, bot_key='SLACK_BOT_TOKEN'):
        send_client.sendMessage(bot_token=self.checkKey(bot_key), channel_id=self.checkChannel(channel_id), message=message)

    def sendMarkdown(self, message="~Hello~ \n> *Markdown* _world_`!!`", header="My Title",  channel_id=None, bot_key='SLACK_BOT_TOKEN'):
        send_client.sendMarkdown(bot_token=self.checkKey(bot_key), channel_id=self.checkChannel(channel_id), header=header, message=message)

    def sendBlock(self, blocks=[], attachments=[], text='', channel_id=None, bot_key='SLACK_BOT_TOKEN'):
        send_client.sendBlock(bot_token=self.checkKey(bot_key), channel_id=self.checkChannel(channel_id), blocks=blocks, attachments=attachments, text=text)

    # Danger! Must use SLACK_BOT_TOKEN with OAuth Scope set for files:write
    def sendFile(self, filePath="avatar.png", title="my file name", message="Here is my file", channel_id=None, bot_key='SLACK_BOT_TOKEN'):
        send_client.sendFile(self.checkKey(bot_key), channel_id=self.checkChannel(channel_id), filePath=filePath, message=message, title=title)
 

# Testing
# test = SlackTools()

# Test Webhook
# test = SlackTools_webhook()
# test.sendMessage()
# test.sendMarkdown()

# Test Bot
# test = SlackTools_bot()
# test.sendFile()
# test.sendMessage(channel_id=None)
# test.sendMarkdown(channel_id=None)

# TODO Notify on event