import os
import shutil
from typing import Optional, Literal
import streamlit as st
from dotenv import load_dotenv; load_dotenv()

def remove_existing_files(directory):
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            st.error(f"Error while removing existing files: {e}")


def get_files_in_directory(directory):
    # This function help us to get the file path along with filename.
    files_list = []

    if os.path.exists(directory) and os.path.isdir(directory):
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)
            
            if os.path.isfile(file_path):
                files_list.append(file_path)

    return files_list

def save_uploaded_file(uploaded_file, directory_name):
    # Function to save uploaded file
    remove_existing_files(directory_name)

    file_path = os.path.join(directory_name, uploaded_file.name)
    with open(file_path, "wb") as file:
        file.write(uploaded_file.read())
    st.sidebar.success("File uploaded successfully")


def llm_calling(
        user_prompt:str,
        system_prompt: Optional[str] = "You are a Large Language Model. You answer questions",
        llm_model: Optional[Literal['gpt-4-turbo-preview', 'gpt-4']] = "gpt-4-turbo-preview",
        temperature: Optional[float] = 1, # 0 to 2
        max_tokens: Optional[int] = 4095, # 1 to 4095
        top_p: Optional[float] = 1, # 0 to 1
        frequency_penalty: Optional[float] = 0, # 0 to 2
        presence_penalty: Optional[float] = 0 # 0 to 2
        ) -> str:
        if not (1 <= max_tokens <= 4095):
          raise ValueError("`max_tokens` must be between 1 and 4095, inclusive.")

        from openai import OpenAI
        client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

        response = client.chat.completions.create(
        model=llm_model,
        messages=[
            {
            "role": "system",
            "content": f"{system_prompt}"
            },
            {
            "role": "user",
            "content": f"{user_prompt}"
            }
        ],
        temperature=temperature,
        max_tokens=max_tokens,
        top_p=top_p,
        frequency_penalty=frequency_penalty,
        presence_penalty=presence_penalty
    )
        
        
        return response.choices[0].message.content


