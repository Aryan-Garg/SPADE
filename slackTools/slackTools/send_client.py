from pydoc import text
from slack_sdk.web import WebClient

''' Note!
Why create the webhook client each time?
It allows slackTools to connect to multiple webhooks/endpoints
'''

def sendMessage(bot_token, message, channel_id):
    # Send the message
    sendBlock(bot_token, channel_id, text=message)

def sendMarkdown(bot_token, channel_id, header, message):
    # Create Blocks
    blocks = []
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
    sendBlock(bot_token, channel_id, blocks=blocks)

# See https://api.slack.com/reference/block-kit/blocks#image
# See https://api.slack.com/messaging/composing/layouts#when-to-use-attachments
def sendBlock(bot_token, channel_id, blocks=[], attachments=[],  text=''):
    
    # Posting messages requires the `chat:write` scope
    if len(blocks) >= 1 or len(attachments) >= 1 or len(text)>=1:
        client = WebClient(bot_token)
        response = client.chat_postMessage(
            channel=channel_id,
            text=text,
            blocks=blocks,
            attachments=attachments,
        )
        assert response.status_code == 200

def sendFile(bot_token, channel_id, filePath, message='', title=''):
    client = WebClient(bot_token)

    # Uploading files requires the `files:write` scope
    response = client.files_upload(
        channels=channel_id,
        file=filePath,
        title=title, 
        initial_comment=message
    )
    assert response.status_code == 200
    