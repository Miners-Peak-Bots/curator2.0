def parse_entities(msg):
    """
    Iterates Message.entities and prepares
    an array of objects that can later be
    easily worked with for identifying forbidden
    chats, links etc.
    """
    if not msg.entities:
        return []
    parsed = []
    text = msg.text
    for entity in msg.entities:
        offset = entity.offset
        length = entity.length
        msg_text = text[offset:(offset+length)]
        parsed.append(
            {
                'token': msg_text,
                'token_type': entity.type
            }
        )
    return parsed
