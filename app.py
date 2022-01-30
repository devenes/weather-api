from flask import Flask, render_template, request

# Create an object named app
app = Flask(__name__)

# Create name and lastname variables for main page
@app.route('/')
def home():
    return render_template('main.html', name='Enes', lastname='Turan')

# Add a statement to run the Flask application which can be reached from any host on port 80
if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='0.0.0.0', port=80)