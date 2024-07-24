from flask import Flask, render_template, request
import requests
import html
import random


app=Flask("__name__")
# Getting link of api and other empty lists
url="https://opentdb.com/api.php?amount=50&category=18&type=multiple"
s=requests.Session()
req=requests.get(url)
response=str(req.status_code)
q_list=[]
decoded_question=[]
correct=[]
incorrect=[]
options=[]
decoded_options=[]

# Making function to check connection
def checking():
    if response=="200":
        data=req.json()["results"]

        global length
        length=len(data)

        # Appending data like questions and answers in empty lists
        for i in range(0,length):
            q_list.append(data[i]["question"])
            correct.append(data[i]["correct_answer"])
            incorrect.append(data[i]["incorrect_answers"])

        if not decoded_question:            # for preventing repeation of option after reload
            # decoding the questions
            for q in q_list:
                edited=html.unescape(q)
                decoded_question.append(edited)

            # merging correct and incorrect options
            for i in range(0,len(correct)):
                incorrect[i].insert(0,correct[i])

            # decoding the options
            for answer in incorrect:
                for i in answer:
                    edited=html.unescape(i)
                    options.append(edited)
                        
            # making pair of all options according to the nummber of options i.e 4          
            for i in range(0,len(options),4):
                decoded_options.append(options[i:i+4])

            # shuffling options  
            for mcq in decoded_options:
                random.shuffle(mcq)
        
@app.route('/', methods=["POST","GET"])
def home():
    checking()
    if str(req.status_code)=="200":             
        return render_template("index.html", length=length, decoded_question=decoded_question, decoded_options=decoded_options)
    else:
        error=str(response)+"error, data not found"
        return error

@app.route('/result', methods=['GET','POST'])
def result():
    if response=="200":
        data=req.json()["results"]
        correct_answer=0
        selected_options=[]
        if str(req.status_code)=="200": 
            checking()

            # pprogram for counting the correct no. of questions
            for i in range(0,len(data)):
                select=str("option"+str(i)) # name of the input tag
                selected_options.append(select) 
                selection=request.form.get(selected_options[i]) # getting the selected value

                # counting correct answers and decoding correct answers for accuracy
                if selection==html.unescape(data[i]["correct_answer"]):
                    correct_answer=correct_answer+1
            correctAnswers=str(correct_answer)
        return render_template("result.html", correctAnswers=correctAnswers, length=length)
        
@app.route('/correct', methods=['GET','POST'])
def api():
    if str(req.status_code)=="200": 
        c_ans=[]
        checking() 
        for ans in correct:
                edited=html.unescape(ans)
                c_ans.append(edited)
        
    return render_template("correct.html", c_ans=c_ans, decoded_question=decoded_question, length=length)
        
if __name__=="__main__":
    app.run(debug=True)
