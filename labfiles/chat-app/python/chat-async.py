import os
import asyncio
from dotenv import load_dotenv
from openai import AsyncAzureOpenAI
from azure.identity.aio import DefaultAzureCredential

async def main():
    os.system('cls' if os.name == 'nt' else 'clear')

    env_path = os.path.join(os.path.dirname(__file__), '.env')
    load_dotenv(env_path)

    azure_openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    model_deployment = os.getenv("MODEL_DEPLOYMENT")

    if not azure_openai_endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT environment variable is not set")
    if not model_deployment:
        raise ValueError("MODEL_DEPLOYMENT environment variable is not set")

    credential = DefaultAzureCredential()

    async def get_token():
        token = await credential.get_token("https://cognitiveservices.azure.com/.default")
        return token.token

    async with AsyncAzureOpenAI(
        api_version="2025-03-01-preview",
        azure_endpoint=azure_openai_endpoint,
        azure_ad_token_provider=get_token,
    ) as openai_client:
        last_response_id = None

        while True:
            input_text = input("Enter the prompt (or type 'quit' to exit): ")
            if input_text.lower().strip() == "quit":
                break
            if not input_text:
                print("Please enter a prompt.")
                continue

            response = await openai_client.responses.create(
                model=model_deployment,
                instructions="You are a helpful AI assistant that answers questions and provides information.",
                input=input_text,
                previous_response_id=last_response_id,
            )

            print(response.output_text)
            last_response_id = response.id

    await credential.close()

if __name__ == "__main__":
    asyncio.run(main())

