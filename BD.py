import sqlite3
from Error import Error


class Base:
    def __init__(self):
        self._con = sqlite3.connect("Error.db")
        self._cur = self._con.cursor()
        self._create_bd_()

    def __del__(self):
        self._con.close()

    def _create_bd_(self):
        self._create_table_errors_()
        self._create_table_solutions_()

    def _create_table_errors_(self):
        self._cur.execute('''CREATE TABLE IF NOT EXISTS errors(
    error_id INTEGER PRIMARY KEY,
    no TEXT NOT NULL UNIQUE,
    description Text NOT NULL
    );''')

    def _create_table_solutions_(self):
        self._cur.execute('''CREATE TABLE IF NOT EXISTS solutions(
    solution_id INTEGER PRIMARY KEY,
    error_id INTEGER NOT NULL,
    priority int NOT NULL,
    actions Text NOT NULL
    );''')

    def exist_error(self, code_no: int):
        errors_id = self._get_id_(code_no)
        return errors_id > 0

    def _get_id_(self, code_no):
        res = self._cur.execute(f"SELECT error_id FROM errors where no='{code_no}'")
        error_id = 0
        for r in res.fetchall():
            error_id = r[0]
        return error_id

    def load_test_data(self):
        self.add_errors(Error(1, "Не подключен <u>com port</u>",
                              solutions=[(2, "Замените провод"), (1, "Проверьте подключение провода")]))
        self.add_errors(Error(2, "Не подключен <u>принтер</u>",
                              solutions=[(3, "Замените принтер"), (1, "Проверьте подключение кабеля питания"), (2, "проверьте подключение интерфейсного кабеля")]))

    def getError(self, code_no):
        res = self._cur.execute(f"SELECT error_id, no, description FROM errors where no='{code_no}'")
        er = None
        id = 0
        for r in res.fetchall():
            id = r[0]
            er = Error(r[1], r[2], [])
        if er is not None:
            res = self._cur.execute(f"SELECT priority,actions FROM solutions where error_id='{id}'")
            for r in res.fetchall():
                er.solutions.append((r[0], r[1]))
        return er

    def add_errors(self, error: Error):
        self._cur.execute(f'''INSERT INTO errors(no, description) VALUES
               ('{error.no}', '{error.description}')
               ''')
        self._con.commit()
        id = self._get_id_(error.no)
        for pr, s in error.solutions:
            self._cur.execute(f'''INSERT INTO solutions(error_id, priority, actions) VALUES
                           ('{id}', '{pr}', '{s}')
                           ''')
        self._con.commit()
