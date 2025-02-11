# from flask import Flask, render_template, request, redirect
# import jobs

# app = Flask(__name__)  # Correcting to __name_

# problem = ''

# @app.route('/', methods=['GET', 'POST'])
# def index():
#     global problem
#     if request.method == 'POST':
#         problem = request.form.get('problem', '')  
#         if problem:
#             jobs.get_text(problem)
#             final = jobs.send()
#             print(final)
#     return render_template('home.html')



# if __name__ == '__main__':
#     app.run(debug=True)  



from flask import Flask, render_template, request, redirect
import jobs

app = Flask(__name__)  
problem = ''


@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')
@app.route('/o.html')
def opportunities():
    return render_template('o.html')

@app.route('/t.html')
def training_programs():
    return render_template('t.html')

@app.route('/r.html')
def resources():
    return render_template('r.html')

@app.route('/index', methods = ['GET', 'POST'])
def index():
    global problem
    global final
    final =None
    if request.method == 'POST':
        problem = request.form.get('problem', '') 
        print("prob = ", problem) 
        if problem:
            jobs.get_text(problem)
            final = jobs.send()
    return render_template('index.html',output=final)

if __name__ == '__main__':
    app.run(debug=True)  