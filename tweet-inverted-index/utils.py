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

#import re
def clean_text(text):
    """
    Receives text and removes emojis, leading and trailing whitespaces,
    as well as extra spaces between words.
    To remove emojis and keep portuguese characters, the text is encoded 
    and decoded using the cp860 encoding.
    """
    # remove emojis, leading and trailing whitespaces
    text = text.encode('cp860', 'ignore').decode('cp860').strip()
    
    ## regex option for extra spaces: 
    ## re.sub(r'\s+', ' ', text)
    # remove extra spaces between words
    return ' '.join(text.split())
