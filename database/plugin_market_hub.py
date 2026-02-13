# Sub-File 86-J: The internal App Store / Plugin Directory for the Admin Panel.

class PluginMarketHub:
    def __init__(self):
        self.installed_plugins = ["Llama3_Engine", "iOS_Theme_Pack"]

    def install_from_store(self, plugin_name):
        """Naye AI models ya UI features ko system mein add karta hai."""
        if plugin_name not in self.installed_plugins:
            self.installed_plugins.append(plugin_name)
            print(f"🛒 [Market]: '{plugin_name}' successfully installed to C-Panel.")
            return True
        return False
      
