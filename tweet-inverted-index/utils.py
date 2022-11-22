def remove_entities(text, entities, remove):
    """
    Receives original tweet and using the response data removes all entities
    (mentions, urls, ...) by stringn slicing, leaving only the text. 
    """
    # used to 'update' index as slicing happens
    trim = int()

    # repeat for every field specified in 'remove'
    for field in remove:
        try:
            for item in entities[field]:
                start, end = item['start'] - trim, item['end'] - trim + 1
                text = text.replace(text[start:end], '', 1)
                trim = trim + (end - start)
        # if field does not exist -> proceed
        except KeyError:
            pass
    return text