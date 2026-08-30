from typing import Dict, List
class ConversationMemory:
    
    def __init__(self, max_turns: int = 5):
        
        self.max_turns = max_turns

        self.history: List[Dict[str, str]] = []

    def add_turn(
        self,
        user_message: str,
        assistant_message: str,
    ) -> None:
        self.history.append(
            {
                "user": user_message,
                "assistant": assistant_message,
            }
        )
        if len(self.history) > self.max_turns:

            self.history = self.history[
                -self.max_turns:
            ]

    def get_history(self) -> List[Dict[str, str]]:
        
        return self.history.copy()

    def get_formatted_history(self) -> str:

        if not self.history:
            return "No previous conversation."

        formatted = []

        for index, turn in enumerate(
            self.history,
            start=1,
        ):

            formatted.append(
                f"""
Conversation Turn {index}

User:
{turn["user"]}

Assistant:
{turn["assistant"]}
""".strip()
            )

        return "\n\n".join(formatted)

    def clear(self) -> None:
        """
        Clear all conversation history.
        """

        self.history.clear()

    def size(self) -> int:
        """
        Return number of stored conversation turns.
        """

        return len(self.history)


def main():

    print("=" * 60)
    print("CONVERSATION MEMORY TEST")
    print("=" * 60)

    memory = ConversationMemory(
        max_turns=3
    )

    memory.add_turn(
        "What is karma?",
        "Karma refers to action and its consequences.",
    )

    memory.add_turn(
        "Who teaches Arjuna?",
        "Krishna teaches Arjuna.",
    )

    memory.add_turn(
        "Why is duty important?",
        "The Gita emphasizes performing one's duty.",
    )


    print(
        f"\nMemory size: {memory.size()}"
    )

    print("\nConversation history:")
    print("-" * 60)

    print(
        memory.get_formatted_history()
    )

    print("-" * 60)

    memory.add_turn(
        "What is dharma?",
        "Dharma refers to one's duty and righteous conduct.",
    )

    print(
        f"\nMemory size after adding another turn: "
        f"{memory.size()}"
    )

    print(
        "\nThe oldest conversation turn is automatically "
        "removed when max_turns is exceeded."
    )

    memory.clear()

    print(
        f"\nMemory size after clear: "
        f"{memory.size()}"
    )

    print("=" * 60)


if __name__ == "__main__":
    main()