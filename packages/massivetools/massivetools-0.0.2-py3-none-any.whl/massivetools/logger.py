import logging
import datetime
import pytz

class Formatter(logging.Formatter):
    """override logging.Formatter to use an aware datetime object"""
    def converter(self, timestamp):
        # Create datetime in UTC
        dt = datetime.datetime.fromtimestamp(timestamp, tz=pytz.UTC)
        # Change datetime's timezone
        return dt.astimezone(pytz.timezone('Asia/Seoul'))
    def formatTime(self, record, datefmt=None):
        dt = self.converter(record.created)
        if datefmt:
            s = dt.strftime(datefmt)
        else:
            try:
                s = dt.isoformat(timespec='milliseconds')
            except TypeError:
                s = dt.isoformat()
        return s
    
def create_logger(script_name = '', level_name = 'INFO'):
    # 문자열로 된 로그 레벨을 상수로 변환
    level = logging.getLevelName(level_name.upper())
    if not isinstance(level, int):
        raise ValueError(f"Invalid log level: {level_name}")

    # 로그 생성
    logger = logging.getLogger()
    # 로그의 출력 기준 설정
    logger.setLevel(level)
    # log 출력 형식

    formatter = Formatter('%(asctime)s;%(name)s - %(levelname)s - %(message)s', '%Y-%m-%d %H:%M:%S')
    now = datetime.datetime.now()
    log_file_name = now.strftime("log_%Y_%m_%d_%H_%M_%S.log")
    # log를 파일에 출력
    file_handler = logging.FileHandler(f'./log/{script_name}_{log_file_name}.log')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # log 출력
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    
    return logger
def create_alert_message(channel, alert_text, author):
    ### Example usage:
    return {
        "channel": channel,
        "attachments": [
            {
                "color": "#EF002B",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": "Important Alert!",
                            "emoji": True
                        }
                    },
                    {
                        "type": "rich_text",
                        "elements": [
                            {
                                "type": "rich_text_section",
                                "elements": [
                                    {
                                        "type": "text",
                                        "text": alert_text
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "type": "context",
                        "elements": [
                            {
                                "type": "plain_text",
                                "text": f"Author: {author}",
                                "emoji": True
                            }
                        ]
                    }
                ]
            }
        ]
    }

