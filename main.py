import openai, re
import requests
from bs4 import BeautifulSoup
from googlesearch import search
headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Methods': 'GET',
    'Access-Control-Allow-Headers': 'Content-Type',
    'Access-Control-Max-Age': '3600',
    'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0'
    }
openai.api_key = ""
openai.organization = ""

messages = [
        {"role": "system", "content": "You are a system controller. You can access the internet to get more information to answer questions by responding with just the text 'FETCH <url>'. To get the text output of a website you can respond with just the text FETCH <url> and I will respond with the text content of the page at the URL. You can leverage this to get more information to respond accurately to the questions. If the content for a URL does not provide the information to respond, try additional URLs until you have the most accurate data to respond. You should try at least three sources before responding. You can also leverage google by saying 'GOOGLE <query text>' and I'll respond with the top ten results and their URLs. You can then fetch those URLS with the FETCH command. When using commands, only use the command and nothing else. You will only use the commands or provide the answer. You will use the commands until you have the answer."},
        {"role": "user", "content": "Who's the prime minister of New Zealand?"}
    ]
while True:
    response = openai.ChatCompletion.create(
      model="gpt-4",
      messages=messages
    )
    resp_text = response['choices'][0]["message"]["content"]
    print(resp_text)
    messages.append({"role": "assistant", "content":resp_text})
    z = re.match("FETCH (.+)", resp_text)
    if (z):
        url = z.groups()[0]
        req = requests.get(url, headers)
        soup = BeautifulSoup(req.content, 'html.parser')
        content = " ".join(soup.text.split())
        content = content[0:min(8191, len(content))]
        messages.append({"role": "user", "content": content})
        # print(soup.text)
    else:
        z = re.match("GOOGLE (.+)", resp_text)
        if (z):
            text = z.groups()[0]
            searchresult = search(text, num_results=10, advanced=True)
            content = []
            for r in searchresult:
                content.append(r.title + " " + r.url)
            content = "\n".join(content)
            messages.append({"role": "user", "content": content})
        else:
            break
