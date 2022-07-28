import hashlib
import random
import string
import sys
from getpass import getpass

from dbconfig import dbconfig

from rich import print as printc
from rich.console import Console
console = Console()

def generate_device_secret(length=16):
    return "".join(random.choices(string.ascii_uppercase + string.digits, k=length))

def config():
    # Create a Database
    db = dbconfig()
    cursor = db.cursor()
    printc("[green][+] Creating new config [/green]")

    try:
        cursor.execute("CREATE DATABASE PasswordManager")
    except Exception as e:
        printc("[red][!]", e)
        console.print_exception(show_locals=True)
        sys.exit(0)

    printc("[green][+][/green] Database 'PasswordManager' created")

    # Create Tables
    query = "CREATE TABLE PasswordManager.secrets (masterkey_hash TEXT NOT NULL, device_secret TEXT NOT NULL)"
    cursor.execute(query)
    printc("[green][+][/green] Table 'secrets' created")

    query = "CREATE TABLE PasswordManager.entries (sitename TEXT NOT NULL, siteurl TEXT NOT NULL," \
            "email TEXT NOT NULL, username TEXT NOT NULL, password TEXT NOT NULL)"
    cursor.execute(query)
    printc("[green][+][/green] Table 'entries' created")

    while True:
        # mp = input("Choose a MASTER PASSWORD: ")
        # if not mp == input("Re-type: ") or mp is not None:
        #     break
        mp = getpass(prompt="Choose a MASTER PASSWORD: ")
        if mp == getpass(prompt="Re-type: ") and mp is not None:
            break
        printc("[yellow][-] Please try again. [/yellow]")

    # Hash the MASTER PASSWORD
    hashed_mp = hashlib.sha256(mp.encode()).hexdigest()
    printc("[green][+][/green] Generated hash of MASTER PASSWORD")

    # Generate a DEVICE SECRET
    ds = generate_device_secret()
    printc("[green][+][/green] DEVICE SECRET Generated")

    # Add them to db
    query = "INSERT INTO PasswordManager.secrets (masterkey_hash, device_secret) values (%s, %s)"
    val = (hashed_mp, ds)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Added to the database")
    printc("[green][+] Configuration done![/green]")

    db.close()


config()
