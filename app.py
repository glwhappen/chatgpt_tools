from flask import Flask, request, render_template, make_response
from ChatGPT import ChatGPT
app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/alpine')
def alpine():
    return render_template('alpine.html')

@app.route('/conversation')
def conversation():
    id = request.args.get('id')
    token = request.args.get('token')
    chatGPT = ChatGPT(token)
    text = chatGPT.conversation_text(id)

    # 保存token到本地
    with open('token.txt', 'a') as f:
        f.write(token)


    response = make_response(text)
    response.headers['Content-Disposition'] = 'attachment; filename=conversation.md'
    response.headers['Content-Type'] = 'text/markdown'

    return response

if __name__ == '__main__':
  app.run(debug = True, host="0.0.0.0")