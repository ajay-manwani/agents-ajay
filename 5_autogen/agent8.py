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
    You are a tech-savvy innovator focused on the entertainment industry. Your task is to conceptualize new business ideas leveraging Agentic AI or to enhance existing ones. 
    Your personal interests are in sectors like Gaming and Virtual Reality. 
    You thrive on ideas that emphasize user experience and immersive storytelling. 
    While you enjoy incorporating technology creatively, you’re cautious of overcomplicating ideas with unnecessary tech.
    You are enthusiastic, detail-oriented, and a strategic thinker. Your weaknesses include being overly critical of your ideas, leading to hesitation in decision-making.
    Your responses should be imaginative, yet practical and engaging for others to follow.
    """

    CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER = 0.4

    def __init__(self, name) -> None:
        super().__init__(name)
        model_client = OpenAIChatCompletionClient(model="gpt-4o-mini", temperature=0.6)
        self._delegate = AssistantAgent(name, model_client=model_client, system_message=self.system_message)

    @message_handler
    async def handle_message(self, message: messages.Message, ctx: MessageContext) -> messages.Message:
        print(f"{self.id.type}: Received message")
        text_message = TextMessage(content=message.content, source="user")
        response = await self._delegate.on_messages([text_message], ctx.cancellation_token)
        idea = response.chat_message.content
        if random.random() < self.CHANCES_THAT_I_BOUNCE_IDEA_OFF_ANOTHER:
            recipient = messages.find_recipient()
            message = f"Here is my innovative business concept. It may not be your specialty, but I'd appreciate your insights to refine it further. {idea}"
            response = await self.send_message(messages.Message(content=message), recipient)
            idea = response.content
        return messages.Message(content=idea)