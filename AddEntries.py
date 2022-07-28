from getpass import getpass

from Crypto.Hash import SHA512
from Crypto.Protocol.KDF import PBKDF2
from rich import print as printc

import aesutil
from dbconfig import dbconfig


def compute_master_key(mp, ds):
    password = mp.encode()
    salt = ds.encode()
    key = PBKDF2(password, salt, 32, count=1000000, hmac_hash_module=SHA512)
    return key


def checkEntry(sitename, siteurl, email, username):
    db = dbconfig()
    cursor = db.cursor()
    query = f"SELECT * FROM PasswordManager.entries WHERE sitename = '{sitename}' AND siteurl = '{siteurl}' AND email = '{email}' AND username = '{username}'"
    cursor.execute(query)
    results = cursor.fetchall()

    if len(results) != 0:
        return True
    return False


def addEntry(mp, ds, sitename, siteurl, email, username):
    # Check if the entry already exists
    if checkEntry(sitename, siteurl, email, username):
        printc("[yellow][-][/yellow] Entry with these details already exists")
        return

    # Input Password
    password = getpass("Password: ")

    # compute master key
    mk = compute_master_key(mp, ds)

    # encrypt password with mk
    encrypted = aesutil.encrypt(key=mk, source=password, keyType="bytes")

    # Add to db
    db = dbconfig()
    cursor = db.cursor()
    query = "INSERT INTO PasswordManager.entries (sitename, siteurl, email, username, password) values (%s, %s, %s, %s, %s)"
    val = (sitename, siteurl, email, username, encrypted)
    cursor.execute(query, val)
    db.commit()

    printc("[green][+][/green] Added entry ")
