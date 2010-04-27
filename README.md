
MongoLog : Centralized Logging made simple using MongoDB
========================================================

Setup
-----

Before using this handler for logging you will need to create
a capped collection on the mongodb server.

You can do this using the following commands in the mongo shell:

        > use mongolog
        > db.createCollection('log', {capped:true, size:100000})

... and you are ready. Running stats() on log collection should 
show something like this:

        > db.log.stats()
        { "ns" : "mongolog.log", "count" : 0, "size" : 0, "storageSize" :
        100096, "numExtents" : 1, "nindexes" : 0, "lastExtentSize" : 100096,
        "paddingFactor" : 1, "flags" : 0, "totalIndexSize" : 0, "indexSizes" : {
        }, "capped" : 1, "max" : 2147483647, "ok" : 1 }


Usage
-----

        import logging
        from mongolog.handlers import MongoHandler

        log = logging.getLogger('demo')
        log.setLevel(logging.DEBUG)

        log.addHandler(MongoHandler.to(db='mongolog', collection='log'))

        log.debug('Some message')


Check the samples folder for more details

Why centralized logging?
------------------------

- easy troubleshouting:
    - having the answers to why? quickly and accurately
    - for troubleshouting while the system is down
    - removed risk of loss of log information
- resource tracking
- security

What is MongoDB?
----------------

"Mongo is a high-performance, open source, schema-free document-oriented database."

It can eficiently store arbitrary JSON objects.
You can read more at http://www.mongodb.org/


Why MongoDB is great for logging?
---------------------------------

- MongoDB inserts can be done asynchronously 
- old log data automatically LRU's out thanks to capped collections
- it's fast enough for the problem 
- document-oriented / JSON is a great format for log information

Read more about this subject on the mongoDB blog: http://blog.mongodb.org

Have fun!

