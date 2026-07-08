import os
from openai import OpenAI
from azure.identity import DefaultAzureCredential, get_bearer_token_provider
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

        token_provider = get_bearer_token_provider(
            DefaultAzureCredential(), "https://ai.azure.com/.default"
        )

        openai_client = OpenAI(
            base_url=project_connection,
            api_key=token_provider,
        )

        while True:
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower() == "quit":
                break
            if len(input_text) == 0:
                print("Please enter a prompt.")
                continue

            completion = openai_client.chat.completions.create(
                model=model_deployment,
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful AI assistant that answers questions and provides information."
                    },
                    {
                        "role": "user",
                        "content": input_text
                    }
                ]
            )
            print(completion.choices[0].message.content)

    except Exception as ex:
        print(ex)


if __name__ == '__main__':
    main()
