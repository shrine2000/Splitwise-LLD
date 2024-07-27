from models import User, ExpenseTracker
from enums import SplitType


def main():
    # Initialize the expense tracker
    tracker = ExpenseTracker()

    # Add users
    alice = User("u1", "Alice", "alice@example.com")
    bob = User("u2", "Bob", "bob@example.com")
    charlie = User("u3", "Charlie", "charlie@example.com")
    daisy = User("u4", "Daisy", "daisy@example.com")

    tracker.add_user(alice)
    tracker.add_user(bob)
    tracker.add_user(charlie)
    tracker.add_user(daisy)

    # Add expenses
    print("Adding expenses...")
    tracker.add_expense("u1", 1000, ["u1", "u2", "u3", "u4"], SplitType.EQUAL)
    print("Balances after equal split:")
    print_balances(tracker)

    tracker.add_expense("u1", 1250, ["u2", "u3"], SplitType.EXACT, [370, 880])
    print("Balances after exact split:")
    print_balances(tracker)

    tracker.add_expense(
        "u4", 1200, ["u1", "u2", "u3", "u4"], SplitType.PERCENT, [40, 20, 20, 20]
    )
    print("Balances after percent split:")
    print_balances(tracker)


def print_balances(tracker):
    # Print balances for all users
    for user_id in tracker._users.keys():
        print(f"\nBalances for user {user_id}:")
        balances = tracker.show_balances(user_id)
        if not balances:
            print("No balances")
        else:
            for balance in balances:
                print(balance)


if __name__ == "__main__":
    main()
