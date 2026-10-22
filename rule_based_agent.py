class ATMAgent:
    """
    A simple rule-based agent that acts as an ATM Menu System.
    It uses state tracking to handle multi-step interactions like deposits and withdrawals.
    """
    def __init__(self):
        self.name = "ATM-Bot"
        self.balance = 1000.0  # Starting balance
        self.state = "MAIN_MENU"

    def get_response(self, user_input: str) -> str:
        """
        Process user input based on the current state.
        """
        user_input = user_input.lower().strip()

        if self.state == "MAIN_MENU":
            return self.handle_main_menu(user_input)
        elif self.state == "DEPOSIT":
            return self.handle_deposit(user_input)
        elif self.state == "WITHDRAW":
            return self.handle_withdraw(user_input)
        else:
            self.state = "MAIN_MENU"
            return "An error occurred. Returning to main menu.\n" + self.show_menu()

    def handle_main_menu(self, user_input: str) -> str:
        if user_input in ['1', 'balance', 'check balance']:
            return f"Your current balance is: Rs. {self.balance:.2f}\n" + self.show_menu()
            
        elif user_input in ['2', 'deposit']:
            self.state = "DEPOSIT"
            return "Please enter the amount you wish to deposit (or type 'cancel' to return):"
                
        elif user_input in ['3', 'withdraw']:
            self.state = "WITHDRAW"
            return "Please enter the amount you wish to withdraw (or type 'cancel' to return):"
                
        elif user_input in ['4', 'exit', 'quit', 'bye']:
            return "Goodbye! Thank you for using our ATM."
            
        elif user_input in ['help', 'menu', 'options']:
            return self.show_menu()
            
        else:
            return "Invalid option.\n" + self.show_menu()

    def handle_deposit(self, user_input: str) -> str:
        if user_input in ['cancel', 'back', 'menu']:
            self.state = "MAIN_MENU"
            return "Deposit cancelled.\n" + self.show_menu()
            
        try:
            # Also allow replacing 'rs.' just in case the user types it
            user_input_clean = user_input.replace('$', '').replace('rs.', '').replace('rs', '').strip()
            amount = float(user_input_clean)
            if amount > 0:
                self.balance += amount
                self.state = "MAIN_MENU"
                return f"Successfully deposited Rs. {amount:.2f}. New balance is: Rs. {self.balance:.2f}\n" + self.show_menu()
            else:
                return "Deposit amount must be positive. Please enter a valid amount or type 'cancel':"
        except ValueError:
            return "Invalid amount. Please use a number (e.g., 50) or type 'cancel':"

    def handle_withdraw(self, user_input: str) -> str:
        if user_input in ['cancel', 'back', 'menu']:
            self.state = "MAIN_MENU"
            return "Withdrawal cancelled.\n" + self.show_menu()
            
        try:
            user_input_clean = user_input.replace('$', '').replace('rs.', '').replace('rs', '').strip()
            amount = float(user_input_clean)
            if amount > 0:
                if amount <= self.balance:
                    self.balance -= amount
                    self.state = "MAIN_MENU"
                    return f"Successfully withdrew Rs. {amount:.2f}. New balance is: Rs. {self.balance:.2f}\n" + self.show_menu()
                else:
                    return f"Insufficient funds. Your balance is Rs. {self.balance:.2f}. Please enter a valid amount or type 'cancel':"
            else:
                return "Withdrawal amount must be positive. Please enter a valid amount or type 'cancel':"
        except ValueError:
            return "Invalid amount. Please use a number (e.g., 20) or type 'cancel':"

    def show_menu(self) -> str:
        return (
            "--- ATM Menu ---\n"
            "1. Check Balance\n"
            "2. Deposit\n"
            "3. Withdraw\n"
            "4. Exit"
        )

def main():
    agent = ATMAgent()
    print(f"[{agent.name}] is now online.")
    print(agent.show_menu())
    
    while True:
        try:
            user_input = input("\nYou: ").strip()
        except EOFError:
            print("\nExiting ATM.")
            break
            
        if not user_input:
            continue
            
        response = agent.get_response(user_input)
        print(f"{agent.name}:\n{response}")
        
        if user_input.lower() in ['4', 'exit', 'quit', 'bye'] and agent.state == "MAIN_MENU":
            break

if __name__ == "__main__":
    main()
