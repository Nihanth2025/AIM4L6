import requests
from config import HF_API_KEY
from colorama import Fore, Style, init
init(autoreset=True)
DEFAULT_MODEL="google/pegasus-xsum"
def bulid_api_url(model_name):
    return f"https://api-inference.huggingface.co/models/{model_name}"
def query(payload: dict, model_name=DEFAULT_MODEL):
    api_url=bulid_api_url(model_name)
    headers={"Authorization": f"Bearer {HF_API_KEY}"}
    response=requests.post(api_url, headers=headers, json=payload)
    return response.json()
def summarize_text(text, min_length, max_length,model_name=DEFAULT_MODEL):
    payload={
        "inputs": text,
        "parameters": {
            "min_length": min_length,
            "max_length": max_length,
        },
    }
    print(Fore.BLUE + Style.BRIGHT + f"\n???? performing ai summarization using model: {model_name}")
    result=query(payload, model_name=model_name)
    if isinstance(result, list) and result and "summary_text" in result[0]:
        return result[0]["summary_text"]
    else:
        print(Fore.RED + "error in summarization response: ", result)
        return None
if __name__=="__main__":
    print(Fore.RED + Style.BRIGHT + "???? Hi there what's your name!!!!!!!!!:",)
    user_name=input("your name: ").strip()
    if not user_name:
        user_name="User"
    print(Fore.YELLOW + f"Welcome {user_name} let's give your text some ai magic and love")
    print(Fore.GREEN +Style.BRIGHT + "???? Please enter the text you want to summarize: ")
    user_text=input("Enter your text: ").strip()
    if not user_text:
        print(Fore.RED + "error: no text provided")
    else:
        print(Fore.YELLOW + Style.BRIGHT + "??? Enter the model name you want to use (e.g., facebook/bart-large-cnn): ")
        model_choice=input("Model choice: ").strip()
        if not model_choice:
            model_choice=DEFAULT_MODEL
        print(Fore.YELLOW + Style.BRIGHT + "??? Choose your summarization style:")
        print("1. standard summary (quick and concise)")
        print("2. enhanced summary (more detailed and refined)")
        style_choice=input("Your choice (1/2): ").strip()
        if style_choice=="2":
            min_length, max_length=80,200
            print(Fore.GREEN + Style.BRIGHT + "??? Generating enhanced summary...")
        else:
            min_length, max_length=50,150
            print(Fore.GREEN + Style.BRIGHT + "??? Generating standard summary...")
        summary=summarize_text(user_text, min_length, max_length, model_name=model_choice)
        if summary:
            print(Fore.GREEN + Style.BRIGHT + "??? Here is your summary: ")
            print(Fore.CYAN + summary)
        else:
            print(Fore.RED + "error: unable to generate summary")