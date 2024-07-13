import gradio as gr 
from fake_news import FakeNews

def response(message,history):
    result = ""
    hello_msg = ["Hey Bot!", "Hi", "Hello"]
    bye_msg = ["Bye", "Exit"]
    if any(word in message for word in hello_msg):
        result = "Hello, Welcome to Fake Detector Bot!!"
    elif any(word in message for word in bye_msg):
        result = "Bye, Thank You!!"
    else:
        try:
            result = FakeNews.get_information(message)
        except Exception as e:
            print(str(e))
    return result

demo = gr.ChatInterface(fn=response,retry_btn=None,undo_btn=None,title="Fake Detector Bot")

if __name__ == "__main__":
    demo.launch(share=True)