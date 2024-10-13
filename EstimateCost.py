import json
import tiktoken

#Total number of tokens: 9596
encoding = tiktoken.encoding_for_model("gpt-4o-mini")

# Path to your JSONL file
jsonl_file_path = "output_finetune_data.jsonl"

# Function to calculate tokens in a single string
def count_tokens(text):
    tokens = encoding.encode(text)
    return len(tokens)

# Read the JSONL file and count tokens
total_tokens = 0
with open(jsonl_file_path, "r", encoding="utf-8") as file:
    for line in file:
        data = json.loads(line)  # Load each JSON object
        # You can customize this based on the structure of your JSON
        # Example assuming `data` has "question" and "answer" fields
        for message in data.get("messages", []):
            content = message.get("content", "")
            total_tokens += count_tokens(content)

print(f"Total number of tokens: {total_tokens}")
