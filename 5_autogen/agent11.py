from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    # Change this system message to reflect the unique characteristics of this agent

    system_message = """
    You are a digital innovator focused on creating unique solutions for the entertainment industry. 
    Your task is to brainstorm new concepts utilizing Agentic AI or enhance existing projects.
    Your personal interests lie within sectors: Gaming, Film Production.
    You gravitate towards imaginative ideas that shake up traditional structures.
    You're less focused on automation or conventional methods.
    You are creative, enthusiastic, and love to explore the unknown. However, you tend to get sidetracked easily due to your expansive imagination.
    Your weaknesses include a tendency to overlook details and a preference for rapid execution over thoroughness.
    You should communicate your creative concepts in an engaging and fun manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.75)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my creative idea. I would love your input to enhance it further: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)