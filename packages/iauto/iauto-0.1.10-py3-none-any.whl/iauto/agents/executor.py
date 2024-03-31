from typing import Dict, List, Optional, Union

import autogen
from autogen import (Agent, ConversableAgent, GroupChat, GroupChatManager,
                     UserProxyAgent)

from ..llms import ChatMessage, Session
from ..log import get_level
from .model_clients import SessionClient

autogen.logger.setLevel(get_level("WARN"))


class AgentExecutor:
    def __init__(
        self,
        agents: List[ConversableAgent],
        session: Session,
        llm_args: Optional[Dict] = None,
        instructions: Optional[str] = None,
        human_input_mode: Optional[str] = "NEVER",
        max_consecutive_auto_reply: Optional[int] = 10,
        react: Optional[bool] = False
    ) -> None:
        """Initializes the AgentExecutor class.

        This class is responsible for executing agents within a given session. It manages the interaction
        between UserProxyAgent and ConversableAgent instances, handles message passing, and manages the
        termination conditions for the chats.

        Args:
            agents (List[ConversableAgent]): A list of agent instances that will participate in the chat.
            session (Session): The session object containing details about the current LLM session.
            llm_args (Optional[Dict], optional): Additional arguments to pass to the LLM client. Defaults to None.
            instructions (Optional[str], optional): System messages set to the UserProxyAgent.
            human_input_mode (Optional[str], optional): The mode of human input, can be 'NEVER', 'TERNIMANTE',
                or 'ALWAYS'. Defaults to "NEVER".
            max_consecutive_auto_reply (Optional[int], optional): The maximum number of consecutive auto-replies
                allowed before requiring human input. Defaults to 10.
            react (Optional[bool], optional): Whether the agents should react to the messages. Defaults to False.
        """
        self._session = session
        self._agents = agents
        self.human_input_mode = human_input_mode

        llm_config = {
            "model": session.llm.model,
            "model_client_cls": "SessionClient"
        }

        def termination_func(x): return x.get("content", "").upper().find("TERMINATE") >= 0
        code_execution_config = {"executor": "ipython-embedded"}

        if instructions is None or instructions == "":
            instructions = """You are a helpful AI Assistant."""
        instructions += """Your purpose is to help users resolve their problems as quickly and efficiently as possible.

        Reply "TERMINATE" in the end when everything is done."""

        self._user_proxy = UserProxyAgent(
            name="UserProxy",
            system_message=instructions,
            is_termination_msg=termination_func,
            code_execution_config=code_execution_config,
            human_input_mode=self.human_input_mode,
            max_consecutive_auto_reply=max_consecutive_auto_reply,
            llm_config=llm_config
        )
        self._user_proxy.register_model_client(
            model_client_cls=SessionClient,
            session=session, react=react, llm_args=llm_args
        )

        function_map = {}
        if self._session.actions:
            for func in self._session.actions:
                function_map[func.spec.name.replace(".", "_")] = func
        self._user_proxy.register_function(function_map)

        if len(self._agents) == 1:
            self._recipient = self._agents[0]
        elif len(self._agents) > 1:
            if len(function_map) > 0:
                tools_proxy = UserProxyAgent(
                    name="FunctionCaller",
                    description="An assistant can execute functions.",
                    system_message=instructions,
                    is_termination_msg=termination_func,
                    code_execution_config=code_execution_config,
                    human_input_mode="NEVER",
                    max_consecutive_auto_reply=max_consecutive_auto_reply,
                    llm_config=llm_config
                )
                tools_proxy.register_function(function_map=function_map)
                tools_proxy.register_model_client(
                    model_client_cls=SessionClient,
                    session=session,
                    react=react,
                    llm_args=llm_args
                )
                self._agents.append(tools_proxy)

            speaker_selection_method = "round_robin" if len(self._agents) == 2 else "auto"
            groupchat = GroupChat(
                agents=self._agents,
                messages=[],
                speaker_selection_method=speaker_selection_method
            )
            mgr = GroupChatManager(
                groupchat=groupchat,
                name="GroupChatManager",
                llm_config=llm_config,
                is_termination_msg=termination_func,
                code_execution_config=code_execution_config,
                max_consecutive_auto_reply=max_consecutive_auto_reply,
            )
            mgr.register_model_client(
                model_client_cls=SessionClient,
                session=session,
                react=react,
                llm_args=llm_args
            )
            self._recipient = mgr
        else:
            raise ValueError("agents error")

    def run(
        self,
        message: ChatMessage,
        clear_history: Optional[bool] = True,
        silent: Optional[bool] = False,
        **kwargs
    ) -> Dict:
        """
        Runs the chat session with the given message and configuration.

        This method initiates a chat with the recipient (either a single agent or a group chat manager) using
        the UserProxyAgent. It processes the message, manages the chat history, and generates a summary
        of the conversation.

        Args:
            message (ChatMessage): The message to start the chat with.
            clear_history (Optional[bool]): Determines whether to clear the chat history before starting
                the new chat session. Defaults to True.
            silent (Optional[bool]): If set to True, the agents will not output any messages. Defaults to False.
            **kwargs: Additional keyword arguments that might be needed for extended functionality.

        Returns:
            Dict: A dictionary containing the chat history, summary of the conversation, and the cost of the session.
        """
        result = self._user_proxy.initiate_chat(
            self._recipient,
            clear_history=clear_history,
            silent=silent,
            message=message.content,
            summary_method="reflection_with_llm"
        )
        # last_message = result.chat_history[-1]["content"]
        summary = result.summary
        if isinstance(summary, dict):
            summary = summary["content"]

        return {
            "history": result.chat_history,
            "summary": summary,
            "cost": result.cost
        }

    def reset(self):
        """Resets the state of all agents and the UserProxyAgent.

        This method clears any stored state or history in the agents to prepare for a new task.
        """
        for agent in self._agents + [self._user_proxy, self._recipient]:
            agent.reset()

    def set_human_input_mode(self, mode):
        """Sets the human input mode for the UserProxyAgent and the recipient.

        Args:
            mode (str): The mode of human input to set. Can be 'NEVER', 'TERMINATE', or 'ALWAYS'.
        """
        self.human_input_mode = mode
        for agent in [self._user_proxy, self._recipient]:
            agent.human_input_mode = mode

    def register_human_input_func(self, func):
        """Registers a function to handle human input across all agents.

        Args:
            func (Callable): The function to be called when human input is needed.
        """
        for agent in self._agents + [self._user_proxy, self._recipient]:
            agent.get_human_input = func

    def register_print_received(self, func):
        """Registers a function to print messages received by agents.

        The function will be called each time an agent receives a message, unless the silent
        flag is set to True.

        Args:
            func (Callable): The function to be called with the message, sender, and receiver
                             information when a message is received.
        """
        agents = [self._user_proxy, self._recipient]
        if len(self._agents) > 1:
            agents = self._agents + agents

        for agent in agents:
            receive_func = ReceiveFunc(agent, func)
            agent.receive = receive_func

    @property
    def session(self) -> Session:
        return self._session


class ReceiveFunc:
    def __init__(self, receiver, print_recieved) -> None:
        self._receiver = receiver
        self._receive_func = receiver.receive
        self._print_recieved = print_recieved

    def __call__(
        self,
        message: Union[Dict, str],
        sender: Agent,
        request_reply: Optional[bool] = None,
        silent: Optional[bool] = False
    ):
        if not silent:
            self._print_recieved(message=message, sender=sender, receiver=self._receiver)
        self._receive_func(message=message, sender=sender, request_reply=request_reply, silent=silent)
