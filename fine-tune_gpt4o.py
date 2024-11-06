from openai import OpenAI
client = OpenAI()

file = client.files.create(
  file=open("output_finetune_data_176.jsonl", "rb"),
  purpose="fine-tune"
)

fine_tune_job = client.fine_tuning.jobs.create(
  training_file=file.id,
  model="gpt-4o-mini-2024-07-18",
  suffix='Tairan_176data',
  hyperparameters={
    "n_epochs": 3,
    "batch_size": 3,
    "learning_rate_multiplier": 0.05
  }
)

# job_info = client.fine_tuning.jobs.retrieve(fine_tune_job.id)
# print(job_info['hyperparameters'])