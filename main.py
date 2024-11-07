import time
import random
from nextdnsapi.api import *
from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

app.secret_key = 'jexxer'

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['password']
    config_id = request.form['config']
    
    try:
        header = account.login(email, password)
        print(account.list(header)) 
    except Exception as e:
        return redirect(url_for('index'))
    
    file = request.files['file']
    if file:
        file_name = 'uploads/' + file.filename
        file.save(file_name)
        
        try:
            with open(file_name, 'r') as saved_domains:
                for i in saved_domains:
                    domain = i.strip()
                    print(f"Adding domain: {domain}")
                    timer = random.randint(1, 4) 
                    time.sleep(timer)
                    response = denylist.blockdomain(domain, config_id, header)
                    print(response)  
        except Exception as e:
            print(f"An error occurred while processing the file: {e}")
            return redirect(url_for('index'))
        
        print("Domains successfully added to the denylist!")
    else:
        print("No file selected!")

    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
