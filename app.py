import streamlit as st
import os
from PIL import Image
from utils import utils
from lyzr_qa import question_generation

st.set_page_config(
    page_title="Lyzr-Question Answer Generation",
    layout="centered",  # or "wide" 
    initial_sidebar_state="auto",
    page_icon="./logo/lyzr-logo-cut.png"
)

data = "data"
os.makedirs(data, exist_ok=True)

image = Image.open("./logo/lyzr-logo.png")
st.image(image=image, width=150) # logo for main page
st.title('Lyzr-Question Answer Generation📚')
st.markdown('Welcome to the lyzr Question Generation app, this app will help you to generate questions and their responses on given pdf file!!!')

st.markdown("""
    <style>
    .reportview-container .main .block-container {
        max-width: 1200px;
        padding-top: 2rem;
        padding-right: 3rem;
        padding-left: 3rem;
        padding-bottom: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

def rag_response(topic):
    agent = question_generation()
    metric = f""" Tell me everything you know about this {topic}, Provide a detailed reponse on this {topic} from the given file"""
    response = agent.query(metric)
    return response.response


def gpt_questions(rag_response, topic, number):
    response = utils.llm_calling(user_prompt=f"Develop some {number} numbers of questions on {rag_response} that is clear, relevant, and specific which obeys the {topic}"
                                 f"[!important] Consider the context and purpose of the inquiry, aiming for open-endedness to encourage discussion or exploration. Engage the audience's curiosity while ensuring the question prompts meaningful responses",
                                   system_prompt=f"You are an expert of this {topic}",llm_model="gpt-4-turbo-preview")
    return response



def gpt_answers(questions, topic):
    answers = utils.llm_calling(user_prompt=f'Provide a detailed response to the following {questions}'
                                f"[!important] Elaborating on relevant examples, concepts, and explanations to thoroughly explore the topic"
                                f"[!important] Your answer should delve into the intricacies of the subject matter, drawing upon your understanding and expertise to provide comprehensive insights. Provide examples for each responses", system_prompt=f'You are an expert of this {topic}', llm_model="gpt-4-turbo-preview")

    return answers


def default_file():
    st.sidebar.info('Default File: Object Oriented Programming')
    st.sidebar.markdown(""" ##### Topics can be:
    - Inheritance
    - Polymorphsim
    - Abstraction
    - Encapsualtion
                        """)
    

    user_topic = st.sidebar.text_input('Enter the topic according to subject')
    number_questions = st.sidebar.text_input('Enter the number of questions')
    
    if user_topic is not None:
        button=st.sidebar.button('Submit')
        if (button==True):
            response = rag_response(topic=user_topic) # getting response from rag
            gpt_response = gpt_questions(rag_response=response, topic=user_topic, number=number_questions) # Create n number of response with gpt call
            gpt_answer = gpt_answers(questions=gpt_response, topic=user_topic) # create the responses for questions
            st.subheader('Questions')
            st.write(gpt_response)
            st.markdown('---')
            st.subheader('Answers')
            st.write(gpt_answer)


def upload_file():
    file = st.sidebar.file_uploader("Upload a Subject Book Pdf", type=["pdf"])
    if file is not None:
        utils.save_uploaded_file(file, directory_name=data)

        user_topic = st.sidebar.text_input('Enter the topic according to subject')
        number_questions = st.sidebar.text_input('Enter the number of questions')

        if user_topic is not None:
            button=st.sidebar.button('Sumbit')
            if (button==True):
                response = rag_response(topic=user_topic) # getting response from rag
                gpt_response = gpt_questions(rag_response=response, topic=user_topic, number=number_questions) # Create n number of response with gpt call
                gpt_answer = gpt_answers(questions=gpt_response, topic=user_topic) # create the responses for questions
                st.subheader('Questions')
                st.write(gpt_response)
                st.markdown('---')
                st.subheader('Answers')
                st.write(gpt_answer)
                
    else:
        st.sidebar.warning('Please Upload subject pdf file!!!')


def main():
    image = Image.open("./logo/lyzr-logo.png")
    st.sidebar.image(image, width=150) # logo for side bar
    st.sidebar.subheader('Lyzr- QnA Generator')
    

    if st.sidebar.button('Start with Upload file'):
        upload_file()

    if st.sidebar.button('Start with Default file'):
        default_file()

if __name__ == "__main__":
    main()
