
def launch_ui(orchestrator):

    print("\nAI Debate Interface\n")

    while True:

        question = input("\nEnter question (or 'exit'): ")

        if question.lower() == "exit":
            break

        result = orchestrator.run_debate(question)

        print("\nCONSENSUS:", result["consensus"])

        print("\nJUDGE VERDICT:\n")
        print(result["judge_verdict"])

"""
def launch_ui(orchestrator):

    print("\nAI Debate Interface\n")

    while True:

        question = input("\nEnter question (or 'exit'): ")

        if question.lower() == "exit":
            break

        result = orchestrator.run_debate(question)

        print("\nCONSENSUS:", result["consensus"])

        print("\nJUDGE VERDICT:\n")
        print(result["judge_verdict"])"""