# File Path: backend/demographic_logic.py
# Sub-File D: Age-specific reasoning paths and logic routing.

class DemographicLogic:
    def route_logic(self, age_group):
        if age_group == "child":
            return "Logic: Gamified, Simple, Visual-first."
        elif age_group == "senior":
            return "Logic: High-clarity, Slow-paced, Assistance-focused."
        else:
            return "Logic: High-speed, Professional, Minimalist."
          
