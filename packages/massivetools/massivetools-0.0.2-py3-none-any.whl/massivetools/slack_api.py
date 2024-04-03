from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

class SLACK:
    def __init__(self , author = 'anonymous') -> None:
        self.client = WebClient(token="xoxb-6042172805714-6065174408160-pTaAXM0D11PSjSFUAHQ0vTf0")
        self.author = author
    def create_message(self, channel, alert_text, author):
        pass
    
    def author_block(self):
        return {
            "type": "context",
            "elements": [
                {
                    "type": "plain_text",
                    "text": f"Author: {self.author}",
                    "emoji": True
                }
            ]
        }
    
    def title_block(self):
        return {
            "type": "header",
            "text": {
                "type": "plain_text",
                "text": "Important Alert!",
                "emoji": True
            }
        }
    def text_block(self , text):
        text_block = {
            "type": "rich_text",
            "elements": [
                {
                    "type": "rich_text_section",
                    "elements": [
                        {
                            "type": "text",
                            "text": f"{text}"
                        }
                    ]
                }
            ]
        }
        return text_block
    def create_block(self , color , title , text):
        blocks = []
        blocks.append(self.title_block())
        blocks.append(self.text_block(text))
        blocks.append(self.author_block())
        attachments = [
                {
                    "color": color,
                    "blocks": blocks
                }
            ]
        return attachments
    
    def send_message(self, channel, attachments):
        self.client.chat_postMessage(channel = channel, attachments = attachments)
        
if __name__ == "__main__":
    slack = SLACK()
    message = slack.create_block("#36a64f" , "Important Alert!" , "Restart hopper AI script")
    slack.send_message("test" , message)