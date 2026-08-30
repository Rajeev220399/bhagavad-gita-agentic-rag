import sys
from pathlib import Path
SRC_DIR = Path(__file__).resolve().parent

if str(SRC_DIR) not in sys.path:
    sys.path.insert(0, str(SRC_DIR))


from agents import ask_agent

def show_banner():

    print("\n" + "=" * 70)

    print(
        "             BHAGAVAD GITA RAG"
    )

    print("=" * 70)

    print(
        "\nLocal RAG + CrewAI + Ollama + PGVector"
    )

    print(
        "Type 'exit' to close the application."
    )

    print("=" * 70)

def main():

    show_banner()

    while True:

        try:

            question = input(
                "\nQuestion: "
            ).strip()

        except KeyboardInterrupt:

            print(
                "\n\nApplication stopped."
            )

            break

        except EOFError:

            print(
                "\n\nApplication stopped."
            )

            break

        if not question:
            print(
                "Please enter a question."
            )
            continue

        if question.lower() in {
            "exit",
            "quit",
            "q",
        }:

            print(
                "\nThank you. Goodbye! 🙏"
            )

            break

        print(
            "\nThinking...\n"
        )

        try:

            answer = ask_agent(
                question
            )

            print("\n" + "-" * 70)

            print(
                "ANSWER"
            )

            print("-" * 70)

            print(
                answer
            )

            print("-" * 70)

        except Exception as error:

            print("\n" + "=" * 70)

            print(
                "ERROR"
            )

            print("=" * 70)

            print(
                str(error)
            )

            print("=" * 70)

if __name__ == "__main__":

    main()