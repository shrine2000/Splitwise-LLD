from collections import defaultdict
from enums import SplitType


class User:
    def __init__(self, user_id: str, name: str, email: str):
        self._user_id = user_id
        self._name = name
        self._email = email

    def __str__(self):
        return f"{self._user_id}  {self._name}"


class Expense:
    def __init__(
        self, amount: float, payer: User, split_type: SplitType, shares: list = None
    ):
        self._amount: float = amount
        self._payer: User = payer
        self._split_type: SplitType = split_type
        self._shares: list = shares if shares else []

    def calculate_shares(self, users: list) -> dict:
        user_ids = [user._user_id for user in users]
        match self._split_type:
            case SplitType.EQUAL:
                _split_amount = round(self._amount / len(user_ids), 2)
                return {user_id: _split_amount for user_id in user_ids}
            case SplitType.EXACT:
                total_exact = sum(self._shares)
                if round(total_exact, 2) != round(self._amount, 2):
                    raise ValueError("Sum of shares and total amount is not equal")
                return {
                    user_id: round(share, 2)
                    for user_id, share in zip(user_ids, self._shares)
                }
            case SplitType.PERCENT:
                total_percent = sum(self._shares)
                if round(total_percent, 2) != 100:
                    raise ValueError("Percent shares must sum up to 100.")
                return {
                    user_id: round(self._amount * (percent / 100), 2)
                    for user_id, percent in zip(user_ids, self._shares)
                }


class ExpenseTracker:
    def __init__(self):
        self._users = {}
        self._balances = defaultdict(lambda: defaultdict(float))

    def add_user(self, user: User):
        self._users[user._user_id] = user

    def get_user(self, user_id: str) -> User:
        return self._users.get(user_id)

    def add_expense(
        self,
        payer_id: str,
        amount: float,
        user_ids: list,
        split_type: SplitType,
        shares: list = None,
    ):
        payer = self.get_user(payer_id)
        if not payer:
            raise ValueError("Payer not found.")

        users = [self.get_user(user_id) for user_id in user_ids]
        if not all(users):
            raise ValueError("One or more users not found.")

        expense = Expense(amount, payer, split_type, shares)
        shares_dict = expense.calculate_shares(users)

        for user in users:
            if user._user_id != payer_id:
                self._balances[user._user_id][payer_id] += shares_dict[user._user_id]
                self._balances[payer_id][user._user_id] -= shares_dict[user._user_id]

    def show_balances(self, user_id: str = None) -> list:
        results = []
        if user_id:
            user = self.get_user(user_id)
            if not user:
                raise ValueError("User not found.")
            balances = self._balances[user_id]
            if not balances:
                results.append("No balances")
            else:
                for owee in sorted(balances.keys()):
                    amount = balances[owee]
                    if amount > 0:
                        results.append(f"{user_id} owes {owee}: {round(amount, 2)}")
                    elif amount < 0:
                        results.append(f"{owee} owes {user_id}: {round(-amount, 2)}")
        else:
            all_balances = defaultdict(lambda: defaultdict(float))
            for user_id, owed_dict in self._balances.items():
                for owee, amount in owed_dict.items():
                    all_balances[owee][user_id] += amount

            for user_id in sorted(all_balances.keys()):
                for owee in sorted(all_balances[user_id].keys()):
                    amount = all_balances[user_id][owee]
                    if amount > 0:
                        results.append(f"{user_id} owes {owee}: {round(amount, 2)}")
                    elif amount < 0:
                        results.append(f"{owee} owes {user_id}: {round(-amount, 2)}")

        return results
