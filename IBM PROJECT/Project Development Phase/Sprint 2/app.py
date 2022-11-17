from flask import Flask,render_template,redirect,url_for, request,session
import ibm_db
import credentials
import ibm_boto3
from ibm_botocore.client import Config, ClientError



# Create resource https://s3.ap.cloud-object-storage.appdomain.cloud

cos = ibm_boto3.resource("s3",
    ibm_api_key_id=credentials.COS_API_KEY_ID,
    ibm_service_instance_id=credentials.COS_INSTANCE_CRN,
    config=Config(signature_version="oauth"),
    endpoint_url=credentials.COS_ENDPOINT
)

#Database connection
conn = ibm_db.connect("DATABASE="+credentials.DB2_DATABASE_NAME+";HOSTNAME="+credentials.DB2_HOST_NAME+";PORT="+credentials.DB2_PORT+";SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID="+credentials.DB2_UID+";PWD="+credentials.DB2_PWD+"",'','')

app=Flask(__name__)


@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/')
def signin():
    return render_template('signin.html')

@app.route('/signup')
def signup():
    return render_template('signup.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():  
    if 'email' in session:  
        session.pop('email',None)
        return redirect('/')
    return redirect('/')  


@app.route('/postSignUpData', methods=['GET', 'POST'])
def postSignUpData():
    msg=''
    if request.method == 'POST':
        name = request.form.get("name",False)
        email = request.form.get("email",False)
        password = request.form.get("password",False)
        username = request.form.get("username",False)
        

        sql = "SELECT * FROM user WHERE email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        if account:
            return render_template('signup.html', msg="You are already a member, please login using your details")
        else:
            insert_sql = "INSERT INTO user VALUES (?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt,1, email)
            ibm_db.bind_param(prep_stmt,2, password)
            ibm_db.bind_param(prep_stmt,3, name)
            ibm_db.bind_param(prep_stmt,4, username)
            ibm_db.execute(prep_stmt)
            msg="Registration successfull.."
            return render_template('signin.html',msg=msg)

@app.route('/postSignInData',methods =['POST','GET'])
def postSignInData():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
    
        sql = "SELECT PASSWORD FROM user WHERE email=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,email)
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        if account and account["PASSWORD"]==password:
            return render_template('index.html',email=email)
        else:
            msg="username or password is incorrect"
            return render_template('signin.html',msg=msg)


@app.route('/profile')
def profile():
  sql = "SELECT * FROM user"
  stmt = ibm_db.exec_immediate(conn, sql)
  while ibm_db.fetch_row(stmt) != False:
    email= ibm_db.result(stmt, 0)
    name= ibm_db.result(stmt, 2)
    username= ibm_db.result(stmt, 3)
    return render_template("profile.html", name=name, email=email, username=username)



if __name__=='__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)

