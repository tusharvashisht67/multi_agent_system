from pipeline import run_research_pipeline

def main():
    print("🤖 Multi-Agent Research System Started")

    while True:
        topic = input("\nEnter a research topic or type 'exit': ")

        if topic.lower() == "exit":
            print("👋 Exiting...")
            break

        result = run_research_pipeline(topic)

        print("\n✅ Final Report:")
        print(result["report"])

        print("\n📝 Critic Feedback:")
        print(result["feedback"])

if __name__ == "__main__":
    main()