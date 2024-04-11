import os
from lyzr import QABot
from dotenv import load_dotenv; load_dotenv()
from pathlib import Path


os.environ['OPENAI_API_KEY'] = os.getenv('OPENAI_API_KEY')


def question_generation(path):

    qa_bot = QABot.pdf_qa(
    input_files=[Path(path)],
    )

    return qa_bot


