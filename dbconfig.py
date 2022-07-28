import sys

import mysql.connector
from rich import print as printc
from rich.console import Console
console = Console()

def dbconfig():
    try:
        db = mysql.connector.connect(
            host='localhost',
            user='root',
            password='kaloriasid'
        )

    except Exception as e:
        printc("[red][!]", e)
        console.print_exception(show_locals=True)
        sys.exit(0)

    return db


# dbconfig()
