from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# Replace 'llama-3-model' with the actual model name if different
model_name = "meta-llama/Meta-Llama-3-8B"  # Example placeholder name, update with actual name
access_token = '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'  # Your Hugging Face access token

# Load the tokenizer and model
tokenizer = AutoTokenizer.from_pretrained(model_name, use_auth_token=access_token)
model = AutoModelForCausalLM.from_pretrained(model_name, use_auth_token=access_token)

# Check if CUDA is available and move the model to GPU if possible
device = "cuda" if torch.cuda.is_available() else "cpu"
model.to(device)

def generate_response(prompt):
    inputs = tokenizer(prompt, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model.generate(inputs.input_ids, max_new_tokens=150)
    response = tokenizer.decode(outputs[0], skip_special_tokens=True)
    return response

def chat():
    print("Chatbot: Hello! How can I help you today?")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break
        response = generate_response(user_input)
        print(f"Chatbot: {response}")

if __name__ == "__main__":
    chat()
