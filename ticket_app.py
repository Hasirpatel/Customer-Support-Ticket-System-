import sqlite3
import csv
from datetime import datetime

conn = sqlite3.connect("tickets.db")
cursor = conn.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS tickets (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT,
        description TEXT,
        priority TEXT,
        status TEXT,
        created_at TEXT,
        updated_at TEXT
    )
""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS ticket_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ticket_id INTEGER,
        old_status TEXT,
        new_status TEXT,
        changed_at TEXT
    )
""")

conn.commit()

def create_ticket(title, description, priority):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("""
        INSERT INTO tickets (title, description, priority, status, created_at, updated_at)
        VALUES (?, ?, ?, 'Open', ?, ?)
    """, (title, description, priority, now, now))
    conn.commit()
    print(f"Ticket created successfully.")

def update_ticket_status(ticket_id, new_status):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute("SELECT status FROM tickets WHERE id = ?", (ticket_id,))
    row = cursor.fetchone()
    if row is None:
        print("Ticket not found.")
        return
    old_status = row[0]
    cursor.execute("""
        UPDATE tickets SET status = ?, updated_at = ? WHERE id = ?
    """, (new_status, now, ticket_id))
    cursor.execute("""
        INSERT INTO ticket_logs (ticket_id, old_status, new_status, changed_at)
        VALUES (?, ?, ?, ?)
    """, (ticket_id, old_status, new_status, now))
    conn.commit()
    print(f"Ticket {ticket_id} updated from '{old_status}' to '{new_status}'.")

def view_tickets():
    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()
    print("\nID | Title | Priority | Status | Created At")
    print("-" * 60)
    for row in rows:
        print(f"{row[0]} | {row[1]} | {row[3]} | {row[4]} | {row[5]}")

def export_to_csv():
    cursor.execute("SELECT * FROM tickets")
    rows = cursor.fetchall()
    with open("tickets_export.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["ID", "Title", "Description", "Priority", "Status", "Created At", "Updated At"])
        writer.writerows(rows)
    print("Exported to tickets_export.csv")

def main():
    while True:
        print("\n--- Helpdesk Ticket System ---")
        print("1. Create Ticket")
        print("2. Update Ticket Status")
        print("3. View All Tickets")
        print("4. Export to CSV")
        print("5. Exit")
        choice = input("Choose an option: ")
        if choice == "1":
            title = input("Title: ")
            desc = input("Description: ")
            priority = input("Priority (Low/Medium/High): ")
            create_ticket(title, desc, priority)
        elif choice == "2":
            tid = int(input("Ticket ID: "))
            status = input("New Status (Open/In Progress/Resolved): ")
            update_ticket_status(tid, status)
        elif choice == "3":
            view_tickets()
        elif choice == "4":
            export_to_csv()
        elif choice == "5":
            break

main()