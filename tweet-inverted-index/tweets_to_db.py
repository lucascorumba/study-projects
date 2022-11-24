import psycopg2
import hidden
from get_tweets import get_tweets
import utils


# get PostgreSQL credentials
secrets = hidden.pg_secrets()

# connects to PostgreSQL
conn = psycopg2.connect(host=secrets['host'],port=secrets['port'], connect_timeout=5,
        database=secrets['database'], user=secrets['user'], password=secrets['pass'])

# get cursor
cur = conn.cursor()

# create table
sql = "CREATE TABLE IF NOT EXISTS tweet(id BIGINT, body VARCHAR(280) NOT NULL, \
    author_id BIGINT NOT NULL, created_at TIMESTAMPTZ NOT NULL, PRIMARY KEY (id));"
cur.execute(sql)

# get tweets from a single request (quantity specified in "max_results" parameter)
tweets = get_tweets()

# counter for inserts in the database
count = int()

# iterate through all tweets
for i in tweets.get('data'):
    # tweet text
    text = i['text']
    # entities to  be removed
    remove = ('mentions', 'urls')
    text = utils.remove_entities(text, i['entities'], remove)
    
    # remove emojis, leading and trailing whitespaces
    text = utils.clean_text(text)

    # skip tweets without text left
    if len(text) < 1: continue

    # get tweet id, author id, created time
    tweet_id, author_id, created_at = i['id'], i['author_id'], i['created_at']

    # insert tweet data into database
    sql = "INSERT INTO tweet (id, body, author_id, created_at) VALUES (%s, %s, %s, %s) \
        ON CONFLICT (id) DO NOTHING RETURNING id"
    cur.execute(sql, (tweet_id, text, author_id, created_at))

    # count inserts into database
    if cur.fetchone() is not None: count = count + 1

    #print(f"\nORIGINAL TWEET: {i['text']}\nCLEANED TWEET: {text}\n\n \
    #    TWEET {i['id']} - CREATED AT: {i['created_at']}\t BY: {i['author_id']}\n \
    #    ----------------------------------------------------------------------------------")

print(f"API request retrieved {tweets['meta']['result_count']} tweets")

# commit changes to database and close cursor
conn.commit()
cur.close()

print(f"{count} records written on disk")