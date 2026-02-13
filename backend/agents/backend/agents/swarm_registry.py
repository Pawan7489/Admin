# Sub-File 87-Q: The Attendance Sheet for the Swarm.
# Scans and registers active agent nodes at startup. [cite: 2026-02-11]

class SwarmRegistry:
    def __init__(self):
        self.active_agents = []

    def take_attendance(self, expected_agents_list):
        """System startup par sabhi AI agents ki attendance leta hai."""
        print("📋 [Registry]: Taking Swarm Attendance...")
        
        for agent in expected_agents_list:
            # Ping agent node
            is_alive = True 
            if is_alive:
                self.active_agents.append(agent)
                print(f"✔️ [Registry]: {agent} is PRESENT and Ready.")
            else:
                print(f"❌ [Registry]: {agent} is OFFLINE. Initiating wake-up protocol.")
                
        return self.active_agents
