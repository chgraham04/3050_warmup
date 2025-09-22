"""
Organize logical navigation through CLI
call functions defined in cli_helper.py
"""
from admin import open_firestore_db
from query_fs import run_query, help_message, welcome_messsage

def print_results(rows):
    total = len(rows)
    if total == 0:
        print("No results.")
        return
    print(f"{total} result(s):")
    print(f' | {"Make & Model":<23} | {"Price ($)":<9} | {"Mileage (mi)":<12} | {"Trim":<11} | {"Type":<12} | {"VIN":<20} |')
    print("  " + "-" * 106)
    for r in rows:
        print("  " + r)
    print("  " + "-" * 106)

def execute_cli():
    db = open_firestore_db()
    print(welcome_messsage())

    while True:
        try:
            raw = input("> ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye.")
            break

        if not raw:
            continue

        upper = raw.upper()
        if upper == "HELP":
            print(help_message())
            continue
        if upper in ("QUIT", "EXIT"):
            print("Goodbye.")
            break

        # QUERY HANDLING
        try:
            rows = run_query(raw, db)
            print_results(rows)
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    execute_cli()
