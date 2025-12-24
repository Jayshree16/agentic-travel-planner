from agent.travel_agent import create_travel_agent

def main():
    agent = create_travel_agent()   # ✅ NO ARGUMENTS

    response = agent.invoke({
        "messages": [
            ("human", "Plan a 3-day budget trip to Goa from Hyderabad")
        ]
    })

    print("\n===== Travel Plan =====\n")
    print(response["messages"][-1].content)


if __name__ == "__main__":
    main()
