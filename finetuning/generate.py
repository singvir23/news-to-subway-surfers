import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig

# --- CONFIG ---
MODEL_PATH = "meta-llama/Meta-Llama-3-8B-Instruct" # or whatever model we use
ADAPTER_PATH = "./llama_tiktok" # Your saved weights folder (our tuned model)
SYSTEM_PROMPT = (
    "You are a Gen Z digital analyst and content creator. Your primary task is to receive "
    "a formal news summary and translate its core message into a short, highly engaging "
    "TikTok script. Use Gen Z slang (e.g., 'no cap', 'it's giving', 'period'), relevant "
    "emojis, and a conversational, punchy tone. The output must be concise and self-contained."
)


# NEWS_SUMMARY = ( wherever the news summary is coming from, change
   
# )



MAX_NEW_TOKENS = 385 # apprx length for around a 2min video

# Configure 4-bit quantization (MUST MATCH TRAINING CONFIG)
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_quant_type="nf4", 
    bnb_4bit_compute_dtype=torch.bfloat16, 
    bnb_4bit_use_double_quant=False,
)

# 1. Load the Base Model and Tokenizer
print("Loading base model...")
base_model = AutoModelForCausalLM.from_pretrained(
    MODEL_PATH,
    quantization_config=bnb_config,
    device_map="auto",
    dtype=torch.bfloat16,
)
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token

# 2. Attach the Fine-Tuned Adapter Weights
print(f"Loading LORA adapter from {ADAPTER_PATH}...")
model = PeftModel.from_pretrained(base_model, ADAPTER_PATH)

# Optional: Merge the adapter for cleaner generation
# If you run out of VRAM, comment this line out, but it simplifies the model object.
model = model.merge_and_unload()
print("Model and adapter loaded successfully.")

# 3. Format the Chat Prompt
chat = [
    {"role": "system", "content": SYSTEM_PROMPT},
    {"role": "user", "content": f"News Summary:\n{NEWS_SUMMARY}"},
]

# Apply the chat template to get the exact format Llama 3 expects
prompt = tokenizer.apply_chat_template(chat, tokenize=False, add_generation_prompt=True)
print("\n--- Input Prompt ---")
print(prompt.strip())

# 4. Generate the Response
inputs = tokenizer(prompt, return_tensors="pt").to("cuda")

# Use greedy decoding for this test
output_tokens = model.generate(
    **inputs,
    max_new_tokens=MAX_NEW_TOKENS,
    do_sample=False,
)

# 5. Decode and Print
output_text = tokenizer.decode(output_tokens[0], skip_special_tokens=True)

# Extract only the assistant's response part
# We look for the last 'assistant' turn since the model generated it.
try:
    response = output_text.split("<|end_header_id|>assistant\n")[-1]
    # Remove any trailing control tokens
    response = response.replace("<|eot_id|>", "").strip()
except IndexError:
    response = "Error parsing response. Raw output:\n" + output_text

print("\n--- TikTok Generation ---")
print(response)
print("-------------------------\n")
