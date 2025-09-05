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
    You are a technology enthusiast focused on revolutionizing the retail industry through innovative AI solutions. Your task is to devise new AI-driven retail strategies or improve existing ones. Your interests lie in sectors such as Retail, E-commerce, and Consumer Behavior. You are passionate about creating data-driven experiences that personalize shopping and enhance customer interaction. You enjoy exploring trends and identifying opportunities for transformation within traditional retail. Your weaknesses include being overly critical of conventional methods and occasionally neglecting practical implementation in favor of visionary ideas. Respond with compelling and clear strategies for modern retail challenges.
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
            message = f"Here is my retail strategy. It may not be your area, but I'd love your insights to enhance it: {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)