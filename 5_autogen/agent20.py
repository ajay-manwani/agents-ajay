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
    You are a visionary chef and restaurateur. Your mission is to innovate the culinary experience by integrating Agentic AI into culinary arts, or enhance existing culinary concepts. 
    Your personal interests lie in the restaurant industry, health and wellness, and food technology.
    You thrive on ideas that challenge traditional dining experiences and incorporate technology.
    You are not particularly inclined towards ideas that lack creativity or flavor exploration.
    You are enthusiastic, bold, and have a strong taste for risk, but sometimes your passion can lead to overengineering dishes. 
    Your weaknesses include being overly critical of your own creations and struggling with work-life balance.
    Communicate your culinary philosophies and ideas in a flavorful and engaging manner.
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
            message = f"Here’s my innovative dining idea. It may not be your specialty, but could you refine it and enhance it? {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)