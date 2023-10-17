from model import annoattr, annotag, annoclass, annoscene, annoattritem


# Let's just use the local mongod instance. Edit as needed.

# Please note that MONGO_HOST and MONGO_PORT could very well be left
# out as they already default to a bare bones local 'mongod' instance.
MONGO_HOST = 'mongodb'
# MONGO_HOST = '203.156.220.13'
MONGO_PORT = 27017

# Skip these if your db has no auth. But it really should.
# MONGO_USERNAME = '<your username>'
# MONGO_PASSWORD = '<your password>'

MONGO_DBNAME = 'annodict'

# Enable reads (GET), inserts (POST) and DELETE for resources/collections
# (if you omit this line, the API will default to ['GET'] and provide
# read-only access to the endpoint).
# RESOURCE_METHODS = ['GET', 'POST']

# Enable reads (GET), edits (PATCH), replacements (PUT) and deletes of
# individual items  (defaults to read-only item access).
# ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

X_DOMAINS = ['*']
X_HEADERS = ['Content-Type', 'If-Match']  # Needed for the "Try it out" buttons
IF_MATCH = False

PAGINATION_LIMIT = 1000

DOMAIN = {
    'annotag': annotag,
    'annoclass': annoclass,
    'annoattr': annoattr,
    'annoscene': annoscene,
    'annoattritem': annoattritem,
}
