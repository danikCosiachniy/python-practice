class FakeDB:
    """Фейковая БД: собирает вызовы execute/executemany/query, эмулирует transaction()."""
    def __init__(self):
        self.executed = []        # [(sql, params)]
        self.executed_many = []   # [(sql, list_of_tuples)]
        self.queries = []         # [(sql, params)]
        self._query_result = []

    # совместимость с контекстным менеджером
    def __enter__(self): return self
    def __exit__(self, exc_type, exc, tb): pass

    def connect(self): pass
    def close(self): pass

    def execute(self, sql, params=None):
        self.executed.append((sql, params))

    def executemany(self, sql, params_seq):
        seq = list(params_seq)
        self.executed_many.append((sql, seq))

    def query(self, sql, params=None):
        self.queries.append((sql, params))
        return list(self._query_result)

    # транзакция
    class _Tx:
        def __init__(self, outer): self.outer = outer
        def __enter__(self): return None
        def __exit__(self, exc_type, exc, tb): return False

    def transaction(self):  # with db.transaction():
        return FakeDB._Tx(self)

    # helper
    def set_query_result(self, rows):
        self._query_result = rows