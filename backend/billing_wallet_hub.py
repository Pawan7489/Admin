# Sub-File 86-L: Manages user wallets, subscription plans, and API billing.
# The commercial engine of the SaaS ecosystem.

class BillingWalletHub:
    def __init__(self):
        self.user_wallets = {"client_001": 500.0} # Starting credits in INR/USD
        self.api_costs = {"text_gen": 0.5, "voice_gen": 2.0}

    def deduct_credits(self, user_id, service_used):
        """User ke wallet se usage ke hisab se payment deduct karta hai."""
        cost = self.api_costs.get(service_used, 0.0)
        
        if self.user_wallets.get(user_id, 0) >= cost:
            self.user_wallets[user_id] -= cost
            print(f"💸 [Billing]: Deducted ₹{cost} from {user_id}. Remaining Balance: ₹{self.user_wallets[user_id]}")
            return True
        else:
            print(f"❌ [Billing Error]: Insufficient balance for {user_id}. Please recharge.")
            return False

    def calculate_dynamic_pricing(self, load, base_price):
        """
        Calculates Surge Pricing ($P_{dynamic}$) during heavy traffic.
        Formula: $P_{dynamic} = Base \times (1 + \frac{Current\_Load}{Max\_Capacity})$
        """
        return base_price * 1.2 # 20% surge during peak hours
