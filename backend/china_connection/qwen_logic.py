# File: backend/china_connection/qwen_logic.py
# Purpose: Uses Qwen 2.5 (Alibaba) for advanced reasoning and logic.
# The "Brain" behind the "Code".

from transformers import AutoModelForCausalLM, AutoTokenizer

class QwenLogicEngine:
    def __init__(self):
        # Qwen 2.5 - 7B is the sweet spot for Colab
        self.model_id = "Qwen/Qwen2.5-7B-Instruct" 
        self.tokenizer = AutoTokenizer.from_pretrained(self.model_id)
        self.model = AutoModelForCausalLM.from_pretrained(
            self.model_id, 
            device_map="auto", 
            torch_dtype="auto"
        )

    def solve_logic(self, problem_statement):
        """
        Step-by-step reasoning (Chain of Thought) generate karta hai.
        """
        print(f"🐲 [Qwen]: Reasoning on: {problem_statement}...")
        
        messages = [
            {"role": "system", "content": "You are a logical reasoning expert."},
            {"role": "user", "content": problem_statement}
        ]
        
        text = self.tokenizer.apply_chat_template(
            messages, tokenize=False, add_generation_prompt=True
        )
        model_inputs = self.tokenizer([text], return_tensors="pt").to(self.model.device)

        generated_ids = self.model.generate(
            **model_inputs,
            max_new_tokens=512
        )
        
        response = self.tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
        return response
      
