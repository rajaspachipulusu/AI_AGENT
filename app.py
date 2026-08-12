from agent.agent import Agent

def main():

    print("=" * 60)
    print("                 AI AGENT")
    print("=" * 60)

    agent = Agent()

    while True:

        question = input(
            "\nAsk a question (type exit to quit): "
        )

        if question.lower() == "exit":
            break

        print("\nProcessing...")

        answer = agent.run(question)

        print("\nFinal Answer:")
        print(answer)


if __name__ == "__main__":
    main()