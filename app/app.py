from flask import Flask, request, redirect, url_for, render_template_string
import pymongo
from datetime import datetime

app = Flask(__name__)

# MongoDB setup
client = pymongo.MongoClient("mongodb://localhost:27017/")
db = client["typing_speed_test"]
collection = db["results"]

def get_sample_text():
    return "The quick brown fox jumps over the lazy dog."

@app.route('/')
def index():
    sample_text = get_sample_text()
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Typing Speed Test</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            width: 50%;
            margin: 0 auto;
            text-align: center;
        }
        textarea {
            width: 100%;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Typing Speed Test</h1>
        <p id="sample-text">{{ sample_text }}</p>
        <form action="{{ url_for('submit') }}" method="POST">
            <input type="hidden" name="start_time" id="start_time">
            <textarea name="typed_text" id="typed_text" rows="4" cols="50"></textarea>
            <br>
            <button type="submit">Submit</button>
        </form>
    </div>
    <script>
        document.getElementById('start_time').value = new Date().toISOString();
    </script>
</body>
</html>
''', sample_text=sample_text)

@app.route('/submit', methods=['POST'])
def submit():
    start_time = datetime.fromisoformat(request.form['start_time'])
    end_time = datetime.now()
    typed_text = request.form['typed_text']

    sample_text = get_sample_text()
    time_taken = (end_time - start_time).total_seconds()
    words_typed = len(typed_text.split())
    correct_words = sum(1 for w1, w2 in zip(typed_text.split(), sample_text.split()) if w1 == w2)
    
    wpm = (words_typed / time_taken) * 60
    accuracy = (correct_words / len(sample_text.split())) * 100

    result = {
        "timestamp": end_time,
        "time_taken": time_taken,
        "wpm": wpm,
        "accuracy": accuracy
    }

    collection.insert_one(result)
    return redirect(url_for('results'))

@app.route('/results')
def results():
    results = collection.find().sort("timestamp", -1).limit(5)
    return render_template_string('''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <title>Typing Speed Test Results</title>
    <style>
        body {
            font-family: Arial, sans-serif;
        }
        .container {
            width: 50%;
            margin: 0 auto;
            text-align: center;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Previous Results</h1>
        <ul>
            {% for result in results %}
            <li>
                Time Taken: {{ result.time_taken }} seconds, 
                WPM: {{ result.wpm }}, 
                Accuracy: {{ result.accuracy }}%
                ({{ result.timestamp.strftime('%Y-%m-%d %H:%M:%S') }})
            </li>
            {% endfor %}
        </ul>
        <a href="{{ url_for('index') }}">Back to Test</a>
    </div>
</body>
</html>
''', results=results)

if __name__ == '__main__':
    app.run(debug=True)
