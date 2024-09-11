from typing import Optional, List
from llm_sandbox import SandboxSession
from langchain import hub
from langchain_openai import ChatOpenAI
from langchain.tools import tool
from langchain.agents import AgentExecutor, create_tool_calling_agent
import os
from dotenv import load_dotenv
load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

@tool
def run_code(lang: str, code: str, libraries: Optional[List] = None) -> str:
    """
    Run code in a sandboxed environment.
    :param lang: The language of the code.
    :param code: The code to run.
    :param libraries: The libraries to use, it is optional.
    :return: The output of the code.
    """
    with SandboxSession(lang=lang, verbose=False) as session:  # type: ignore[attr-defined]
        return session.run(code, libraries).text


if __name__ == "__main__":
    llm = ChatOpenAI(openai_api_key=OPENAI_API_KEY, model="gpt-4o", temperature=0)
    prompt = hub.pull("hwchase17/openai-functions-agent")
    tools = [run_code]

    agent = create_tool_calling_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)
    output = agent_executor.invoke(
        {
            "input": "Write python code to calculate Pi number by Monte Carlo method then run it."
        }
    )
    print(output)

    output = agent_executor.invoke(
        {
            "input": "Write python code to calculate the factorial of a number then run it."
        }
    )
    print(output)

    output = agent_executor.invoke(
        {"input": "Write python code to calculate the Fibonacci sequence then run it."}
    )
    print(output)