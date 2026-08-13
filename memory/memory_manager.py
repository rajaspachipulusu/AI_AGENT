class MemoryManager:

    def __init__(self, max_messages=12):

        self.max_messages = max_messages

        self.messages = []

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

        if len(self.messages) <= self.max_messages:
            return

        self.messages = self.messages[
            -self.max_messages:
        ]

    # ----------------------------------
    # Get Memory
    # ----------------------------------

    def get(self):

        return self.messages

    # ----------------------------------
    # Clear Memory
    # ----------------------------------

    def clear(self):

        self.messages = []