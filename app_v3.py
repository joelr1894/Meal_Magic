from flask import Flask, render_template, request, json
from subprocess import call
app = Flask(__name__)
import sys

#flask app code starts here w/ website
@app.route('/')
def Hello():
    return render_template('homepage.html')

@app.route('/recommend_pg')
def recommend_pg():
    return render_template('Recommendations_page.html')

# request code

@app.route('/recommendation_gen',methods=['POST'])
def recommendation_gen():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _inpNum = int(request.form['inputNum'])
    # validate the received values
    #parse the output from python code
    #maybe use string in between output do dads (use 2d array to hold restaurant names and numbers i.e. data[0][0] = rest name and data [0][1] = rating)
    #output in JSON
    
    if _name and _inpNum :
        #to get output, run recommendation algorithm above and then reformat output here and then return it!!
        #return json.dumps({'html':'<span>' + _name + ' ' +  _inpNum + '</span>'})
        _name = str(_name)
        print _name
        _inpNum = int(_inpNum)
        print _inpNum
        x_temp = execfile('meal_magic_k2.py', '_name' '_inpNum')
        print x_temp
        return json.dumps({'html': '<span>'})
        #subprocess.call(['meal_magic_k2.py', _name, _inpNum])
        #return json.dumps({'html':'<span>' + final_rec + '</span>'})
    #else:
        #return json.dumps({'html':'<span> </span>'})
 
@app.route('/initialSurvey')
def initialSurvey():
    return render_template('InitialSurvey.html')

@app.route('/home')
def home():
    return render_template('homepage.html')

@app.route('/aboutUs')
def aboutUs():
    return render_template('AboutUs_Success.html')

if __name__ == "__main__":
    app.run()