from flask import Flask, request, render_template
import subprocess

app = Flask(__name)

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form['email']
        userid = request.form['userid']
        
        # Execute the shell script with user details
        subprocess.run(['./script.sh', email, userid])

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
