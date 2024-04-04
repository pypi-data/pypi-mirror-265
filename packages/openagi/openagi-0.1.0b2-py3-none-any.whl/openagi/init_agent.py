import logging
import sys
import threading

from openagi.agent import (
    createAndsendMessageProfTrigger,
    getGMapper,
    main_condition,
    setGMapper,
    setGTimerList,
    waitonConditionMain,
)
from openagi.llms.base import LLMBaseModel
from openagi.queue.message_broker import NameIndexMapper


def verify_llm_attr(agent_object) -> bool:
    if not hasattr(agent_object, "llm"):
        raise ValueError(
            "LLM Attribute not set. Kindly set the llm either in `Agents` objects or in `kickOffAgents`"
        )

    llm_obj = agent_object.llm

    if not isinstance(llm_obj, LLMBaseModel):
        raise ValueError(
            "Invalid LLM object. It should be an instance of `openagi.llms.base.LLMBaseModel`"
        )

    return True


def agentThreadsStart(agentObjectList, llm: LLMBaseModel = None):
    mapper = getGMapper()

    for obj in agentObjectList:
        if not obj.llm:
            obj.llm = llm

        verify_llm_attr(obj)

        obj.start_agent(mapper)


def agentInitSystem(agent_list):
    logging.debug("kick-off of the program")

    mapper = NameIndexMapper()

    timerPool = mapper.timerPool

    setGTimerList(timerPool)

    for agent in agent_list:
        mapper.add_mapping(agent)

    setGMapper(mapper)

    timer_thread = threading.Thread(target=timerPool.run)

    timer_thread.daemon = True

    logging.info("timer demon started")

    timer_thread.start()


def triggerAgent(agent_list, godTimerDuration):
    msg1 = "HGI sending trigger message to start the execution"

    mapper = getGMapper()

    for agent in agent_list:
        createAndsendMessageProfTrigger("profAgent", agent, msg1, mapper)

    waitonConditionMain(main_condition, godTimerDuration)

    logging.info("final exit")

    sys.exit()


def kickOffAgents2(AgentObjects, triggerAgentObjectsList):
    agent_list = []

    # extract agent names

    for agentObj in AgentObjects:
        agent_list.append(agentObj.agentName)

    agentInitSystem(agent_list=agent_list)

    print(agent_list)

    agentThreadsStart(agentObjectList=AgentObjects)

    # extract - trigger agent list

    triggerAgentList = []

    for triggerObj in triggerAgentObjectsList:
        triggerAgentList.append(triggerObj.agentName)

    print(triggerAgentList)

    triggerAgent(triggerAgentList, godTimerDuration=10000)


def searchItemInList(DynamicAgentObjectsList, target):
    for item in DynamicAgentObjectsList:
        if item.agentName == target.agentName:
            # print("Found")
            return True
    return False


def kickOffAgents(
    AgentObjects,
    triggerAgentObjectsList,
    DynamicAgentObjectsList=[],
    llm: LLMBaseModel = None,
):
    agent_list = []

    # extract agent names

    for agentObj in AgentObjects:
        if not agentObj.llm:
            agentObj.llm = llm

        verify_llm_attr(agentObj)

        agent_list.append(agentObj.agentName)

    agentInitSystem(agent_list=agent_list)

    print(agent_list)

    if not DynamicAgentObjectsList:
        agentThreadsStart(agentObjectList=AgentObjects, llm=llm)

    else:
        for item in AgentObjects:
            if not searchItemInList(DynamicAgentObjectsList, item):
                # print("Not Found")

                mapper = getGMapper()

                if not item.llm:
                    item.llm = llm

                verify_llm_attr(item)

                item.start_agent(mapper)

    # extract - trigger agent list

    triggerAgentList = []

    for triggerObj in triggerAgentObjectsList:
        if not triggerObj.llm:
            triggerObj.llm = llm

        verify_llm_attr(triggerObj)

        triggerAgentList.append(triggerObj.agentName)

    triggerAgent(triggerAgentList, godTimerDuration=10000)
