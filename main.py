import os
import sys
from config import MAX_ITERS
import argparse
from dotenv import load_dotenv
from openai import OpenAI
from prompts import system_prompt
from call_function import call_function, available_functions

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()
    
    if not api_key:
        raise RuntimeError("api_key is None type")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]

    for i in range(20):
        result = generate_content(client, messages, args.verbose)

        if result:
            print(result)
            return 
    
    print("Maximum number of iterations processed without a final result")
    sys.exit(1)

    
def generate_content(client: OpenAI, messages: list, verbose: bool) -> str | None:
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools=available_functions,
    )
    
    if not response.usage:
        raise RuntimeError("metadata is None Type")

    if verbose:  
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    messages.append(message)

    if message.tool_calls:
        for tool_call in message.tool_calls:
            result_message = call_function(tool_call, verbose)
            if not result_message.get("content"):
                raise RuntimeError(f"Empty function response for {tool_call.function.name}")
            messages.append(result_message)
            if verbose:
                print(f"-> {result_message['content']}")
    else:
        return message.content

if __name__ == "__main__":
    main()