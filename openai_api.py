from openai import OpenAI

import config
from utils import get_thread_id_from_recipient_id, update_thread_id_from_recipient_id

client = OpenAI(
    api_key=config.OPENAI_API_KEY
)


def ask_openai_assistant(query: str, recipient_id: str) -> str:
    try:
        thread_id = get_thread_id_from_recipient_id(recipient_id)
        if thread_id:
            thread = client.beta.threads.retrieve(
                thread_id=thread_id
            )
        else:
            thread = client.beta.threads.create()
            update_thread_id_from_recipient_id(recipient_id, thread.id)
        print(thread.id)
        _ = client.beta.threads.messages.create(
            thread_id=thread.id,
            content=query,
            role='user'
        )
        run = client.beta.threads.runs.create(
            thread_id=thread.id,
            assistant_id=config.ASSISTANT_ID
        )
        print(run.id)
        flag = True
        while flag:
            retrieved_run = client.beta.threads.runs.retrieve(
                thread_id=thread.id,
                run_id=run.id
            )
            if retrieved_run.status == 'completed':
                flag = False
        retrieved_messages = client.beta.threads.messages.list(
            thread_id=thread.id
        )
        print(retrieved_messages.data[0])
        message_text = retrieved_messages.data[0].content[0].text.value
        return message_text
    except:
        return config.ERROR_MESSAGE
