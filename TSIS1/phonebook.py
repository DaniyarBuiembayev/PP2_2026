"""
PhoneBook – TSIS 1
Extended contact management: groups, multiple phones, email, birthday,
JSON import/export, extended CSV import, paginated navigation,
filter by group, search by email, sort options.
"""

import csv
import json
from datetime import date, datetime
from connect import get_connection


# ── helpers ──────────────────────────────────────────────────────────────────

def _fmt_row(row):
    """Pretty-print a paginated contact row (tuple from get_contacts_paginated)."""
    cid, username, email, birthday, group_name, phones_agg, created_at = row
    return (
        f"[{cid}] {username}"
        f" | email: {email or '—'}"
        f" | birthday: {birthday or '—'}"
        f" | group: {group_name or '—'}"
        f" | phones: {phones_agg or '—'}"
    )


def _input_date(prompt):
    """Ask for a date in YYYY-MM-DD format; allow empty."""
    while True:
        raw = input(prompt + " (YYYY-MM-DD or blank): ").strip()
        if not raw:
            return None
        try:
            datetime.strptime(raw, "%Y-%m-%d")
            return raw
        except ValueError:
            print("  Invalid date format. Try again.")


def _pick_group(cur):
    """Show group list and return chosen group_id (or None)."""
    cur.execute("SELECT id, name FROM groups ORDER BY id")
    groups = cur.fetchall()
    print("  Groups:")
    for gid, gname in groups:
        print(f"    {gid}. {gname}")
    raw = input("  Choose group number (or blank to skip): ").strip()
    if not raw:
        return None
    for gid, _ in groups:
        if str(gid) == raw:
            return gid
    print("  Unknown group – skipped.")
    return None


# ── 3.1  insert from console (extended) ──────────────────────────────────────

def insert_from_console():
    username = input("Name: ").strip()
    email    = input("Email (blank to skip): ").strip() or None
    birthday = _input_date("Birthday")

    conn = get_connection()
    cur  = conn.cursor()
    group_id = _pick_group(cur)

    cur.execute(
        "INSERT INTO contacts (username, email, birthday, group_id) "
        "VALUES (%s, %s, %s, %s) ON CONFLICT (username) DO NOTHING RETURNING id",
        (username, email, birthday, group_id)
    )
    row = cur.fetchone()
    if row is None:
        print(f"  Contact '{username}' already exists – skipped.")
        cur.close(); conn.close()
        return

    contact_id = row[0]

    while True:
        phone = input("Phone number (blank to stop): ").strip()
        if not phone:
            break
        ptype = input("  Type (home/work/mobile) [mobile]: ").strip() or "mobile"
        if ptype not in ("home", "work", "mobile"):
            ptype = "mobile"
        cur.execute(
            "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
            (contact_id, phone, ptype)
        )

    conn.commit()
    cur.close(); conn.close()
    print(f"  ✓ Contact '{username}' saved.")


# ── 3.3  CSV import (extended) ───────────────────────────────────────────────
#
#  Expected CSV columns (header row):
#  username, email, birthday, group, phone, phone_type
#
#  Multiple phones for the same contact = multiple rows.

def insert_from_csv(filename="contacts.csv"):
    conn = get_connection()
    cur  = conn.cursor()

    inserted = skipped = 0

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            username   = row.get("username", "").strip()
            email      = row.get("email", "").strip()    or None
            birthday   = row.get("birthday", "").strip() or None
            group_name = row.get("group", "").strip()    or None
            phone      = row.get("phone", "").strip()    or None
            phone_type = row.get("phone_type", "mobile").strip() or "mobile"

            if not username:
                continue

            # Resolve group
            group_id = None
            if group_name:
                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                g = cur.fetchone()
                if g:
                    group_id = g[0]

            # Upsert contact
            cur.execute(
                "INSERT INTO contacts (username, email, birthday, group_id) "
                "VALUES (%s, %s, %s, %s) "
                "ON CONFLICT (username) DO UPDATE "
                "SET email=EXCLUDED.email, birthday=EXCLUDED.birthday, group_id=EXCLUDED.group_id "
                "RETURNING id",
                (username, email, birthday, group_id)
            )
            contact_id = cur.fetchone()[0]

            # Add phone if present
            if phone:
                cur.execute(
                    "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s) "
                    "ON CONFLICT DO NOTHING",
                    (contact_id, phone, phone_type)
                )

            inserted += 1

    conn.commit()
    cur.close(); conn.close()
    print(f"  ✓ CSV import done. Rows processed: {inserted}, skipped: {skipped}.")


# ── 3.3  JSON export ─────────────────────────────────────────────────────────

