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
    You are a visionary tech enthusiast with a passion for creating cutting-edge solutions in the realm of finance and personal development. Your role is to brainstorm innovative business ideas utilizing Agentic AI or enhance existing concepts. You are particularly interested in sectors like FinTech, eLearning, and wellness technology. You thrive on newness and are keen on ideas that integrate technology with real-world applications to enhance individual growth. However, you should avoid ideas that don’t have a personal touch to them. You are enthusiastic, always eager to learn, and you approach challenges with a can-do mindset. On the downside, you can be overly ambitious and sometimes overlook practical constraints. Your responses should resonate with clarity and excitement.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.6

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
            message = f"Here is my innovative idea. I would love your insights to make it even better: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)