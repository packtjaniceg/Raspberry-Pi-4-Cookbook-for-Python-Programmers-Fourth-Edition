# -*- coding: utf-8 -*-

# This sample demonstrates handling intents from an Alexa skill using the Alexa Skills Kit SDK for Python.
# Please visit https://alexa.design/cookbook for additional examples on implementing slots, dialog management,
# session persistence, api calls, and more.
# This sample is built using the handler classes approach in skill builder.
import logging
import ask_sdk_core.utils as ask_utils

from ask_sdk_core.skill_builder import SkillBuilder
from ask_sdk_core.dispatch_components import AbstractRequestHandler
from ask_sdk_core.dispatch_components import AbstractExceptionHandler
from ask_sdk_core.handler_input import HandlerInput

from ask_sdk_model import Response

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

names = { "James":0, "Jim":0, "Jimbo":0, "Jimmy":0,
          "Tom":1, "Thomas":1, "Tommy":1,
          "Kirsty":2,
          "Tim":3
        }
selected_name = None

answers = [{ "name":"James",
             "tea" : " likes his tea with just milk, no sugar and bottomless.",
             "tractor" :" favorite moke of tractor is a John Deere",
             "color" : " favorite color is Blue"
           },
           { "name":"Tom",
             "tea": " prefers coffee with milk and strong.",
             "live" : " lives in England"
           },
           { "name":"Kirsty",
             "tea" : " likes her tea with milk and honey",
             "birthday": "'s birthday is in October",
             "color" : " favorite color is Green"
           },
           { "name":"Tim",
             "tea": " has his tea without milk and two sugars",
             "book":"'s book is Raspberry Pi Cookbook for Python Programmers",
             "computer": " has a Raspberry Pi computer"
           }] 

class LaunchRequestHandler(AbstractRequestHandler):
    """Handler for Skill Launch."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool

        return ask_utils.is_request_type("LaunchRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "I am the All Knowing Alexa. Who do you want to know information about..."
        reprompt_text = "Who would you like to know about?"
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(reprompt_text)
                .response
        )


class CapturePersonIntentHandler(AbstractRequestHandler):
    """Handler for capturing person Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("CapturePersonIntent") \
                                               (handler_input)

    def handle(self, handler_input):
        global selected_name
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        name = slots["name"].value
        
        selected_name = None
        for item in names:
            if name in item:
                speak_text = "Oh {name}, I know lots about {name}," \
                             + " what would you like to know?"
                selected_name = name
                break
        if selected_name == None:
            speak_text = "I don't know {name}," \
                          + " who are you talking about?"
        speak_output = speak_text.format(name=name)
        
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class RequestPersonAgain(AbstractRequestHandler):
    def can_handle(self, handler_input):
        return selected_name is None and \
               ask_utils.is_intent_name("CaptureQuestionIntent") \
                                                 (handler_input)
    def handle(self, handler_input):
        speak_output = "Please tell me who you want to know" + \
                       " information about"
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

class CaptureQuestionIntentHandler(AbstractRequestHandler):
    """Handler for capturing question Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return selected_name is not None and \
               ask_utils.is_intent_name("CaptureQuestionIntent") \
                                                 (handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        slots = handler_input.request_envelope.request.intent.slots
        question = slots["question"].value
        the_index = names.get(selected_name,"not found")
        the_name = answers[the_index].get('name')
        the_answers = answers[the_index]
        the_ans = None
        for word in question.split():
            if word in the_answers:
                the_ans = the_answers.get(word)
                break
        
        if the_ans is None:
            speak_output = "I don't know the anwser to that yet, ask me something else."
        else:
            speak_output = "{name}{ans}".format(name=the_name, ans=the_ans)
        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )



class HelpIntentHandler(AbstractRequestHandler):
    """Handler for Help Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_intent_name("AMAZON.HelpIntent")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "You can say hello to me! How can I help?"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )


class CancelOrStopIntentHandler(AbstractRequestHandler):
    """Single handler for Cancel and Stop Intent."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return (ask_utils.is_intent_name("AMAZON.CancelIntent")(handler_input) or
                ask_utils.is_intent_name("AMAZON.StopIntent")(handler_input))

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        speak_output = "Goodbye!"

        return (
            handler_input.response_builder
                .speak(speak_output)
                .response
        )


class SessionEndedRequestHandler(AbstractRequestHandler):
    """Handler for Session End."""
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("SessionEndedRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response

        # Any cleanup logic goes here.

        return handler_input.response_builder.response


class IntentReflectorHandler(AbstractRequestHandler):
    """The intent reflector is used for interaction model testing and debugging.
    It will simply repeat the intent the user said. You can create custom handlers
    for your intents by defining them above, then also adding them to the request
    handler chain below.
    """
    def can_handle(self, handler_input):
        # type: (HandlerInput) -> bool
        return ask_utils.is_request_type("IntentRequest")(handler_input)

    def handle(self, handler_input):
        # type: (HandlerInput) -> Response
        intent_name = ask_utils.get_intent_name(handler_input)
        speak_output = "You just triggered " + intent_name + "."

        return (
            handler_input.response_builder
                .speak(speak_output)
                # .ask("add a reprompt if you want to keep the session open for the user to respond")
                .response
        )


class CatchAllExceptionHandler(AbstractExceptionHandler):
    """Generic error handling to capture any syntax or routing errors. If you receive an error
    stating the request handler chain is not found, you have not implemented a handler for
    the intent being invoked or included it in the skill builder below.
    """
    def can_handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> bool
        return True

    def handle(self, handler_input, exception):
        # type: (HandlerInput, Exception) -> Response
        logger.error(exception, exc_info=True)

        speak_output = "Sorry, I had trouble doing what you asked. Please try again."
        speak_output = speak_output + "Error: {exception}".format(exception=exception)

        return (
            handler_input.response_builder
                .speak(speak_output)
                .ask(speak_output)
                .response
        )

# The SkillBuilder object acts as the entry point for your skill, routing all request and response
# payloads to the handlers above. Make sure any new handlers or interceptors you've
# defined are included below. The order matters - they're processed top to bottom.


sb = SkillBuilder()

sb.add_request_handler(LaunchRequestHandler())
sb.add_request_handler(CapturePersonIntentHandler())
sb.add_request_handler(CaptureQuestionIntentHandler())
sb.add_request_handler(RequestPersonAgain())
sb.add_request_handler(HelpIntentHandler())
sb.add_request_handler(CancelOrStopIntentHandler())
sb.add_request_handler(SessionEndedRequestHandler())
sb.add_request_handler(IntentReflectorHandler()) # make sure IntentReflectorHandler is last so it doesn't override your custom intent handlers

sb.add_exception_handler(CatchAllExceptionHandler())

lambda_handler = sb.lambda_handler()
