from slack_sdk.webhook import WebhookClient

''' Note!
Why create the webhook client each time?
It allows slackTools to connect to multiple webhooks/endpoints
'''

def sendMessage(webhook, message):
    # Send the message
    sendBlock(webhook, text=message)

def sendMarkdown(webhook, header, message):
    blocks = []

    # Copy header (No Markdown)
    if header and header is not None:
        blocks.append(
            {
                "type": "header",
                "text": {
                    "type": "plain_text",
                    "text": header
                }
            }
        )

    # Copy Message
    if message and message is not None:
        blocks.append(
            {
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": message
                }
            }
        )

    # Send the message
    sendBlock(webhook, blocks=blocks)

# See https://api.slack.com/reference/block-kit/blocks#image
# See https://api.slack.com/messaging/composing/layouts#when-to-use-attachments
def sendBlock(webhook, blocks=[], attachments=[], text=''):
    webhook = WebhookClient(webhook)
    if len(blocks) >= 1 or len(attachments) >= 1 or len(text) >=1:
        # Send the message
        response = webhook.send(
            text=text,
            blocks=blocks, 
            attachments=attachments
        )
        assert response.status_code == 200
        assert response.body == "ok"
