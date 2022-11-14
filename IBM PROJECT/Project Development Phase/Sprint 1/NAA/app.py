from flask import Flask,render_template,redirect

app=Flask(__name__)

@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')


if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)

