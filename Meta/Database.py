class Database:

    def __init__(self, query, qtype):
        self.query = query.lower()
        self.type = qtype
