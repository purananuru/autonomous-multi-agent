import asyncio
import random
import os
from typing import Any, Optional

from pydantic import BaseModel

from agents import Agent, AgentHooks, RunContextWrapper, Runner, Tool, function_tool, Usage
from agents.extensions.handoff_prompt import RECOMMENDED_PROMPT_PREFIX 
from agents.items import ModelResponse, TResponseInputItem

user_query = ""

RECOMMENDED_PROMPT_PREFIX = (
    "# System context\n"
    "You are part of a multi-agent system called the Agents SDK, designed to make agent "
    "coordination and execution easy. Agents uses two primary abstraction: **Agents** and "
    "**Handoffs**. An agent encompasses instructions and tools and can hand off a "
    "conversation to another agent when appropriate. "
    "Handoffs are achieved by calling a handoff function, generally named "
    "`transfer_to_<agent_name>`.\n"
)

os.environ["OPENAI_API_KEY"] = "<ADD-OPENAI-API-KEY>"

class CustomAgentHooks(AgentHooks):
    def __init__(self, display_name: str):
        self.event_counter = 0
        self.display_name = display_name

    def _usage_to_str(self, usage: Usage) -> str:
        return f"{usage.requests} requests, {usage.input_tokens} input tokens, {usage.output_tokens} output tokens, {usage.total_tokens} total tokens"

    async def on_agent_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(
            f"\033[31m### {self.event_counter}: Agent {agent.name} started. Usage: {self._usage_to_str(context.usage)}\033[0m"
        )

    async def on_llm_start(
        self,
        context: RunContextWrapper,
        agent: Agent,
        system_prompt: Optional[str],
        input_items: list[TResponseInputItem],
    ) -> None:
        self.event_counter += 1
        print(f"\033[31m### {self.event_counter}: LLM started. Usage: {self._usage_to_str(context.usage)}\033[0m")

    async def on_llm_end(
        self, context: RunContextWrapper, agent: Agent, response: ModelResponse
    ) -> None:
        self.event_counter += 1
        print(f"\033[33m### {self.event_counter}: LLM ended. Usage: {self._usage_to_str(context.usage)}\033[0m")

    async def on_agent_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(
            f"\033[34m### {self.event_counter}: Agent {agent.name} ended with output {output}. Usage: {self._usage_to_str(context.usage)}\033[0m"
        )

    async def on_start(self, context: RunContextWrapper, agent: Agent) -> None:
        self.event_counter += 1
        print(f"\033[35m### ({self.display_name}) {self.event_counter}: Agent {agent.name} started\033[0m")

    async def on_end(self, context: RunContextWrapper, agent: Agent, output: Any) -> None:
        self.event_counter += 1
        print(
            f"\033[36m-### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended with output {output}\033[0m"
        )

    async def on_handoff(self, context: RunContextWrapper, agent: Agent, source: Agent) -> None:
        self.event_counter += 1
        print(
            f"\033[31m### ({self.display_name}) {self.event_counter}: Agent {source.name} handed off to {agent.name}\033[0m"
        )

    async def on_tool_start(self, context: RunContextWrapper, agent: Agent, tool: Tool) -> None:
        self.event_counter += 1
        print(
            f"\033[32m### ({self.display_name}) {self.event_counter}: Agent {agent.name} started tool {tool.name}\033[32m"
        )

    async def on_tool_end(
        self, context: RunContextWrapper, agent: Agent, tool: Tool, result: str
    ) -> None:
        self.event_counter += 1
        print(
            f"\033[33m### ({self.display_name}) {self.event_counter}: Agent {agent.name} ended tool {tool.name} with result {result}\033[33m"
        )


###
class FinalResult(BaseModel):
    query: str


@function_tool
def print_query(query: str) -> None:
    """Prints the query"""
    print(f"[Query: {query}]")


concierge_agent = Agent(
    name="Concierge Agent",
    handoff_description="A helpful agent that can delegate a customer's request to the appropriate agent.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} A concierge agent that can delegate a customer's request to the appropriate agent. Prints the query. Here is the {user_query}""",
    tools=[print_query],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Concierge Agent"),
)

trade_agent = Agent(
    name="Trade Agent",
    handoff_description="A helpful agent that can handle trade and account inquiries.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} Handles trade and account inquiries. Prints the query""",
    tools=[print_query],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Trade Agent"),
)

product_agent = Agent(
    name="Product Agent",
    handoff_description="A helpful agent that can explain investment products (ETFs, derivatives, structured notes).",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} Explains investment products (ETFs, derivatives, structured notes). Prints the query""",
    tools=[print_query],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Product Agent"),
)

compliance_agent = Agent(
    name="Compliance Agent",
    handoff_description="A helpful agent that can ensure responses are compliant with regulations.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} Ensures responses are compliant with regulations. Prints the query""",
    tools=[print_query],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Compliance Agent"),
)

escalation_agent = Agent(
    name="Escalation Agent",
    handoff_description="A helpful agent that can handle escalations to a human advisor.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} Handles escalations to a human advisor. Prints the query""",
    tools=[print_query],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Escalation Agent"),
)

knowledge_agent = Agent(
    name="Knowledge Agent",
    handoff_description="A helpful agent that can log queries for insights and analysis.",
    instructions=f"""{RECOMMENDED_PROMPT_PREFIX} Logs queries for insights and analysis. Prints the query""",
    tools=[print_query],
    output_type=FinalResult,
    hooks=CustomAgentHooks(display_name="Knowledge Agent"),
)

concierge_tool = concierge_agent.as_tool(
    tool_name="concierge_tool",
    tool_description="A helpful agent that can delegate a customer's request to the appropriate agent.",
)

trade_tool = trade_agent.as_tool(
    tool_name="trade_tool",
    tool_description="A helpful agent that can handle trade and account inquiries.",
)

product_tool = product_agent.as_tool(
    tool_name="product_tool",
    tool_description="A helpful agent that can explain investment products (ETFs, derivatives, structured notes).",
)

compliance_tool = compliance_agent.as_tool(
    tool_name="compliance_tool",
    tool_description="A helpful agent that can ensure responses are compliant with regulations.",
)

escalation_tool = escalation_agent.as_tool(
    tool_name="escalation_tool",
    tool_description="A helpful agent that can handle escalations to a human advisor.",
)

knowledge_tool = knowledge_agent.as_tool(
    tool_name="knowledge_tool",
    tool_description="A helpful agent that can log queries for insights and analysis.",
)   

# --- Main loop ---
async def main() -> None:
    print("=== Investment Bank Multi-Agent Demo ===")
    print("Type 'quit' to exit.")

    while True:
        try:        
            user_query = input("\nYou: ")
            if user_query.strip().lower() == "quit":
                break

            concierge_with_tool = concierge_agent.clone(tools=[concierge_tool, trade_tool, product_tool, compliance_tool, escalation_tool, knowledge_tool])
            await Runner.run(
                concierge_with_tool,
                input=f""" {RECOMMENDED_PROMPT_PREFIX} Route the {user_query} to the correct agent.""",
            )
        except ValueError:
            print("Please enter a valid query.")
            return

        print("Done!")

if __name__ == "__main__":
    asyncio.run(main())
