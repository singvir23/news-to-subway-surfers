import torch
import json
import os
from datasets import load_dataset
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    TrainingArguments,
    logging,
)
from peft import LoraConfig, prepare_model_for_kbit_training
from trl import SFTTrainer

logging.set_verbosity_warning()

# ----------------------------
# CONFIG
# ----------------------------
# Using the instruction-tuned version for chat/instruction fine-tuning

HF_TOKEN =  # hugging face token. create a READ token and paste that here OR Into a dotenv
MODEL_PATH = "meta-llama/Llama-3.1-8B-Instruct" # can also use meta-llama 3 7b instruct

# make sure you request permission on hugging face to get access to these models. it should not take long.


# Ensure this file is in the same directory as the script
DATA_PATH = "./data/reddit_transcripts.csv" # or you can copy the path
OUTPUT_DIR = "/opt/ml/model" # automatic path created by sagemaker

# QLoRA Parameters
LORA_R = 64
LORA_ALPHA = 16
LORA_DROPOUT = 0.1

# Training Parameters
MAX_LENGTH = 512
BATCH_SIZE = 1           # Small batch size for QLoRA memory efficiency
GRAD_ACCUM = 8           # Accumulate gradients over 8 steps for an effective batch size of 8
EPOCHS = 3               # Run for 3 full epochs on the small dataset
LEARNING_RATE = 2e-4     # Standard QLoRA learning rate

# ----------------------------
# 4-bit Quantization Configuration (QLoRA)
# ----------------------------
bnb_config = BitsAndBytesConfig(
    load_in_4bit=True,
    bnb_4bit_use_double_quant=True,
    bnb_4bit_quant_type="nf4",
    bnb_4bit_compute_dtype=torch.bfloat16
)

# format data 

def formatting_function(examples):
    """
    Formats the raw 'tiktok_script' into the Llama-3.1 instruction template.
    We treat the instruction as the 'user' turn and the script as the 'assistant' response.
    """
    # The instruction prompt that will be consistent across all examples
    instruction = "Generate a viral short-form video script in the Gen Z voice for a TikTok video." # we can change these if needed 
    output_texts = []
    
    for script in examples["tiktok_script"]: # will iterate through all the scripts in the data 
        # The Llama 3/3.1 Chat Template format:
        text = (
            f"<|begin_of_text|><|start_header_id|>user<|end_header_id|>\n"
            f"{instruction}<|eot_id|><|start_header_id|>assistant<|end_header_id|>\n"
            f"{script}<|eot_id|>"
        )
        output_texts.append(text)
        
    return {"text": output_texts}

# model & tokenizer setup
print(f"Loading model with 4-bit quantization...")
model = AutoModelForCausalLM.from_pretrained(
    "meta-llama/Meta-Llama-3.1-8B-Instruct", # can also use MODEL_PATH here, but i just used the name since it wasn't working
    quantization_config=bnb_config,
    device_map=None, 
    dtype=torch.bfloat16, 
)

model.config.use_cache = False

tokenizer = AutoTokenizer.from_pretrained("meta-llama/Meta-Llama-3.1-8B-Instruct", token=HF_TOKEN) 
if tokenizer.pad_token is None:
    tokenizer.pad_token = tokenizer.eos_token
tokenizer.padding_side = "right" # Llama requires right padding

# Prepare model for K-bit training (QLoRA)
model = prepare_model_for_kbit_training(model) 

# peft/lora config
peft_config = LoraConfig(
    lora_alpha=LORA_ALPHA,
    lora_dropout=LORA_DROPOUT,
    r=LORA_R,
    bias="none",
    task_type="CAUSAL_LM",
    # Target all linear layers for maximum effect
    target_modules=["q_proj", "k_proj", "v_proj", "o_proj", "gate_proj", "up_proj", "down_proj"], 
)

# Data Loading and Preprocessing

print(f"Loading and formatting dataset: {DATA_PATH}...")

# Load the local JSON file (assuming it contains a list of objects with 'tiktok_script')
raw_dataset = load_dataset("json", data_files=DATA_PATH, split="train") 

# Split the small dataset into train/test
dataset = raw_dataset.train_test_split(test_size=0.1) 
train_dataset = dataset["train"]
eval_dataset = dataset["test"]

# Apply the formatting function to prepare the data for training
# This creates the new 'text' column that SFTTrainer uses
train_dataset = train_dataset.map(formatting_function, batched=True, remove_columns=list(raw_dataset.column_names))
eval_dataset = eval_dataset.map(formatting_function, batched=True, remove_columns=list(raw_dataset.column_names))

#training arguments 
training_args = TrainingArguments(
    output_dir=OUTPUT_DIR,
    # Set evaluation and saving steps appropriately for a small dataset
    eval_strategy="steps",
    save_strategy="epoch",
    logging_steps=5, 
    eval_steps=10, 
    per_device_train_batch_size=BATCH_SIZE, 
    gradient_accumulation_steps=GRAD_ACCUM, 
    num_train_epochs=EPOCHS, 
    learning_rate=LEARNING_RATE, 
    optim="paged_adamw_8bit", # Optimizer optimized for QLoRA
    warmup_ratio=0.03,
    bf16=True, # Use bfloat16 for fast and stable training
    group_by_length=False, 
    lr_scheduler_type="constant",
    report_to="none" 
)

# initialize qlora 

print("Initializing SFT Trainer...")
trainer = SFTTrainer(
    model=model,
    train_dataset=train_dataset,
    eval_dataset=eval_dataset,
    peft_config=peft_config,
    args=training_args, 
)

# begin fine-tuning
print("\nStarting QLoRA fine-tuning...")
trainer.train()
print("QLoRA fine-tuning completed.")

# Save final adapter weights and tokenizer
trainer.model.save_pretrained(OUTPUT_DIR)
tokenizer.save_pretrained(OUTPUT_DIR)

print(f"\nAdapter weights and tokenizer saved to: {OUTPUT_DIR}")


#checkpoint: the use_reentrant parameter should be passed explicitly. 
# Starting in PyTorch 2.9, calling checkpoint without use_reentrant will raise an exception. 
# use_reentrant=False is recommended, but if you need to preserve the current default behavior, you can pass use_reentrant=True. 
# Refer to docs for more details on the differences between the two variants.
