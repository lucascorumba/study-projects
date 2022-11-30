# Inverted Index
>tl;dr this project involves data extraction from the Twitter API, data cleaning, data loading and creation of a inverted index of tweets text using PostgreSQL.

## Overview

### Indexes
When retrieving values from tables, a *sequential scan* is **avoided whenever possible**. One way to improve queries performance is making **indexes**. This increase in performance comes with extra cost of memory and processing. 
We can think of indexes as *hints* to where rows are located within a table. Or even data about location of data.
>Actually, they are hints to which **block** contains the queried data, but delving into this is beyond the scope of this project. I think a "key-to-row hint" analogy should suffice.

There are different kinds of indexes in PostgreSQL, and we can divide them in ==**forward indexes**==(the "normal" index) and ==**inverted indexes**==. 
By default, a statement like the one below will create a **B-tree** index (one of the forward indexes), which is good for most cases.
```
CREATE INDEX name ON table (column);
```
We can specify what kind of index we want to build with the `USING` clause:
```
CREATE INDEX name ON table USING HASH (column);
```
This one created a **hash** index, also one of the forward indexes.

Also, we are not limited to indexing columns (in fact, there are tons of quirks and options. To check all of them, see the [documentation](https://www.postgresql.org/docs/current/sql-createindex.html)), the key field(s) for the index can be specified as **expressions**. As long as we use the same expression in the *WHERE* clause, it will work just fine. 
We will do that soon. But before that, let's take a better look at **inverted indexes**.

### Inverted Indexes
It's all a matter of *what you have* and *what are you trying to find*.
In forward indexes, the general idea is that from a key (indexed) value, a row can be found. 
Inverted indexes goes the other way around, we present a **query** and get back a list of *all* rows that match that query. 
A forward index would store:
```
{ doc_1: ["SQL is awesome"] }
```
While an inverted index would store:
```
{ "SQL": [doc_1], "is": [doc_1], "awesome": [doc_1] }
```
It works when you have a column with more than one thing, like a text (texts have multiple words). In a way, this column will have *multiple keys*. Other way to put it is that we get a mapping from the keyword to the document.
In this context, we are not interested in finding one specific row, but finding a set of rows instead.
For instance, we could query for texts that contain the word "SQL" and get back all the documents that match our query.
In fact, one of the main uses for inverted indexes is fast text search.

*To see all PostgreSQL indexes types, check the [documentation](https://www.postgresql.org/docs/current/indexes-types.html).*

Just like B-trees for forward indexes, the preferred text search-type index is the **Generalized Inverse Index** (GIN). It provides exact matches and efficiency on lookups, but can be costly for inserts and updates.
One workaround for this downside is to load all the data and build the GIN *later*. But if the insert/update overhead is too great and lookup is not a priority, a **Generalized Search Tree** (GiST) might be better suited.

>In this project, I built a GIN after extracting all the data I wanted.
I went this way because my project outline was to load about 10.000 tweets and stop there. In a task with constant load of tweets and eventual lookups, a GiST would be a better idea.

*More on that: [PostgreSQL documentation](https://www.postgresql.org/docs/11/textsearch-indexes.html).*

### Making Inverted Indexes with PostgreSQL
The statement to make a GIN (or GiST) index is really the same as the one used for forward indexes:
```
CREATE INDEX name ON table USING GIN (column);
```
The difference lies in what we can use in the `column` field: a **`tsvector`**. 

But what is a tsvector? To answer that we should dig into **Text Search Functions**.

#### Text Search Functions
From PostgreSQL [documentation](https://www.postgresql.org/docs/9.1/datatype-textsearch.html):
>"PostgreSQL provides two data types that are designed to support full text search, which is the activity of searching through a collection of natural-language documents to locate those that best match a query. The **tsvector** type **represents a document** in a form optimized for text search; the **tsquery** type similarly **represents a text query**."

Very nice. But let's take a look at it to get a better picture:
![demo 1 of to_tsvector function](../readme-imgs/to_tsvector-example-1.png)
`to_tsvector()` takes two parameters, the **language** in what the document is written and the **document** itself. 
This function reduces a document text to *tsvector*, or put in another way, returns a list of words that represent the document. Sort of *reduces a document to its essence*.
The numbers are the positions of the words in the document.
Notice that not all words are returned, and even the ones that were are different. That's because they were **stemed**.
>Stemming is the process of reducing a word to its word stem.

## Requirements
(Optional) It's recommended to not install required packages globally, but locally under a project subfolder using `venv`: 
```
python3 -m venv venv

# Windows
venv-name\Scripts\activate.bat    # cmd
venv-name\Scripts\activate.ps1    # Power Shell

# Unix
source venv-name/bin/activate
```
```
pip install psycopg2-binary
```
```
pip install requests
pip install requests-oauthlib
```

## Usage
```
source venv/bin/activate
```
```
export BEARER_TOKEN=<your_bearer_token>
```