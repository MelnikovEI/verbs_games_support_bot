from google.cloud import dialogflow
from google.cloud.dialogflow_v2 import DetectIntentResponse


def detect_intent(project_id, session_id, text, language_code) -> DetectIntentResponse:
    """Returns the result of detect intent with texts as inputs.
    Using the same `session_id` between requests allows continuation of the conversation."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    return response


if __name__ == '__main__':
    print(detect_intent('verbs-games-support2-vyfg', 1, 'Хай', 'ru'))
