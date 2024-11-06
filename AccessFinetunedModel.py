from openai import OpenAI
import datetime

client = OpenAI()


# client.fine_tuning.jobs.cancel("ftjob-YwkLtTGGfN2npXkQrktpKgEK")

# List 10 fine-tuning jobs
fine_tuning_jobs = client.fine_tuning.jobs.list(limit=5)

# Output the list of fine-tuning jobs in a readable format
print("Listing fine-tuning jobs:")
i = 0
for job in fine_tuning_jobs:
    if i >= 3:
        break
    human_readable_time = datetime.datetime.utcfromtimestamp(job.created_at).strftime('%Y-%m-%d %H:%M:%S')
    print(f"Job ID: {job.id}")
    print(f"Status: {job.status}")
    print(f"Model: {job.fine_tuned_model if job.fine_tuned_model else 'Not Available'}")
    print(f"Created At: {human_readable_time}")
    print(f"Hyperparameters: {job.hyperparameters}")
    print("-" * 40)  # Separator for readability
    i += 1

# job_info = client.fine_tuning.jobs.retrieve('ftjob-4DLUfg5xeBdpAj7eTOjvALOV')
# print(job_info.hyperparameters)

# # Retrieve the state of a fine-tune
# client.fine_tuning.jobs.retrieve("ftjob-abc123")
#
# # Cancel a job
# client.fine_tuning.jobs.cancel("ftjob-qg4gqIPRnwcNhSzvDFgFeiNx")
#
# # List up to 10 events from a fine-tuning job
# client.fine_tuning.jobs.list_events(fine_tuning_job_id="ftjob-abc123", limit=10)
#
# # Delete a fine-tuned model (must be an owner of the org the model was created in)
# client.models.delete("ft:gpt-3.5-turbo:acemeco:suffix:abc123")
