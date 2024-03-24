import re
import time
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain
from langchain_core.output_parsers import BaseOutputParser, StrOutputParser

load_dotenv()

class PythonCodeOutputParser(BaseOutputParser):
    """
    An output parser that extracts Python code encapsulated within
    triple backticks from the model's output.
    """
    def parse(self, output: str) -> str:
        pattern = r"```python\n(.*?)```"
        match = re.search(pattern, output, re.DOTALL)
        if match:
            return match.group(1).strip()
        else:
            raise ValueError("Invalid result format from AI model.")

def code_generate(code: str, user_prompt: str):

    chat_template = ChatPromptTemplate.from_messages([
        ("system", "당신은 유능한 파이썬 프로그래머 입니다. 사용자의 질문에 맞게 코드를 생성/수정 하세요. 코드는 ```python\n ```로 감싸주세요. 답변은 코드만 작성해주세요. 코딩과 관련 없는 질문은 답변하지 않습니다."),
        ("human", "```python\n{code}```, {user_prompt} 코드에 한국어 주석을 달아 설명해주세요."),
    ])

    llm = ChatOpenAI()

    max_retries = 3
    retry_delay = 1

    for attempt in range(max_retries):
        try:
            chat_template.format_messages(code="code", user_prompt="user_prompt")
            chain = chat_template | llm | PythonCodeOutputParser()
            result = chain.invoke({"code": code, "user_prompt": user_prompt})
            print("✅ Code generation successful.")
            return result
        except Exception as e:
            print(f"🔄 Attempt {attempt + 1} failed with error: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise Exception("❌ Maximum retries reached, failing...")



##################################################################
# # 예시 사용법
# code = """
# # 업무 자동화를 위한 예시 코드
# import pyautogui
# import time

# # 업부 자동화를 위한 함수 정의
# def automate_work():
#     # 업무를 수행할 프로그램을 실행
#     # 여기서는 메모장을 예시로 함
#     pyautogui.press('winleft')
#     pyautogui.write('notepad')
#     pyautogui.press('enter')
#     time.sleep(1)

#     # 업무 수행
#     pyautogui.write('업무 내용을 입력하세요.')

#     # 저장 및 종료
#     pyautogui.hotkey('ctrl', 's')
#     time.sleep(1)
#     pyautogui.write('파일명.txt')
#     pyautogui.press('enter')

#     pyautogui.hotkey('alt', 'f4')

# # 업무 자동화 함수 호출
# automate_work()
# """

# user_prompt = "셀레니움을 사용하여 인스타그랩에 자동으로 로그인하고 관련 계정에 좋아요를 누르는 코드를 작성해주세요."

# result = code_generate('', user_prompt)
# print(result)