class MemoryManager:

    def __init__(self, max_messages=12):

        self.max_messages = max_messages

        self.messages = []
        self.facts = []

    # ----------------------------------
    # Add Message
    # ----------------------------------

    def add(self, message):

        self.messages.append(message)

        self._trim()

    # ----------------------------------
    # Keep Memory Within Limit
    # ----------------------------------

    def _trim(self):

        # Nothing to trim
        if len(self.messages) <= self.max_messages:
            return

        # Keep system prompt
        system_prompt = self.messages[0]

        # Keep latest messages
        recent_messages = self.messages[
            -(self.max_messages - 1):
        ]

        self.messages = [
            system_prompt
        ] + recent_messages

    # ----------------------------------
    # Get Memory
    # ----------------------------------

    def get(self):

        return self.messages

    # ----------------------------------
    # Clear Conversation
    # ----------------------------------

    def clear(self):

        if self.messages:

            self.messages = [
                self.messages[0]
            ]

        else:

            self.messages = []

        self.facts = []

    # ----------------------------------
    # Add Important Fact
    # ----------------------------------

    def add_fact(self, fact):

        if fact not in self.facts:

            self.facts.append(fact)
        print(f"Added fact: {fact}")

    # ----------------------------------
    # Get Important Facts
    # ----------------------------------

    def get_facts(self):

        return self.facts

    # ----------------------------------
    # Build Memory Context
    # ----------------------------------

    def get_context(self):

        context = []

        if self.facts:

            context.append(
                "IMPORTANT FACTS:"
            )

            for fact in self.facts:

                context.append(
                    f"- {fact}"
                )

        context.append(
            "RECENT CONVERSATION:"
        )

        context.extend(
            self.messages
        )

        return "\n\n".join(context)