from langchain.chat_models import ChatOpenAI
from quizzes.schematic_prompt import get_format_parser, prompt_template
from langchain.prompts import ChatPromptTemplate
from get_parms import openai_key
import json


class QuizGenerator:
    def __init__(self, config) -> None:
        self.llm = ChatOpenAI(model_name=config["model_name"],
                              temperature=config["temperature"],
                              openai_api_key=openai_key())
        self.output_parser = get_format_parser()
        self.format_instructions = self.output_parser.get_format_instructions()

    def get_prompt_template(self, topic):
        prompt = ChatPromptTemplate.from_template(template=prompt_template)
        prompt_text = prompt.format_messages(
            topic=topic, format_instructions=self.format_instructions)
        return prompt_text

    def generate_quizzes(self, topic_prompt):
        prompt_text = self.get_prompt_template(topic_prompt)
        response = self.llm(prompt_text)
        try:
            output_dict = self.output_parser.parse(response.content)
            return output_dict
        except Exception as e:
            return f"Error: {e}"


if __name__ == '__main__':
    config = {
        "model_name": "gpt-3.5-turbo",
        "temperature": 0.6

    }
    quiz_generator = QuizGenerator(config)
    chat = quiz_generator.generate_quizzes(topic_prompt="Bayes Theorem")
    print(chat)
