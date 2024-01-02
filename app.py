import streamlit as st
import requests
import json
from datetime import datetime  # Import the datetime module

def generate_response(question):
    api_key = ''  # Replace with your actual API key
    url = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key=' + api_key

    headers = {
        'Content-Type': 'application/json'
    }

    data = {
        'contents': [
            {
                'parts': [
                    {
                        'text': question
                    }
                ]
            }
        ]
    }

    response = requests.post(url, headers=headers, data=json.dumps(data))

    if response.status_code == 200:
        response_json = response.json()
        story_text = response_json['candidates'][0]['content']['parts'][0]['text']
        return story_text
    else:
        return f"Error: {response.status_code}, {response.text}"

def Chat_support():
    st.title("🤖 Intelligent Chat Support")
    st.write("Effortlessly connect with our AI chatbot for swift and expert IT support through text, avoiding the need for human intervention.")
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.first_response_captured = False
    
    # User-provided prompt
    if prompt := st.chat_input():
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user", avatar="🧑‍💻"):
            st.write(prompt)

        # Generate a new response using the Generative Language API
        if st.session_state.messages and st.session_state.messages[-1]["role"] != "assistant":
            with st.chat_message("assistant", avatar="☘️"):
                #placeholder = st.empty()
                #placeholder.markdown("▌")

                # Make a request to the Generative Language API
                start_time = datetime.now()
                response = generate_response(prompt)
                end_time = datetime.now()

                # Display the response in the chat
                st.write(response)

                # Print additional information (for debugging or monitoring)
                print('Original response from API:', response)
                time_taken = end_time - start_time
                print(f"Time taken for API call: {time_taken}")

                # Store the assistant's response in the session state
                message = {"role": "assistant", "content": response}
                st.session_state.messages.append(message)

if __name__ == "__main__":
    Chat_support()
