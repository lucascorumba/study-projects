import psycopg2
import hidden
import get_tweets
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

# counter for inserts in the database / counter for total API requests
write_count, request_count = int(), int()

# get parameters to paginate()
url, params = get_tweets.create_url(), get_tweets.get_params(max_results=50)

print("Requesting tweets...")
# move forward through pages of results
for tweets in get_tweets.paginate(url, params):
    # iterate through all tweets in current 'page'
    for tweet in tweets.get('data'):
        # tweet text / entities to  be removed
        text, to_remove = tweet['text'], ('mentions', 'urls')
        text = utils.remove_entities(text, tweet['entities'], to_remove)
        
        # clean and format text
        text = utils.clean_text(text)

        # skip tweets without text left and ensures column size limit
        tweet_len = len(text)
        if tweet_len < 1 or tweet_len > 280: 
            continue

        # get tweet id, author id, created time
        tweet_id, author_id, created_at = tweet['id'], tweet['author_id'], tweet['created_at']

        # insert tweet data into database
        sql = "INSERT INTO tweet (id, body, author_id, created_at) VALUES (%s, %s, %s, %s) \
            ON CONFLICT (id) DO NOTHING RETURNING id"
        cur.execute(sql, (tweet_id, text, author_id, created_at))

        # count inserts into database
        if cur.fetchone() is not None: 
            write_count = write_count + 1

        #print(f"\nORIGINAL TWEET: {tweet['text']}\nCLEANED TWEET: {text}\n\n \
        #    TWEET {tweet['id']} - CREATED AT: {tweet['created_at']}\t BY: {tweet['author_id']}\n \
        #    ----------------------------------------------------------------------------------")

    page_count = tweets['meta']['result_count']
    request_count = request_count + page_count
    print(f"\t{page_count} tweets in this page ---- Total retrieved: {request_count}")

    # commit changes to database
    conn.commit()    

    print(f"\tTotal of {write_count} records written on disk\n")

    # conditions to automatically end retrieval - this endpoint returns the 800 most recent tweets
    if write_count >= 750 or request_count >= 750:
       break

print("Closing database connection...")
# close cursor and connection
cur.close()
conn.close()

print("Finished retrieval")

# run this SQL command in your client to build the inverted index - also in the .sql file
# CREATE INDEX gin ON tweet USING gin(to_tsvector('portuguese', body));

# see 'commands.sql' for query examples
# if you want to run all commands there, go to your client and use:  \i commands.sql