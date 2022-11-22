import psycopg2
import hidden
from get_tweets import get_tweets
import utils


# get PostgreSQL credentials
secrets = hidden.pg_secrets()

# connects to PostgreSQL
conn = psycopg2.connect(host=secrets['host'],port=secrets['port'], connect_timeout=5,
        database=secrets['database'], user=secrets['user'], password=secrets['pass'])

# cursor
cur = conn.cursor()

tweets = get_tweets()

# get tweets from a single request (specified in "max_results" parameter)
for i in tweets.get('data'):
    # tweet text
    text = i['text']
    # entities to  be removed
    remove = ('mentions', 'urls')
    text = utils.remove_entities(text, i['entities'], remove)
    
    # remove emojis
    text = text.encode('cp860', 'ignore').decode('cp860')

    print(f"\nORIGINAL TWEET: {i['text']}\n")
    print(f"CLEANED TWEET: {text.strip()}\n")
    print("---------------------------------------------------------------------")

print(f"retrieved {tweets['meta']['result_count']} tweets")