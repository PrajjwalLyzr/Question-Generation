import streamlit as st
import os
from PIL import Image
from utils import utils
from lyzr_qa import question_generation


utils.page_config()

data = "data"
os.makedirs(data, exist_ok=True)

image = Image.open("./logo/lyzr-logo.png")
st.image(image, width=150)
st.title('Lyzr-Question Answer Generation📚')
st.markdown('Welcome to the lyzr Question Generation app, this app will help you to generate questions and their responses on given pdf file !!!')


def rag_response(topic, path):
    agent = question_generation(path)
    metric = f""" You are an expert of this {topic}. Tell me everything you know about this {topic}, Provide a detailed reponse on this {topic} from the given file"""
    response = agent.query(metric)
    return response.response


def gpt_questions(response, topic, number):
    response = utils.llm_calling(user_prompt=f"Develop some {number} numbers of questions on {response} that is clear, relevant, and specific which obeys the {topic}"
                                 f"[!important] Consider the context and purpose of the inquiry, aiming for open-endedness to encourage discussion or exploration",
                                   system_prompt=f"You are an expert of this {topic}",llm_model="gpt-4-turbo-preview")
    return response



def gpt_answers(questions, topic):
    answers = utils.llm_calling(user_prompt=f"""Provide a detailed response to the following {questions}, including relevant examples, explanations, and, if applicable, diagrams or code examples to illustrate your points. Additionally, consider discussing both the advantages and disadvantages of the topic to provide a comprehensive analysis.
                                Your answer should aim to offer a well-rounded understanding of the subject matter, highlighting its complexities and implications."""
                                , system_prompt=f'You are an expert of this {topic}', llm_model="gpt-4-turbo-preview")

    return answers

def default():
    st.info('Default file: Object Oriented Programming')
    st.markdown(""" ##### Topics can be:
    1. Inheritance
    2. Polymorphsim
    3. Abstraction
    4. Encapsulation               """)
        
    path = './Object Oriented Programming.pdf'

    user_topic = st.text_input('Enter the topic according to subject')
    number_questions = st.text_input('Enter the number of questions')

    if user_topic is not None:
        if st.button('Submit'):
            rag_generated_response = rag_response(topic=user_topic, path=path)  # getting reponse from rag about the subject/topic
            gpt_response = gpt_questions(response=rag_generated_response, topic=user_topic, number=number_questions) # create n number of question on rag response
            gpt_answer = gpt_answers(questions=gpt_response, topic=user_topic) # create the answers for the questions
            st.subheader('Questions')
            st.write(gpt_response)
            st.markdown('---')
            st.subheader('Answers')
            st.write(gpt_answer)

def upload():
    file = st.file_uploader("Upload a Subject Book Pdf", type=["pdf"])
    if file:
        utils.save_uploaded_file(file, directory_name=data)
        path = utils.get_files_in_directory(directory=data)
        filepath = path[0] # get the first filepath

        user_topic = st.text_input('Enter the topic according to subject')
        number_questions = st.text_input('Enter the number of questions')

        if user_topic is not None:
            if st.button('Submit'):
                rag_generated_response = rag_response(topic=user_topic, path=filepath)  # getting reponse from rag about the subject/topic
                gpt_response = gpt_questions(response=rag_generated_response, topic=user_topic, number=number_questions) # create n number of question on rag response
                gpt_answer = gpt_answers(questions=gpt_response, topic=user_topic) # create the answers for the questions
                st.subheader('Questions')
                st.write(gpt_response)
                st.markdown('---')
                st.subheader('Answers')
                st.write(gpt_answer)
            
    else:
        st.warning('Please Upload subject pdf file!!!')

def main(): 
    image = Image.open("./logo/lyzr-logo.png")
    st.sidebar.image(image, width=150)
    st.sidebar.subheader('Lyzr- QnA Generator')

    # session state for default button
    if 'default_button' not in st.session_state:
        st.session_state.default_button = False


    # session state for upload button
    if 'upload_button' not in st.session_state:
        st.session_state.upload_button = False


    def default_button():
        st.session_state.default_button = True
        st.session_state.upload_button = False

    def upload_button():
        st.session_state.upload_button = True
        st.session_state.default_button = False


    st.sidebar.button('Default File', on_click=default_button)
    st.sidebar.button('Upload File', on_click=upload_button)


    if st.session_state.default_button: 
        default()

    if st.session_state.upload_button:
        upload()
        
        

if __name__ == "__main__":
    utils.style_app()
    main()
    utils.template_end()
