import time
from typing import List
from tqdm import tqdm

from instructor import patch
from openai import OpenAI

from financial_datasets.dataset import DatasetItem, Dataset

system_prompt = """
You are an expert at understanding and analyzing financial documents. 
Your role is to generate question and ground truth answer pairs based on the provided financial text. 
The types of texts you will be working with include 10-Ks, 10-Qs, earnings call transcripts, and other financial documents.

When generating questions and answers, adhere to the following guidelines:
1. Your ground truth answers must be directly derived from the content within the provided text. Do not make up, hallucinate, or generate answers that are not explicitly supported by the given text.
2. Ensure that the questions you generate are relevant to the financial context and can be answered based on the information provided in the text.
3. Include the relevant 'context' paragraph from which you generated each question and ground truth answer pair. The 'context' paragraph MUST contain the specific information that supports the ground truth answer.
4. If the provided text does not contain sufficient information to generate a question-answer pair, do not attempt to create one.
5. Your responses should be in the following format:
   Question: [Generated question]
   Answer: [Ground truth answer]
   Context: [Relevant paragraph from the text that supports the answer]

Remember, your primary objective is to create accurate, grounded, and contextually relevant question-answer pairs while strictly avoiding any fabrication or speculation.
"""


class DatasetGenerator:
    def __init__(self, model: str, api_key: str):
        # Ensure model begins with gpt-
        if not model.startswith('gpt-'):
            raise NotImplementedError(f'Model {model} is not supported yet.')

        if not api_key:
            raise ValueError("API key is required.")

        self._model = model
        self._client = patch(OpenAI(api_key=api_key))

    def generate_from_texts(self, texts: List[str], max_questions=10) -> Dataset:
        items: List[DatasetItem] = []
        num_texts = len(texts)
        questions_per_text = max_questions // num_texts
        remaining_questions = max_questions % num_texts

        progress_bar = tqdm(total=max_questions, desc="Generating questions", colour='green')

        for index, text in enumerate(texts):
            try:
                # Determine the number of questions to generate for the current text
                current_max_questions = questions_per_text
                if index < remaining_questions:
                    current_max_questions += 1

                # Generate questions
                response = self._client.chat.completions.create(
                    model=self._model,
                    response_model=Dataset,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": f"Generate {current_max_questions} questions for the following block of text: {text}"}
                    ],
                )

                # Add the generated items to our total list of questions
                items.extend(response.items)

                # Update the progress bar by the number of questions generated
                progress_bar.update(len(response.items))
            except Exception as e:
                print(f"Failed to generate questions for batch {index + 1}: {e}")
                continue

            # Sleep for 1 second to avoid overloading the LLM
            time.sleep(1)

        # Ensure the progress bar is closed
        progress_bar.close()

        return Dataset(
            items=items,
        )
