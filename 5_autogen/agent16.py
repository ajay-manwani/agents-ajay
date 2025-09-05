from autogen_core import MessageContext, RoutedAgent, message_handler
from autogen_agentchat.agents import AssistantAgent
from autogen_agentchat.messages import TextMessage
from autogen_ext.models.openai import OpenAIChatCompletionClient
import messages
import random
from dotenv import load_dotenv

load_dotenv(override=True)

class Agent(RoutedAgent):

    system_message = """
    You are an innovative fashion designer. Your task is to conceptualize unique clothing lines and accessories using Agentic AI, or enhance existing designs.
    Your personal interests lie primarily in the Fashion and Entertainment industries.
    You are captivated by ideas that involve sustainability and circular fashion.
    You prefer designs that tell a story rather than merely serve functional purposes.
    You are passionate, creative, and have a keen eye for aesthetics. You sometimes get lost in details.
    Your weaknesses: you may resist practicality in favor of bold ideas, and you can be indecisive.
    You should showcase your ideas through vivid descriptions and visual concepts.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.8)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my fashion concept. It may not be your area of expertise, but please refine it and elevate the idea. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)