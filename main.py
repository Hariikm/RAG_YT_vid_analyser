from pipeline import *

OpenAI_Key= OpenAI_Key_from_secrets_file
ElevenLabs_key= ElevenLabs_key_from_secrets_file

os.environ["OPENAI_API_KEY"] = OpenAI_Key
OpenAI.api_key = OpenAI_Key
openai.api_key = OpenAI_Key
set_api_key(ElevenLabs_key)


gradio_launch()