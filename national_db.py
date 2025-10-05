#!/usr/bin/env python3

# استدعاء مكتبات
import sqlite3 as sql
import os
from typing import List, Dict, Any

#تعريف متغيرات قاعدة البيانات
#identify the variables
conn = None
cur = None

#دالة انشاء قاعدة بيانات او الاتصال بقاعدة بيانات موجودة
#function to creat a DB or connect on it , if it is there
#المدخلات = مسار قاعدة البيانات الي تباه
#input = path of DB is already there or the DB which you want to creat
def creat_db(path: str):
    global conn, cur  #(لمنع مشاكل المتغيرات # to prevent problem
    #تخزين قاعدة البيانات في مسار مخصص داحل مجلد مخصص يدخله المستخدم
    # save a DB in a dedicated path on Dedicated folder
    folder = os.path.dirname(path)
    if folder and not os.path.exists(folder):
        os.makedirs(folder, exist_ok=True)

    #انشاء قاعدة البيانات و ربطه بل متغير الخارجي
    #creat a DB var and link it with the public one
    conn = sql.connect(path, check_same_thread=False)
    #انشاء الكورسور حقها و ربطه بل متغير الخارجي
    #creat a cursor var and link it with the public one
    cur = conn.cursor()
    #اعطاء امر (sql) لأنشاء قاعدة البيانات و تعديل اعداداتها
    #give sql command to DB and set the setting
    cur.execute("""
    CREATE TABLE IF NOT EXISTS messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        text TEXT NOT NULL
    )
    """)

    #save the changes
    conn.commit() #حفظ التغيرات


#دالة الأضافة تضيف بيانات الى قاعدة البيانات
#function of add , it is add data to the DB
#data = {"neme" : "the name", "text" : "the msg"}
def add_user(data: Dict[str, Any]) -> Dict[str, Any]:
    global conn, cur #(لمنع مشاكل المتغيرات # to prevent problem
    #لتأكد من ان البرنامج متصل بقاعدة البيانات و اعطاء رسالة خطأ اذا كان غير متصل
    if not cur: # to make sure that the program get connect with DB and give an error msg if it did not connect
        return {"ok": False, "error": "DB not initialized"}

    # make it empty if the keys is wrong
    #يجعلها فاضية اذا كانت المفاتيح خطأ
    name = (data.get("name") or "").strip()
    text = (data.get("text") or "").strip()

    # Verify the parameter
    # لتحقق من المدخلات
    if not name or not text:
        return {"ok": False, "error": "name and text required"}

    #لتأكد من عدم تكرر الرسائل مع بعض
    #to check that no duplicate msg
    cur.execute("SELECT 1 FROM messages WHERE text = ?", (text,))
    if cur.fetchone():
        return {"ok": False, "error": "duplicate"}

    #لأضافة البيانات الى قاعدة البيانات
    #to insert a msg
    cur.execute("INSERT INTO messages (name, text) VALUES (?, ?)", (name, text))
    conn.commit()
    return {"ok": True}

def pop_messages(limit: int = 200) -> List[Dict[str, Any]]:
    global conn, cur #(لمنع مشاكل المتغيرات # to prevent problem
    # لتأكد من ان البرنامج متصل بقاعدة البيانات و اعطاء رسالة خطأ اذا كان غير متصل
    if cur is None: # to make sure that the program get connect with DB and give an error msg if it did not connect
        return []

    #سحب البيانات من قاعدة البيانات و التأكد من حذفها عند سحبها
    #to select data from th DB and make sure that it will del when we select it
    cur.execute("BEGIN")# عشان نضمن انو العمليتين حقت الحذف و السحب حتم مع بعض
    cur.execute("SELECT id, name, text FROM messages ORDER BY id ASC LIMIT ?", (limit,))
    rows = cur.fetchall()
    ids = [r[0] for r in rows]
    if ids:
        #حذف البيانات من قاعدة البيانات
        #del the data from the DB
        q = ",".join("?" for _ in ids)
        cur.execute(f"DELETE FROM messages WHERE id IN ({q})", ids)

    conn.commit()

    return [{"id": r[0], "name": r[1], "text": r[2]} for r in rows]