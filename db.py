import sys
from pathlib import Path

# библиотека pg8000 подключена как git submodule
sys.path.insert(0, str(Path(__file__).parent / "lib" / "postgresql" / "src"))

import pg8000.native

from calculator import add, mul, sub
from db_config import DB_CONFIG

con = pg8000.native.Connection(**DB_CONFIG)
con.run("CREATE TABLE IF NOT EXISTS results (id SERIAL PRIMARY KEY, expr TEXT, value INT)")
for expr, value in [("2 + 3", add(2, 3)), ("5 - 2", sub(5, 2)), ("4 * 6", mul(4, 6))]:
    con.run("INSERT INTO results (expr, value) VALUES (:e, :v)", e=expr, v=value)
print("pg8000", pg8000.__version__)
for row in con.run("SELECT * FROM results ORDER BY id"):
    print(row)
con.close()
