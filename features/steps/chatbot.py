from behave.api.pending_step import StepNotImplementedError

from globebotter.rag import graph

@given(u'a session with the chatbot')
def step_impl(context):
    context.chatbot = graph


@when(u'a user asks the chatbot to recommend three sights in Rome')
def step_impl(context):
    context.chatbot.invoke({"messages": "what is the square root of 10?"}, config = {"configurable": {"thread_id": "abc123"}})


@then(u'the response should be similar to "1. The Colosseum 2. Vatican City 3. Trevi Fountain"')
def step_impl(context):
    raise StepNotImplementedError(u'Then the response should be similar to "1. The Colosseum 2. Vatican City 3. Trevi Fountain"')


@then(u'the response should be less similar to')
def step_impl(context):
    raise StepNotImplementedError(u'Then the response should be less similar to')

