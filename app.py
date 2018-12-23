from flask import Flask, request, render_template, make_response, url_for, abort, session
from werkzeug.utils import secure_filename, redirect, escape

app = Flask(__name__)


@app.route('/helloworld')
def hello_world():
    return 'Hello World!'


@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username  #字符串格式化

# Variable Rules
# You can add variable sections to a URL by marking sections with <variable_name>. Your function then
# receives the <variable_name> as a keyword argument. Optionally, you can use a converter to specify the type of the
# argument like <converter:variable_name>.
# Converter types:
# string	(default) accepts any text without a slash
# int	accepts positive integers
# float	accepts positive floating point values
# path	like string but also accepts slashes
# uuid	accepts UUID strings
#


@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/path/<path:subpath>')
def show_subpath(subpath):
    # show the subpath after /path/
    return 'Subpath %s' % subpath
# 指定GET POST方法
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        return "post login"
    else:
        return "get login"

#3. Rendering Templates
# Flask will look for templates in the templates folder.
@app.route('/hello/')
@app.route('/hello/<name>')
def hello(name=None):
    return render_template('hello.html', name=name)
#4.the request object
# The current request method is available by using the method attribute. To access form data (data transmitted in a
# POST or PUT request) you can use the form attribute.
@app.route('/login1', methods=['POST', 'GET'])
def login1():
    error = None
    # 获取?key=value get方法参数
    searchword = request.args.get('key', '')
    if request.method == 'POST':
        if valid_login(request.form['username'],
                       request.form['password']):
            return log_the_user_in(request.form['username'])
        else:
            error = 'Invalid username/password'

    # the code below is executed if the request method
    # was GET or the credentials were invalid
    return render_template('login.html', error=error)

# 5.file uploads
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        f = request.files['the_file']
        f.save('/var/www/uploads/uploaded_file.txt')
        # 名字容易被串改，使用secure_filename
        f.save('/var/www/uploads/' + secure_filename(f.filename))
# 6.cookies
@app.route('/cookies')
def index():
    username = request.cookies.get('username')
    # use cookies.get(key) instead of cookies[key] to not get a
    # KeyError if the cookie is missing.

    # set the cookie
    resp = make_response(render_template(""))
    resp.set_cookie('username', 'the username')
    return resp

# 7. Redirects and Errors
# To redirect a user to another endpoint, use the redirect() function; to abort a request
# early with an error code, use the abort() function:
@app.route('/index')
def index1():
    return redirect(url_for('login')) #重定向

@app.route('/login2')
def login2():
    abort(401)   #抛出异常
    # this_is_never_executed()
# By default a black and white error page is shown for each error code. If you want to customize the error page, you can use the errorhandler() decorator:
@app.errorhandler(404)  #自定义异常处理页面
def page_not_found(error):
    return render_template('page_not_found.html'), 404
# 8.about response
@app.errorhandler(404)
def not_found(error):
    resp = make_response(render_template('error.html'), 404)
    resp.headers['X-Something'] = 'A value'  #添加默认头部在response中
    return resp

# 8 session
# Set the secret key to some random bytes. Keep this really secret!
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/session')
def session():
    if 'username' in session:
        # escapte 相当于url.encode,转换Html字符串
        return 'Logged in as %s' % escape(session['username'])
    return 'You are not logged in'

@app.route('/loginsession', methods=['GET', 'POST'])
def loginsession():
    if request.method == 'POST':
        session['username'] = request.form['username']
        return redirect(url_for('index'))
    return '''
        <form method="post">
            <p><input type=text name=username>
            <p><input type=submit value=Login>
        </form>
    '''

@app.route('/logout')
def logout():
    # remove the username from the session if it's there
    session.pop('username', None)  #删除session
    return redirect(url_for('index'))


# 9.How to generate good secret keys
# A secret key should be as random as possible. Your operating system has ways to
# generate pretty random data based on a cryptographic random generator. Use the following command to quickly
# generate a value for Flask.secret_key (or SECRET_KEY): $ python -c 'import os; print(os.urandom(16))'
# b'_5#y2L"F4Q8z\n\xec]/'

# 10.logging
@app.route('/logger')
def log():
    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')
    app.logger.info('An error occurred')
    return 'logger test'









def valid_login(param, param1):
    pass
def log_the_user_in(param):
    pass



if __name__ == '__main__':
    app.run()
