from flask import Flask,render_template

app=Flask(__name__)

@app.route('/')
def base():
    return render_template('base.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')



if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)
