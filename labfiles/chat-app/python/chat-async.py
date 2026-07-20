# import namespaces for async
import asyncio
from openai import AsyncOpenAI
from azure.identity.aio import DefaultAzureCredential, get_bearer_token_provider                                 

async def main():                                                                                                                                                                                                                                                                                                                                                                                                                                           
    
    #  Initialize an async OpenAI client
credential = DefaultAzureCredential()
token_provider = get_bearer_token_provider(
 credential, "https://ai.azure.com/.default"
)

async_client = AsyncOpenAI(
     base_url=azure_openai_endpoint,
     api_key=token_provider
)
# Await an asynchronous response
response = await async_client.responses.create(
             model=model_deployment,
             instructions="You are a helpful AI assistant that answers questions and provides information.",
             input=input_text,
             previous_response_id=last_response_id
)
assistant_text = response.output_text
print("Assistant:", assistant_text)
last_response_id = response.id

# Close the async client session
 await credential.close()

