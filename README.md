# YouTube Content Query Framework

## Overview

This innovative project introduces a Retrieval-Augmented Generation (RAG) framework that integrates with GPT-3.5, powered by ChromaDB, to facilitate an in-depth understanding of YouTube documentaries and lectures. It's designed to extract comprehensive video content, enabling users to query specific information and receive accurate responses directly related to the video content.

## Structure

The solution is encapsulated across three primary components:

### 1. `components.py`

- Central to the framework, this module defines a class encompassing critical functions essential for processing and querying video content.

### 2. `pipeline.py`

- This script orchestrates the workflow, invoking functions from `components.py` to establish a coherent pipeline. It also contains the implementation for initiating the Gradio interface, offering an intuitive UI for user interactions.

### 3. `main.py`

- The entry point of the application. Running this script activates the Gradio web app, presenting a user-friendly platform for engaging with the framework's capabilities.

## Getting Started

### Installation

First, ensure that all necessary dependencies are installed:

```bash
pip install -r requirements.txt
```

### Configuration

- **API Keys:** Securely store your OpenAI and ElevenLabs API keys by either:
  - Creating a `secrets.yaml` file in the project root, or
  - Directly inserting your keys in the `main.py` file.

### Launching the Application

Activate the web interface through the following command:

```bash
python main.py
```

For a Jupyter Notebook demonstration, including similar functionalities and interactive components, refer to `test.ipynb`.
