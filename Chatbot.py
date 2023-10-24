import google.generativeai as palm
import re
from gradio.components import Textbox, HTML
from gradio import Interface

palm.configure(api_key='YOUR_API_KEY')

models = [m for m in palm.list_models() if 'generateText' in m.supported_generation_methods]
model = models[0].name

def genResp(text):
    completion = palm.generate_text(
        model=model,
        prompt=text,
        temperature=0,
        max_output_tokens=800 # The maximum length of the response
    )
    return completion.result

questions = [
    [
        "History of {} programming language",
        "What is {} programming language?",
        "What are the features of {} programming language?",
    ],
    "PreRequisites for {} programming language?",
    "Requirements for {} programming language?",
    "Installations for {} programming language?",
    "What are the advantages of {} programming language?",
    "What are the applications of {} programming language? (with examples like frameworks, libraries, etc.)",
    "What are the concepts to learn {} programming language?",
    "What are the resources to learn {} programming language? (like courses, video, blogs, etc. links)",
]

infoQuestions = [
    "About {}: ",
    "PreRequisites for {}: ",
    "Requirements for {}: ",
    "Installations for {} programming language?",
    "Advantages of {}: ",
    "Applications of {}: ",
    "Concepts to learn {}: ",
    "Resources to learn {}: ",
]

def chatWithAI(language):
    if language:
        language = language.lower()
        question = "Is {} a programming language? Reply True or False"
        if bool(genResp(question.format(language))):
            responses = ""
            i = -1
            for question in questions:
                i += 1
                if isinstance(question, list):
                    responses += f'<p style="font-size: 20px; font-weight: bold;">{infoQuestions[i].format(language)}</p><br>'
                    for q in question:
                        res = re.sub(r"\n", "<br>", genResp(q.format(language)))
                        responses += f'{res}<br><br>'
                else:
                    res = re.sub(r"\n", "<br>", genResp(question.format(language)))
                    responses += f'<p style="font-size: 20px; font-weight: bold;">{infoQuestions[i].format(language)}</p><br>{res}<br><br>'
            return responses
        else:
            rs = re.sub(r"\n", "<br>", genResp(f"What is {language}?"))
            responses = f'The provided input is not a programming language.<br><p style="font-size: 20px; font-weight: bold;">What is {language}</p><br>{rs}'
            return responses
    else:
        return "Please enter the name of a programming language."

# Create a Gradio Component
inputs = Textbox(lines=2, label="Chat with AI")
outputs = HTML(label="Reply")

# Create a Gradio interface
chatInterface = Interface(
    fn=chatWithAI,
    inputs=inputs, 
    outputs=outputs, 
    title="Chatbot for Engineers",
    description="Enter the name of a programming language.",
    theme="default"
)

chatInterface.launch(inline=True, share=True)
