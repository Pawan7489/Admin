# Sub-File 86-F: Pools multiple free-tier Kaggle/Colab accounts.
# Automatically rotates API keys when free quotas are exhausted.

class ComputeAggregator:
    def __init__(self, key_vault):
        # Vault contains lists of free API keys for different accounts
        self.colab_accounts = key_vault.get('colab_keys', [])
        self.current_key_index = 0

    def get_active_compute_node(self):
        """Current active account ka GPU check karta hai."""
        active_key = self.colab_accounts[self.current_key_index]
        return active_key

    def switch_account_on_limit(self):
        """Agar limit khatam ho jaye, toh next free account par switch karta hai."""
        self.current_key_index = (self.current_key_index + 1) % len(self.colab_accounts)
        new_key = self.colab_accounts[self.current_key_index]
        print(f"🔄 [Compute Pool]: Quota exceeded. Switching to Backup Account ID: {self.current_key_index}...")
        return new_key
      
