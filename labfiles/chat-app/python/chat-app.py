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
            api_version="2024-08-01-preview",
            azure_endpoint=project_connection,
            azure_ad_token_provider=lambda: DefaultAzureCredential().get_token("https://cognitiveservices.azure.com/.default").token,
        )

        while True:
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            # Get a chat completion response
            response = openai_client.chat.completions.create(
                model=model_deployment,
                messages=[
                    {"role": "system", "content": "You are a helpful AI assistant that answers questions and provides information."},
                    {"role": "user", "content": input_text},
                ],
            )
            print(response.choices[0].message.content)

    except Exception as ex:
        print(f"Error: {ex}")
        print(f"Error type: {type(ex).__name__}")
        
        # Print environment variables for debugging
        print(f"\nDebug info:")
        print(f"AZURE_OPENAI_ENDPOINT: {os.getenv('AZURE_OPENAI_ENDPOINT')}")
        print(f"MODEL_DEPLOYMENT: {os.getenv('MODEL_DEPLOYMENT')}")


if __name__ == '__main__':
    main()
