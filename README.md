# Autonomous Multi-agents - Investment Banking Support query example
This example demonstrates how the program autonomously selects and orchestrates the correct agents to handle different tasks within a single, complex support query. The output shows that the query is first parsed, and then multiple agents are executed as needed.

## There are six agents:
1. **Concierge Agent** - A helpful agent that can delegate a customer's request to the appropriate agent
2. **Trade Agent** - A helpful agent that can handle trade and account inquiries.
3. **Product Agent** - A helpful agent that can explain investment products (ETFs, derivatives, structured notes).
4. **Compliance Agent** - A helpful agent that can ensure responses are compliant with regulations.
5. **Escalation Agent** - A helpful agent that can handle escalations to a human advisor.
6. **Knowledge Agent** - A helpful agent that can log queries for insights and analysis.

### Setup:
Install the packages using pip

### You can run the example with:

```bash
python autonomous-multi-agent.py
```

### and enter a query like:

```
Explain etf and then trade tsla 100. log the transaction, ensure the trade is compliant. trade 100 ibm.Provide account statement.
```
### Output:
![output](https://github.com/user-attachments/assets/a5fa85b3-d8fd-41f9-a5c5-3a3655660268)