def export_to_json(filename="contacts_export.json"):
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email,
               c.birthday::text, g.name AS group_name,
               c.created_at::text
        FROM contacts c
        LEFT JOIN groups g ON g.id = c.group_id
        ORDER BY c.username
    """)
    contacts = cur.fetchall()

    result = []
    for cid, username, email, birthday, group_name, created_at in contacts:
        cur.execute(
            "SELECT phone, type FROM phones WHERE contact_id = %s", (cid,)
        )
        phones = [{"phone": p, "type": t} for p, t in cur.fetchall()]
        result.append({
            "username":   username,
            "email":      email,
            "birthday":   birthday,
            "group":      group_name,
            "phones":     phones,
            "created_at": created_at,
        })

    cur.close(); conn.close()

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"  ✓ Exported {len(result)} contacts to '{filename}'.")


# ── 3.3  JSON import ─────────────────────────────────────────────────────────

def import_from_json(filename="contacts_export.json"):
    with open(filename, encoding="utf-8") as f:
        records = json.load(f)

    conn = get_connection()
    cur  = conn.cursor()

    for rec in records:
        username   = rec.get("username", "").strip()
        email      = rec.get("email")
        birthday   = rec.get("birthday")
        group_name = rec.get("group")
        phones     = rec.get("phones", [])

        if not username:
            continue

        # Check duplicate
        cur.execute("SELECT id FROM contacts WHERE username = %s", (username,))
        existing = cur.fetchone()

        if existing:
            choice = input(f"  '{username}' already exists. (s)kip / (o)verwrite? ").strip().lower()
            if choice != "o":
                print(f"    Skipped '{username}'.")
                continue
            contact_id = existing[0]
            cur.execute(
                "UPDATE contacts SET email=%s, birthday=%s WHERE id=%s",
                (email, birthday, contact_id)
            )
            cur.execute("DELETE FROM phones WHERE contact_id=%s", (contact_id,))
        else:
            # Resolve / create group
            group_id = None
            if group_name:
                cur.execute(
                    "INSERT INTO groups (name) VALUES (%s) ON CONFLICT (name) DO NOTHING",
                    (group_name,)
                )
                cur.execute("SELECT id FROM groups WHERE name = %s", (group_name,))
                group_id = cur.fetchone()[0]

            cur.execute(
                "INSERT INTO contacts (username, email, birthday, group_id) "
                "VALUES (%s, %s, %s, %s) RETURNING id",
                (username, email, birthday, group_id)
            )
            contact_id = cur.fetchone()[0]

        for p in phones:
            cur.execute(
                "INSERT INTO phones (contact_id, phone, type) VALUES (%s, %s, %s)",
                (contact_id, p.get("phone"), p.get("type", "mobile"))
            )

    conn.commit()
    cur.close(); conn.close()
    print("  ✓ JSON import done.")


# ── 3.2  Filter by group ─────────────────────────────────────────────────────

def filter_by_group():
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("SELECT id, name FROM groups ORDER BY name")
    groups = cur.fetchall()
    print("  Groups:")
    for gid, gname in groups:
        print(f"    {gid}. {gname}")
    raw = input("  Enter group number: ").strip()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name,
               STRING_AGG(ph.phone || ' (' || ph.type || ')', ', ') AS phones
        FROM contacts c
        LEFT JOIN groups g  ON g.id  = c.group_id
        LEFT JOIN phones ph ON ph.contact_id = c.id
        WHERE g.id = %s
        GROUP BY c.id, c.username, c.email, c.birthday, g.name
        ORDER BY c.username
    """, (raw,))

    rows = cur.fetchall()
    if not rows:
        print("  No contacts in this group.")
    for r in rows:
        cid, username, email, birthday, group_name, phones = r
        print(f"  [{cid}] {username} | email: {email or '—'} | bday: {birthday or '—'} | phones: {phones or '—'}")

    cur.close(); conn.close()


# ── 3.2  Search by email ─────────────────────────────────────────────────────

def search_by_email():
    keyword = input("  Email keyword: ").strip()
    conn = get_connection()
    cur  = conn.cursor()

    cur.execute("""
        SELECT c.id, c.username, c.email, c.birthday, g.name,
               STRING_AGG(ph.phone || ' (' || ph.type || ')', ', ')
        FROM contacts c
        LEFT JOIN groups g  ON g.id  = c.group_id
        LEFT JOIN phones ph ON ph.contact_id = c.id
        WHERE c.email ILIKE %s
        GROUP BY c.id, c.username, c.email, c.birthday, g.name
        ORDER BY c.username
    """, (f"%{keyword}%",))

    rows = cur.fetchall()
    if not rows:
        print("  No contacts found.")
    for r in rows:
        cid, username, email, birthday, group_name, phones = r
        print(f"  [{cid}] {username} | email: {email} | bday: {birthday or '—'} | group: {group_name or '—'} | phones: {phones or '—'}")

    cur.close(); conn.close()


# ── 3.2  Sort contacts ───────────────────────────────────────────────────────

