import torch
from datasets import load_dataset
from transformers import (
    AutoTokenizer,
    AutoModelForCausalLM,
    TrainingArguments,
    Trainer,
    DataCollatorForLanguageModeling
)
from peft import LoraConfig, get_peft_model

# ----------------------------
# Model
# ----------------------------
model_name = "gpt2"

tokenizer = AutoTokenizer.from_pretrained(model_name)
tokenizer.pad_token = tokenizer.eos_token

model = AutoModelForCausalLM.from_pretrained(model_name)

# ----------------------------
# LoRA Configuration (smaller = faster)
# ----------------------------
lora_config = LoraConfig(
    r=4,
    lora_alpha=8,
    target_modules=["c_attn"],
    lora_dropout=0.05,
    bias="none",
    task_type="CAUSAL_LM"
)

model = get_peft_model(model, lora_config)
model.print_trainable_parameters()

# ----------------------------
# Dataset (LIMIT TO 1000 LINES)
# ----------------------------
dataset = load_dataset("text", data_files={"train": "jarvis_dataset.txt"})

# Use only first 1000 lines for fast training
max_samples = min(1000, len(dataset["train"]))
dataset["train"] = dataset["train"].select(range(max_samples))

def tokenize_function(examples):
    return tokenizer(
        examples["text"],
        truncation=True,
        padding="max_length",
        max_length=64   # smaller = much faster
    )

tokenized_dataset = dataset.map(
    tokenize_function,
    batched=True,
    remove_columns=["text"]
)

data_collator = DataCollatorForLanguageModeling(
    tokenizer=tokenizer,
    mlm=False
)

# ----------------------------
# Training Arguments (FAST)
# ----------------------------
training_args = TrainingArguments(
    output_dir="./jarvis_lora",
    num_train_epochs=1,                     # only 1 epoch
    per_device_train_batch_size=8,          # bigger batch
    logging_steps=10,
    save_strategy="no",                     # don’t save during training
    report_to="none",
    fp16=torch.cuda.is_available(),         # faster if GPU available
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset["train"],
    data_collator=data_collator
)

# ----------------------------
# Train
# ----------------------------
trainer.train()

# Save final model
model.save_pretrained("./jarvis_lora")
tokenizer.save_pretrained("./jarvis_lora")

print("⚡ Fast LoRA training complete.")