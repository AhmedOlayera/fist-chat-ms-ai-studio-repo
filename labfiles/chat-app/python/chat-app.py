import os
from openai import AzureOpenAI
from azure.identity import DefaultAzureCredential
from dotenv import load_dotenv


def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    try:
        # Load configuration settings
        env_path = os.path.join(os.path.dirname(__file__), '.env')
        load_dotenv(env_path)
        project_connection = os.getenv("AZURE_OPENAI_ENDPOINT")
        model_deployment = os.getenv("MODEL_DEPLOYMENT")

        if not project_connection:
            raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is not set")
        if not model_deployment:
            raise ValueError("MODEL_DEPLOYMENT environment variable is not set")

        openai_client = AzureOpenAI(
            api_version="2025-03-01-preview",
            azure_endpoint=project_connection,
            azure_ad_token_provider=lambda: DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default").token,
        )
        # Track responses
        last_response_id = None

        while True:
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue
# Get a response
stream = openai_client.responses.create(
             model=model_deployment,
             instructions="You are a helpful AI assistant that answers questions and provides information.",
             input=input_text,
             previous_response_id=last_response_id,
             stream=True
)
for event in stream:
     if event.type == "response.output_text.delta":
         print(event.delta, end="")
     elif event.type == "response.completed":
         last_response_id = event.response.id
print()
            response = openai_client.responses.create(
                model=model_deployment,
                instructions="You are a helpful AI assistant that answers questions and provides information.",
                input=input_text,
                previous_response_id=last_response_id,
            )

            print(response.output_text)
            last_response_id = response.id

    except Exception as ex:
        print(f"Error: {ex}")
        print(f"Error type: {type(ex).__name__}")

        # Print environment variables for debugging
        print(f"\nDebug info:")
        print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
        print(f"MODEL_DEPLOYMENT: {os.getenv('MODEL_DEPLOYMENT')}")


if __name__ == '__main__':
    main()
