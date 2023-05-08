import argparse
from environs import Env
from google.cloud import dialogflow
import json
from tqdm import tqdm


def create_intent(project_id, display_name, training_phrases_parts, message_texts):
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()
    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        # Here we create a new training phrase for each provided part.
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(display_name=display_name, training_phrases=training_phrases, messages=[message])

    response = intents_client.create_intent(request={"parent": parent, "intent": intent})
    return response


if __name__ == '__main__':
    env = Env()
    env.read_env()
    google_cloud_project = env('GOOGLE_CLOUD_PROJECT')

    parser = argparse.ArgumentParser(description='Скрипт для заливки в проект dialogflow интентов через API')
    parser.add_argument("intents_file", help='name of file.json with intents in the folder of script')
    args = parser.parse_args()
    intents_file = args.intents_file

    with open(intents_file, "r", encoding='utf-8') as questions_file:
        questions_json = questions_file.read()
    questions = json.loads(questions_json)
    for intent, question in tqdm(questions.items()):
        response = create_intent(google_cloud_project, intent, question['questions'], [question['answer']])
        print(f"Intent created: {response}")
