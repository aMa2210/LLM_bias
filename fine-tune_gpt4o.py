from openai import OpenAI
client = OpenAI()

file = client.files.create(
  file=open("output_finetune_data.jsonl", "rb"),
  purpose="fine-tune"
)

client.fine_tuning.jobs.create(
  training_file=file.id,
  model="gpt-4o-mini-2024-07-18",
  suffix='Tairan',
  hyperparameters={
    "n_epochs": 2,
    "learning_rate_multiplier": 0.1
  }
)