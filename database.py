import sqlite3
import json
import hashlib

DB = "narrativeflow.db"

try:
    import bcrypt
    _BCRYPT = True
except ImportError:
    _BCRYPT = False


def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        email TEXT,
        password_hash TEXT NOT NULL
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS stories (
        story_key TEXT NOT NULL, username TEXT NOT NULL,
        title TEXT, genre TEXT, tone TEXT, messages TEXT,
        plot_arc TEXT DEFAULT '{}',
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        PRIMARY KEY (story_key, username)
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS characters (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_key TEXT NOT NULL, username TEXT NOT NULL,
        name TEXT NOT NULL, role TEXT, description TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    c.execute("""CREATE TABLE IF NOT EXISTS scenes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        story_key TEXT NOT NULL, username TEXT NOT NULL,
        scene_order INTEGER DEFAULT 0,
        title TEXT, location TEXT, purpose TEXT,
        characters_in_scene TEXT DEFAULT '[]',
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )""")
    # Migrations — safe to run on existing databases
    migrations = [
        "ALTER TABLE stories ADD COLUMN plot_arc TEXT DEFAULT '{}'",
        "ALTER TABLE stories ADD COLUMN writing_style TEXT DEFAULT ''",
        "ALTER TABLE stories ADD COLUMN word_goal INTEGER DEFAULT 0",
        "ALTER TABLE characters ADD COLUMN speaking_style TEXT DEFAULT ''",
    ]
    for sql in migrations:
        try: c.execute(sql)
        except sqlite3.OperationalError: pass
    conn.commit()
    conn.close()


# ── Password hashing ──────────────────────────────────────────────────────────
def _make_hash(pw):
    if _BCRYPT:
        return bcrypt.hashpw(pw.encode(), bcrypt.gensalt(12)).decode()
    return hashlib.sha256(pw.encode()).hexdigest()

def _check_hash(pw, stored):
    if stored.startswith("$2b$") or stored.startswith("$2a$"):
        return _BCRYPT and bcrypt.checkpw(pw.encode(), stored.encode())
    return stored == hashlib.sha256(pw.encode()).hexdigest()

def _upgrade_hash(username, pw, stored):
    if _BCRYPT and not (stored.startswith("$2b$") or stored.startswith("$2a$")):
        try:
            conn = sqlite3.connect(DB)
            conn.cursor().execute("UPDATE users SET password_hash=? WHERE username=?",
                                  (bcrypt.hashpw(pw.encode(), bcrypt.gensalt(12)).decode(), username.strip()))
            conn.commit(); conn.close()
        except: pass


# ── Users ─────────────────────────────────────────────────────────────────────
def register_user(username, email, password):
    try:
        conn = sqlite3.connect(DB)
        conn.cursor().execute(
            "INSERT INTO users (username,email,password_hash) VALUES (?,?,?)",
            (username.strip(), email.strip(), _make_hash(password)))
        conn.commit(); conn.close()
        return {"ok": True}
    except sqlite3.IntegrityError:
        return {"ok": False, "error": "Username already taken"}
    except Exception as e:
        return {"ok": False, "error": str(e)}

def verify_login(username, password):
    conn = sqlite3.connect(DB)
    row = conn.cursor().execute(
        "SELECT password_hash FROM users WHERE username=?", (username.strip(),)).fetchone()
    conn.close()
    if not row: return False
    if _check_hash(password, row[0]):
        _upgrade_hash(username, password, row[0])
        return True
    return False


# ── Stories ───────────────────────────────────────────────────────────────────
def save_story(username, story):
    conn = sqlite3.connect(DB)
    conn.cursor().execute("""
        INSERT INTO stories (story_key,username,title,genre,tone,messages,plot_arc,writing_style,word_goal,updated_at)
        VALUES (?,?,?,?,?,?,?,?,?,CURRENT_TIMESTAMP)
        ON CONFLICT(story_key,username) DO UPDATE SET
            title=excluded.title, genre=excluded.genre, tone=excluded.tone,
            messages=excluded.messages, plot_arc=excluded.plot_arc,
            writing_style=excluded.writing_style, word_goal=excluded.word_goal,
            updated_at=CURRENT_TIMESTAMP
    """, (story["id"], username,
          story.get("title","Untitled"), story.get("genre","Fantasy"),
          story.get("tone","Light"),
          json.dumps(story.get("messages",[])),
          json.dumps(story.get("plot_arc",{})),
          story.get("writing_style",""),
          story.get("word_goal",0)))
    conn.commit(); conn.close()

def load_stories(username):
    conn = sqlite3.connect(DB)
    rows = conn.cursor().execute(
        "SELECT story_key,title,genre,tone,messages,plot_arc,writing_style,word_goal FROM stories WHERE username=? ORDER BY updated_at DESC",
        (username,)).fetchall()
    conn.close()
    result = []
    for r in rows:
        try: arc = json.loads(r[5]) if r[5] else {}
        except: arc = {}
        result.append({"id":r[0],"title":r[1],"genre":r[2],"tone":r[3],
                        "messages":json.loads(r[4]),"plot_arc":arc,
                        "writing_style":r[6] or "","word_goal":r[7] or 0})
    return result

def delete_story(username, story_id):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("DELETE FROM stories WHERE story_key=? AND username=?", (story_id, username))
    c.execute("DELETE FROM characters WHERE story_key=? AND username=?", (story_id, username))
    c.execute("DELETE FROM scenes WHERE story_key=? AND username=?", (story_id, username))
    conn.commit(); conn.close()

def update_story_title(username, story_id, new_title):
    conn = sqlite3.connect(DB)
    conn.cursor().execute(
        "UPDATE stories SET title=?,updated_at=CURRENT_TIMESTAMP WHERE story_key=? AND username=?",
        (new_title.strip(), story_id, username))
    conn.commit(); conn.close()


# ── Characters ────────────────────────────────────────────────────────────────
def add_character(username, story_id, name, role, description, speaking_style=""):
    conn = sqlite3.connect(DB)
    conn.cursor().execute(
        "INSERT INTO characters (story_key,username,name,role,description,speaking_style) VALUES (?,?,?,?,?,?)",
        (story_id, username, name.strip(), role.strip(), description.strip(), speaking_style.strip()))
    conn.commit(); conn.close()

def load_characters(username, story_id):
    conn = sqlite3.connect(DB)
    rows = conn.cursor().execute(
        "SELECT id,name,role,description,speaking_style FROM characters WHERE story_key=? AND username=? ORDER BY created_at",
        (story_id, username)).fetchall()
    conn.close()
    return [{"id":r[0],"name":r[1],"role":r[2],"description":r[3],"speaking_style":r[4] or ""} for r in rows]

def delete_character(char_id):
    conn = sqlite3.connect(DB)
    conn.cursor().execute("DELETE FROM characters WHERE id=?", (char_id,))
    conn.commit(); conn.close()


# ── Scenes ────────────────────────────────────────────────────────────────────
def add_scene(username, story_id, title, location, purpose, characters_in):
    conn = sqlite3.connect(DB)
    order = (conn.cursor().execute(
        "SELECT COUNT(*) FROM scenes WHERE story_key=? AND username=?",
        (story_id, username)).fetchone()[0] or 0) + 1
    conn.cursor().execute(
        "INSERT INTO scenes (story_key,username,scene_order,title,location,purpose,characters_in_scene) VALUES (?,?,?,?,?,?,?)",
        (story_id, username, order, title.strip(), location.strip(), purpose.strip(), json.dumps(characters_in)))
    conn.commit(); conn.close()

def load_scenes(username, story_id):
    conn = sqlite3.connect(DB)
    rows = conn.cursor().execute(
        "SELECT id,scene_order,title,location,purpose,characters_in_scene FROM scenes WHERE story_key=? AND username=? ORDER BY scene_order",
        (story_id, username)).fetchall()
    conn.close()
    return [{"id":r[0],"order":r[1],"title":r[2],"location":r[3],
             "purpose":r[4],"characters":json.loads(r[5] or "[]")} for r in rows]

def delete_scene(scene_id):
    conn = sqlite3.connect(DB)
    conn.cursor().execute("DELETE FROM scenes WHERE id=?", (scene_id,))
    conn.commit(); conn.close()


# ── Edit character ─────────────────────────────────────────────────────────────
def update_character(char_id, name, role, description, speaking_style):
    conn = sqlite3.connect(DB)
    conn.cursor().execute(
        "UPDATE characters SET name=?,role=?,description=?,speaking_style=? WHERE id=?",
        (name.strip(), role.strip(), description.strip(), speaking_style.strip(), char_id))
    conn.commit(); conn.close()


# ── Edit scene ────────────────────────────────────────────────────────────────
def update_scene(scene_id, title, location, purpose, characters_in):
    conn = sqlite3.connect(DB)
    conn.cursor().execute(
        "UPDATE scenes SET title=?,location=?,purpose=?,characters_in_scene=? WHERE id=?",
        (title.strip(), location.strip(), purpose.strip(),
         json.dumps(characters_in), scene_id))
    conn.commit(); conn.close()
