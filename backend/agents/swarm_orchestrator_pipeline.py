# Sub-File 87-F: Manages the sequential and parallel execution of AI Agents.
# Ensures the 'Assembly Line' never stops or breaks.

class SwarmOrchestratorPipeline:
    def execute_factory_line(self, project_intent):
        """Task ko step-by-step saare agents se pass karwata hai."""
        print(f"🏭 [Factory Manager]: Starting Assembly Line for -> '{project_intent}'")
        
        # Step 1: Planning
        blueprint = ArchitectAgent().create_master_blueprint(project_intent)
        
        # Step 2: Parallel Execution (Designing & Coding simultaneously)
        ui_json = UIDesignerAgent().design_interface(blueprint["UI_Designer"])
        api_code = BackendCoderAgent().generate_api_logic(blueprint["Backend_Coder"])
        
        # Step 3: Integration & Testing
        test_result = QATesterAgent().audit_code_in_sandbox(api_code)
        
        if test_result == "Passed":
            return self._forward_to_launch(ui_json, api_code)
        else:
            return self._trigger_rework_loop(api_code)
          
