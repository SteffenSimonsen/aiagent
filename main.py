import os 
import sys
from dotenv import load_dotenv
from google import genai
from google.genai import types

from functions.get_files_info import schema_get_files_info
from functions.get_file_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python_file import schema_run_python_file
from functions.call_function import call_function

def main():
    #setup 
    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key)
    
    
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    If you are in doubt of where files are located you should go and search for them your self. You can list files and directories, you can use this tool to find the file path youre looking for.
    
    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    #functions available for the LLM
    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_write_file,
            schema_run_python_file
        ]
    )


    #user command line input
    try:
        user_prompt = sys.argv[1]
    except:
        print("No prompt provided, exiting...")
        sys.exit(1)

    
    #messages allows for history
    messages = [
        types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]


    for i in range (20):
        try:
            #model interaction
            response = client.models.generate_content(
                model='gemini-2.0-flash-001',  
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions],
                    system_instruction=system_prompt)
            )

            if not response.function_calls:
                if response.text:
                    print(response.text)
                break


            response_candidates = response.candidates

            for candidate in response_candidates:
                messages.append(candidate.content)
            
            #response parsing

            # if not response.function_calls:
            #     print(response.text)
            # else:
            for function_call_part in response.function_calls:

                function_call_result = call_function(function_call_part)

                messages.append(types.Content(role="user",
                                              parts=function_call_result.parts
                                              )) 

                if not function_call_result.parts[0].function_response.response:
                    raise Exception("Something went wrong with execution of the function")
                
                
                if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
                    print(f"-> {function_call_result.parts[0].function_response.response}")
                
        
        except Exception as e:
            print(f"The agent broke: {e}")
            print("Exiting")
            sys.exit(1)
            
    if len(sys.argv) > 2 and sys.argv[2] == "--verbose":
            
            print(f"User prompt: {user_prompt}")    
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

if __name__ == "__main__":
    main()
