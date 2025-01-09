from datetime import date, datetime, time

def serialize_date(obj):
    """序列化日期对象为字符串"""
    if isinstance(obj, datetime):
        return obj.strftime('%Y-%m-%d %H:%M:%S')
    if isinstance(obj, time):
        return obj.strftime('%H:%M:%S')
    if isinstance(obj, date):
        return obj.strftime('%Y-%m-%d')
    return obj

def format_alpaca_messages_to_list_json(messages: list) -> list:
    formatted_messages = []
    for message in messages:
        temp_messages = []
        for msg in message["history"]:
            temp_messages.append({
                "timestamp": msg["timestamp"],
                "role": "user",
                "content": msg["student_question"]
            })
            temp_messages.append({
                "timestamp": msg["timestamp"],
                "role": "assistant",
                "content": msg["ai_response"]
            })
        temp_messages.append({
            "timestamp": message["timestamp"],
            "role": "user",
            "content": message["student_question"]
        })
        temp_messages.append({
            "timestamp": message["timestamp"],
            "role": "assistant",
            "content": message["ai_response"]
        })
        formatted_messages.append(temp_messages)
    return formatted_messages

def format_list_json_to_alpaca_messages(messages: list) -> dict:
    """
    Format the list of messages to the alpaca format
    The list of messages is a list of dictionaries with the following keys:
    - timestamp: the timestamp of the message
    - role: the role of the message (user or assistant)
    - content: the content of the message
    The function will return a dictionary with the following keys:
    - timestamp: the timestamp of the last message
    - student_question: the student question
    - ai_response: the ai response
    - history: the history of the messages
    - details: the details of the message
    """
    if len(messages) % 2 != 0:
        messages.append({
            "timestamp": datetime.now().timestamp(),
            "role": "assistant",
            "content": ""
        })
    formatted_messages = {}
    history = []
    for message in range(0,len(messages)-2,2):
        message_pair = messages[message:message+2]
        history.append({
            "timestamp": message_pair[0]["timestamp"],
            "student_question": message_pair[0]["content"],
            "ai_response": message_pair[1]["content"],
        })
    formatted_messages["history"] = history
    formatted_messages["timestamp"] = messages[-2]["timestamp"]
    formatted_messages["student_question"] = messages[-2]["content"]
    formatted_messages["ai_response"] = messages[-1]["content"]
    formatted_messages["details"] = {"summary": ""}
    return formatted_messages
