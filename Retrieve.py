import pyperclip

from dbconfig import dbconfig

from rich import print as printc
from rich.table import Table
from rich.console import Console

from AddEntries import compute_master_key
import aesutil

def retrieve_entries(mp, ds, search, decrypt_password=False):
    db = dbconfig()
    cursor = db.cursor()

    if len(search) == 0:
        query = "SELECT* FROM PasswordManager.entries"
    else:
        query = "SELECT* FROM PasswordManager.entries WHERE"
        for i in search:
            query += f" {i} = '{search[i]}' AND "
        query = query[:-5]

    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) == 0:
        printc("[yellow][-][/yellow] No results for the search")
        return

    if (decrypt_password and (len(results) > 1)) or (not decrypt_password):
        table = Table(title="RESULTS")
        table.add_column("Site Name")
        table.add_column("URL")
        table.add_column("Email")
        table.add_column("Username")
        table.add_column("Password")

        for i in results:
            table.add_row(i[0], i[1], i[2], i[3], "{hidden}")

        console = Console()
        console.print(table)
        return

    if len(results) == 1 and decrypt_password:
        mk = compute_master_key(mp, ds)

        decrypted = aesutil.decrypt(key=mk, source=results[0][4], keyType="bytes")

        pyperclip.copy(decrypted.decode())
        printc("[green][+][/green] Password copied to clipboard")

        db.close()