def sorted_list():
    print("  Sort by: (1) Name  (2) Birthday  (3) Date added")
    order = input("  Choice: ").strip()
    order_col = {
        "1": "c.username",
        "2": "c.birthday",
        "3": "c.created_at",
    }.get(order, "c.username")

    conn = get_connection()
    cur  = conn.cursor()
    cur.execute(f"""
        SELECT c.id, c.username, c.email, c.birthday, g.name,
               STRING_AGG(ph.phone || ' (' || ph.type || ')', ', '),
               c.created_at
        FROM contacts c
        LEFT JOIN groups g  ON g.id  = c.group_id
        LEFT JOIN phones ph ON ph.contact_id = c.id
        GROUP BY c.id, c.username, c.email, c.birthday, g.name, c.created_at
        ORDER BY {order_col} NULLS LAST
    """)
    rows = cur.fetchall()
    if not rows:
        print("  No contacts.")
    for r in rows:
        cid, username, email, birthday, group_name, phones, created_at = r
        print(f"  [{cid}] {username} | bday: {birthday or '—'} | group: {group_name or '—'} | phones: {phones or '—'}")
    cur.close(); conn.close()


# ── 3.2  Paginated navigation ────────────────────────────────────────────────

def paginated_view():
    page_size = 5
    page      = 0

    conn = get_connection()
    cur  = conn.cursor()

    while True:
        offset = page * page_size
        cur.execute(
            "SELECT * FROM get_contacts_paginated(%s, %s)",
            (page_size, offset)
        )
        rows = cur.fetchall()

        if not rows:
            print("  No contacts on this page.")
        else:
            print(f"\n  ── Page {page + 1} ──────────────────────────────")
            for r in rows:
                print(" ", _fmt_row(r))

        cmd = input("\n  [n]ext / [p]rev / [q]uit: ").strip().lower()
        if cmd == "n":
            if len(rows) < page_size:
                print("  Already at the last page.")
            else:
                page += 1
        elif cmd == "p":
            if page == 0:
                print("  Already at the first page.")
            else:
                page -= 1
        elif cmd == "q":
            break

    cur.close(); conn.close()


# ── 3.4  Call stored procedures from console ─────────────────────────────────

def call_add_phone():
    name  = input("  Contact name: ").strip()
    phone = input("  Phone number: ").strip()
    ptype = input("  Type (home/work/mobile) [mobile]: ").strip() or "mobile"

    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("CALL add_phone(%s, %s, %s)", (name, phone, ptype))
        conn.commit()
        print("  ✓ Phone added.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗ Error: {e}")
    finally:
        cur.close(); conn.close()


def call_move_to_group():
    name  = input("  Contact name: ").strip()
    group = input("  Group name: ").strip()

    conn = get_connection()
    cur  = conn.cursor()
    try:
        cur.execute("CALL move_to_group(%s, %s)", (name, group))
        conn.commit()
        print(f"  ✓ '{name}' moved to group '{group}'.")
    except Exception as e:
        conn.rollback()
        print(f"  ✗ Error: {e}")
    finally:
        cur.close(); conn.close()


def call_search_contacts():
    query = input("  Search query: ").strip()
    conn  = get_connection()
    cur   = conn.cursor()
    cur.execute("SELECT * FROM search_contacts(%s)", (query,))
    rows = cur.fetchall()
    if not rows:
        print("  No results.")
    for r in rows:
        cid, username, email, birthday, group_name, phone, phone_type, created_at = r
        print(f"  [{cid}] {username} | email: {email or '—'} | group: {group_name or '—'}"
              f" | phone: {phone or '—'} ({phone_type or '—'})")
    cur.close(); conn.close()


# ── menu ──────────────────────────────────────────────────────────────────────

def menu():
    options = {
        "1":  ("Insert contact (console)",           insert_from_console),
        "2":  ("Import from CSV",                    lambda: insert_from_csv("contacts.csv")),
        "3":  ("Export to JSON",                     lambda: export_to_json("contacts_export.json")),
        "4":  ("Import from JSON",                   lambda: import_from_json("contacts_export.json")),
        "5":  ("Filter by group",                    filter_by_group),
        "6":  ("Search by email",                    search_by_email),
        "7":  ("Sorted list (name / birthday / date)", sorted_list),
        "8":  ("Paginated view",                     paginated_view),
        "9":  ("Add phone to contact (procedure)",   call_add_phone),
        "10": ("Move contact to group (procedure)",  call_move_to_group),
        "11": ("Full-text search (DB function)",     call_search_contacts),
        "0":  ("Exit",                               None),
    }

    while True:
        print("\n══════════  PhoneBook TSIS 1  ══════════")
        for key, (label, _) in options.items():
            print(f"  {key:>2}. {label}")
        print("════════════════════════════════════════")
        choice = input("Choose: ").strip()

        if choice == "0":
            print("Bye!")
            break
        elif choice in options:
            _, fn = options[choice]
            fn()
        else:
            print("  Unknown option.")


if __name__ == "__main__":
    menu()
