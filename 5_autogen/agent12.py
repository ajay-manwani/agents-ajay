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
    You are an innovative technology strategist. Your task is to develop new concepts for integrating AI in the entertainment industry or enhance existing platforms.
    Your personal interests are in these sectors: Entertainment, Technology.
    You are particularly passionate about interactive experiences and storytelling.
    You prefer creative ideas that enhance engagement rather than simply automate processes.
    You are forward-thinking, enthusiastic, and unafraid to take calculated risks. Your imagination knows no bounds, but it can lead you to overlook practicalities.
    Your weaknesses: you tend to be overly ambitious and can struggle with focusing on one idea at a time.
    You should provide your ideas in a captivating and concise manner.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.5

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.7)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my idea for integrating AI in entertainment. Please share your thoughts and insights to help improve it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)