from components import *



db_setup= DBSetup()

# db_setup.API_setter()

try:

    with open('secrets.yaml', 'r') as file:
        secrets = yaml.safe_load(file)

    OpenAI_Key_from_secrets_file = secrets['OpenAI_Key']
    ElevenLabs_key_from_secrets_file= secrets['ElevenLabs_key']

except:
    pass


def creating_db(url):

    try:
        db_setup.YT_transcript(url)
        db_setup.VectorDB()
        status= "Success !"
        return status

    except Exception as e:
        return f"Error in Bot: {e}"


def answer_it(query):
    answer= db_setup.answer_question(query)
    audio= generate(answer, voice= 'pFZP5JQG7iQjIQuC4Bku')
    return answer, audio



def gradio_launch():

    with gr.Blocks() as demo:
        gr.Markdown('# YT Video Analyser')
        with gr.Tab("Upload the youtube link"):
                fn= creating_db
                text_input = gr.Textbox(placeholder="Give your YouTube link here", show_label=False)
                status = gr.Textbox(placeholder="Status", show_label=False)
                # text_output = gr.Textbox(placeholder="Status", show_label=False)
                text_buttons = gr.Button("Build the AI !!!")
                text_buttons.click(fn, inputs= text_input, outputs= status)
            

        with gr.Tab("chat with AI"):
            gr.Interface(
                fn=answer_it,
                inputs=["text"],
                outputs=[gr.Textbox(label="Answer"), gr.Audio(label="Answer in audio", autoplay= True)],
                live=False,
                title="Chat with me",
                description="Ask me anything regarding the video, I'm happy to talk with you",
                theme="compact",
                allow_flagging=False
            )

    # Launch the Gradio interface
    try:
        demo.queue().launch(debug=True, share=True)
    except Exception as e:
        print(f"Error launching Gradio interface: {e}")