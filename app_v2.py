from flask import Flask, render_template, request, json
from subprocess import call
app = Flask(__name__)

@app.route('/')
def Hello():
    return render_template('homepage.html')

@app.route('/recommend')
def recommend():
    return render_template('Recommendations_page.html')

# request code

@app.route('/recommendation',methods=['POST'])
def recommendation():
 
    # read the posted values from the UI
    _name = request.form['inputName']
    _inpNum = request.form['inputNum']
 
    # validate the received values
    #parse the output from python code
    #maybe use string in between output do dads (use 2d array to hold restaurant names and numbers i.e. data[0][0] = rest name and data [0][1] = rating)
    #output in JSON
    if _name and _inpNum :
        #to get output, run recommendation algorithm above and then reformat output here and then return it!!
        #return json.dumps({'html':'<span>' + _name + ' ' +  _inpNum + '</span>'})
        outp = subprocess.call(['python', ' meal_magic.py', str(_name), _inpNum])
        return json.dumps({'html':'<span>' outp '</span>'})
    else:
        return json.dumps({'html':'<span> </span>'})
 
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
