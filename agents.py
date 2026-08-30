import sys
from pathlib import Path
SRC_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))

from crewai import Agent, Crew, Process, Task, LLM

from config import (
    OLLAMA_BASE_URL,
    OLLAMA_LLM,
)

from tools import search_bhagavad_gita
local_llm = LLM(
    model=f"ollama/{OLLAMA_LLM}",
    base_url=OLLAMA_BASE_URL,
    temperature=0.1,
)

def create_rag_agent():

    return Agent(

        role="Bhagavad Gita Research Assistant",

        goal=(
            "Answer questions about the Bhagavad Gita "
        ),

        backstory=(
            "You are a research assistant. "
            "You always search the Bhagavad Gita "
        ),

        llm=local_llm,

        tools=[
            search_bhagavad_gita
        ],

        verbose=True,

        allow_delegation=False,
    )

def create_task(
    agent,
    question: str,
):

    return Task(

        description=f"""
Answer the question:

{question}
""",

        expected_output=(
            "Bhagavad Gita passages, including source"
        ),

        agent=agent,
    )

def ask_agent(
    question: str,
):

    agent = create_rag_agent()

    task = create_task(
        agent=agent,
        question=question,
    )

    crew = Crew(

        agents=[
            agent
        ],

        tasks=[
            task
        ],

        process=Process.sequential,

        verbose=True,
    )

    result = crew.kickoff()

    return str(result)

def main():

    print("\n" + "=" * 70)
    print("=" * 70)

    print(
        f"\nLocal LLM : {OLLAMA_LLM}"
    )

    print(
        f"Ollama    : {OLLAMA_BASE_URL}"
    )

    print(
        "\nCommands:"
    )

    print(
        "  exit  -> quit"
    )

    print("=" * 70)

    while True:

        try:

            question = input(
                "\nYou: "
            ).strip()

        except KeyboardInterrupt:

            print(
                "\n\nExiting..."
            )

            break

        except EOFError:

            print(
                "\n\nExiting..."
            )

            break

        if question.lower() in {
            "exit",
            "quit",
        }:

            print(
                "\nGoodbye!"
            )

            break

        if not question:
            continue

        try:

            answer = ask_agent(
                question
            )

            print("\n")
            print("=" * 70)
            print("FINAL ANSWER")
            print("=" * 70)

            print(
                answer
            )

            print("=" * 70)

        except Exception as error:

            print("\n")
            print("=" * 70)
            print("ERROR")
            print("=" * 70)

            print(
                error
            )

            print("=" * 70)

if __name__ == "__main__":
    main()