"""
Flask application for Emotion Detection.
"""

import json

from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask("Emotion Detector")

@app.route("/emotionDetector")
def emotion_detector_route():
    """
    Analyse the user-provided text and return emotion scores
    along with the dominant emotion.
    """
    text_to_analyze = request.args.get('textToAnalyze')

    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again."

    try:
        result = json.loads(emotion_detector(text_to_analyze))
    except Exception:
        return "Emotion detection service is unavailable right now."

    try:
        emotions = result['emotionPredictions'][0]['emotion']
    except (KeyError, IndexError, TypeError):
        return "Invalid text! Please try again."

    anger = emotions['anger']
    disgust = emotions['disgust']
    fear = emotions['fear']
    joy = emotions['joy']
    sadness = emotions['sadness']
    dominant_emotion = max(emotions, key=emotions.get)

    output = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, "
        f"'fear': {fear}, 'joy': {joy} and "
        f"'sadness': {sadness}. The dominant emotion is {dominant_emotion}."
    )

    return output

@app.route("/")
def render_index_page():
    """
    Render the index page of the Emotion Detector application.
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)