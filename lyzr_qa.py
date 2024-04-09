import os
from lyzr import QABot
from dotenv import load_dotenv; load_dotenv()
from utils import utils


os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


def question_generation():

    file = utils.get_files_in_directory('data')
    qa_bot = QABot.pdf_qa(
    input_files=file,
    )

    return qa_bot


