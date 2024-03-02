import os
from langchain.llms import OpenAI
import langchain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import TextLoader
from langchain_community.vectorstores import Chroma
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.chains.question_answering import load_qa_chain
import re
from youtube_transcript_api import YouTubeTranscriptApi
import openai
import gradio as gr
from elevenlabs import generate, play, set_api_key
import yaml


class DBSetup:

    def __init__(self):
        self.db= None
        self.chain= None
        self.vid_ID= None
        self.OpenAI_Key= None
        self.ElevenLabs_key= None

    # def API_setter(self):
    #     with open('secrets.yaml', 'r') as file:
    #         secrets = yaml.safe_load(file)

    #     self.OpenAI_Key = secrets['OpenAI_Key']
    #     self.ElevenLabs_key= secrets['ElevenLabs_key']
    #     os.environ["OPENAI_API_KEY"] = self.OpenAI_Key
    #     OpenAI.api_key = self.OpenAI_Key
    #     openai.api_key = self.OpenAI_Key
    #     set_api_key(self.ElevenLabs_key)

    def YT_transcript(self, url):

        def extract_video_id(url):
            pattern = re.compile(
                r'(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})')
            match = pattern.search(url)
            return match.group(1) if match else None

        try:
            video_id = extract_video_id(url)
            if video_id:
                transcript = YouTubeTranscriptApi.get_transcript(video_id)
                text_only = ' '.join(item['text'] for item in transcript)
                self.vid_ID = video_id
                with open(f'Data_folder\{video_id}.txt', 'w') as file:
                    file.write(text_only)
            
            else:
                print("Error: Unable to extract transcript from the URL.")
                return None
        except Exception as e:
            print(f"Error getting transcript: {e}")
            return None


    def VectorDB(self):
        loader = TextLoader(f"Data_folder\{self.vid_ID}.txt")
        documents = loader.load()
        print(documents)

        # split it into chunks
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        docs = text_splitter.split_documents(documents)
        print("This from VectorDB fn:    ", docs)
        # create the open-source embedding function
        embedding_function = OpenAIEmbeddings()
        # load it into Chroma
        
        self.db =  Chroma.from_documents(docs, embedding_function, persist_directory=f'VectorDB/{self.vid_ID}')
        # _openai = OpenAI(model="gpt-3.5-turbo", temperature=0.7, max_tokens=3000)
        # self.chain = load_qa_chain(_openai, chain_type="stuff")


    def __chat_with_memory(self, full_prompt):

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo-16k",
            messages=[
            {"role": "system", "content": "You are a helpful assistant. Only answer if question is related to the context,if you don't know the  say I dont have any information regarding this topic"},
            {"role": "user", "content": full_prompt}
            ]
        )
        return (completion.choices[0].message)


    def answer_question(self, query):
        
        if self.db is None:
            print("Error: Database not initialized. Please call VectorDB method first.")
            return None
        
        new_docs = self.db.similarity_search(query)

        print("This is from answer_question fn:    ",new_docs)

        final_str=f'''Answer the query from the context given only
                    Context--{new_docs}
                    Query--{query}'''
        
        print(final_str)
        answer= self.__chat_with_memory(final_str)
        return answer["content"]
    