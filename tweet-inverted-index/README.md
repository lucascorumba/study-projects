# Inverted Index
>tl;dr this project involves data extraction from Twitter API, data cleaning and creation of a inverted index using PostgreSQL.

## Overview
### Indexes and Inverted Indexes
When retrieving values from tables, a **sequential scan** is avoided whenever possible. To improve queries performance, there are **indexes**.
We can think of indexes as *hints* to where rows are located within a table. 
>Actually, they are hints to which **block** contains the queried data, but delving into this is outside the scope of this project. I think a "key-to-row hint" analogy should suffice.

There are different kinds of indexes in PostgreSQL, and we can divide them in **forward indexes**(the "normal" index) and **inverted indexes**. 
This increase in performance comes with extra cost of memory and processing. By default, a statement like the one below will create a **B-tree** index (one of the "normal" indexes), which is good for most cases.
```
CREATE INDEX index ON table (column);
```
We can specify what kind of index we want to build with the *USING* clause:
```
CREATE INDEX index ON table USING hash (column);
```
This one created a hash index.

Also, we are not limited to indexing columns (in fact, there are tons of quirks and options. To check all of them, see the [documentation](https://www.postgresql.org/docs/current/sql-createindex.html)), the key field(s) for the index can be specified as *expressions*. As long as we use the same expression in the *WHERE* clause, it will work just fine. We will do that soon. 


## Requirements
```py
pip install psycopg2-binary
```
```py
pip install requests
pip install requests-oauthlib
```

## Usage
```
python3 -m venv venv
source venv/bin/activate
```
```
export BEARER_TOKEN=<your_bearer_token>
```