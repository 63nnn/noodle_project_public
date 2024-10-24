import openai
import os
from unittest.mock import patch


import json

with open("training\\gpt fine tuning\\private.json", "r") as file:
    jj = json.load(file)


# Mock API key
openai.api_key = jj["GPT_API_KEY"]

# Simulated mock response for uploading a file
mock_upload_response = {
    "id": "file-mock-id123",
    "object": "file",
    "bytes": 1234,
    "created_at": 1609459200,
    "filename": "mock_training_data.jsonl",
    "purpose": "fine-tune",
}

# Simulated mock response for fine-tuning job creation
mock_fine_tune_response = {
    "id": "ft-mock-job-id123",
    "object": "fine-tune",
    "created_at": 1609459200,
    "model": "gpt-3.5-turbo",
    "status": "pending",
    "fine_tuned_model": None,
}

# Simulated mock status response
mock_status_response = {
    "id": "ft-mock-job-id123",
    "object": "fine-tune",
    "status": "succeeded",
    "fine_tuned_model": "gpt-3.5-turbo-ft-mock-id",
}

# Mock OpenAI API calls
with patch("openai.File.create") as mock_file_create, patch(
    "openai.FineTune.create"
) as mock_fine_tune_create, patch(
    "openai.FineTune.retrieve"
) as mock_fine_tune_retrieve:

    # Mock responses
    mock_file_create.return_value = mock_upload_response
    mock_fine_tune_create.return_value = mock_fine_tune_response
    mock_fine_tune_retrieve.return_value = mock_status_response

    # Upload file simulation
    training_file_id = openai.File.create(
        file=open("path_to_your_training_data.jsonl", "rb"), purpose="fine-tune"
    )["id"]

    print(f"Training file uploaded with ID: {training_file_id}")

    # Create fine-tuning job simulation
    fine_tune_response = openai.FineTune.create(
        model="gpt-3.5-turbo", training_file=training_file_id, n_epochs=3
    )

    print(f"Fine-tuning job created with ID: {fine_tune_response['id']}")

    # Simulate monitoring fine-tuning status
    fine_tune_id = fine_tune_response["id"]
    fine_tune_status = openai.FineTune.retrieve(fine_tune_id)

    print(f"Fine-tuning status: {fine_tune_status['status']}")
    if fine_tune_status["status"] == "succeeded":
        fine_tuned_model = fine_tune_status["fine_tuned_model"]
        print(f"Fine-tuning succeeded. Fine-tuned model: {fine_tuned_model}")
    else:
        print("Fine-tuning failed.")
