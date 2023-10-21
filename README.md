from flask import Flask, request, render_template
import subprocess

app = Flask(__name)

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    userid = request.form['userid']
    
    # Execute the shell script with user details
    subprocess.run(['./script.sh', email, userid])

    return "Form submitted successfully"

if __name__ == '__main__':
    app.run(debug=True)
