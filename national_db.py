#!/usr/bin/env python3

import sqlite3 as sql
import os
from typing import List, Dict, Any




class database:
    #function to creat a DB or connect on it , if it is there
    #input = path of DB is already there or the DB which you want to creat
    def __init__(self,path:str):
        # save a DB in a dedicated path on Dedicated folder
        folder = os.path.dirname(path)
        if folder and not os.path.exists(folder):
            os.makedirs(folder, exist_ok=True)

        #creat a DB var and link it with the public one
        conn = sql.connect(path, check_same_thread=False)

        #creat a cursor var and link it with the public one
        cur = conn.cursor()

        #give sql command to DB and set the setting
        cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            text TEXT NOT NULL
        )
        """)

        conn.commit()

        #save connect info in self var
        self.__conn = conn
        self.__cur = cur



    #function of add , it is add data to the DB
    #data = {"neme" : "the name", "text" : "the msg"}
    def add_user(self,data: Dict[str, str]) -> Dict[str, Any]:
        # get connect info from self var
        conn = self.__conn
        cur = self.__cur

        #get user info
        name = data["name"]
        text = data["text"]

        if not cur: # to make sure that the program get connect with DB and give an error msg if it did not connect
            return {"ok": False, "error": "DB not initialized"}
        
        # check the type of data
        if not isinstance(data["text"],str) or not isinstance(data["name"],str):
            return {"ok": False, "error": "name and text required"}        

        # Verify the parameter
        if not name or not text:
            return {"ok": False, "error": "name and text required"}

        #to check that no duplicate msg
        cur.execute("SELECT 1 FROM messages WHERE text = ?", (text,))
        if cur.fetchone():
            return {"ok": False, "error": "duplicate"}

        #to insert a msg
        cur.execute("INSERT INTO messages (name, text) VALUES (?, ?)", (name, text))
        conn.commit()
        return {"ok": True}

    
    def pop_messages(self,limit: int = 200) -> List[Dict[str, Any]]:
        # get connect info from self var
        conn = self.__conn
        cur = self.__cur

        if cur is None: # to make sure that the program get connect with DB and give an error msg if it did not connect
            return []

        #to select data from th DB and make sure that it will del when we select it
        cur.execute("BEGIN")
        cur.execute("SELECT id, name, text FROM messages ORDER BY id ASC LIMIT ?", (limit,))
        rows = cur.fetchall()
        ids = [r[0] for r in rows]
        if ids:
            #del the data from the DB
            q = ",".join("?" for _ in ids)
            cur.execute(f"DELETE FROM messages WHERE id IN ({q})", ids)

        conn.commit()

        return [{"id": r[0], "name": r[1], "text": r[2]} for r in rows]