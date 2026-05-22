from flask import Flask, render_template, request
import whisper
import os
os.environ['PATH']+=os.pathsep+r"D:\Ai_interview_analyzer\ffmpeg-8.1.1-essentials_build\bin"


app = Flask(
    __name__,
    template_folder=os.path.join(os.path.dirname(__file__), 'Templates'),
    static_folder=os.path.join(os.path.dirname(__file__), 'static'),
)

UPLOAD_FOLDER = os.path.join(os.getcwd(), 'uploads')
os.makedirs(UPLOAD_FOLDER,exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Load whisper model
model = whisper.load_model("base")


@app.route('/')
def home():
    return render_template('index.html')


@app.route('/practice')
def practice():
    return render_template('practice.html')


@app.route('/analyze', methods=['POST'])
def analyze():

    if 'audio' not in request.files:
        return "No audio uploaded"

    file = request.files['audio']

    if file.filename == '':
        return "No file selected"

    filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
    file.save(filepath)

    # Speech to text
    result = model.transcribe(filepath)

    transcript = result['text']

    # Basic analysis
    words = transcript.split()
    total_words = len(words)

    filler_words = ['um', 'uh', 'like', 'actually', 'basically']

    filler_count = 0

    for word in words:
        if word.lower() in filler_words:
            filler_count += 1

    # Score logic
    communication_score = 100

    if filler_count > 10:
        communication_score -= 20

    if total_words < 30:
        communication_score -= 20

    if total_words > 100:
        communication_score += 10

    if communication_score > 100:
        communication_score = 100

    # Feedback
    feedback = []

    if filler_count > 10:
        feedback.append("Too many filler words used.")
    else:
        feedback.append("Good speaking clarity.")

    if total_words < 30:
        feedback.append("Answer is too short.")
    else:
        feedback.append("Answer length is good.")

    if communication_score >= 80:
        feedback.append("Excellent communication skills.")
    elif communication_score >= 60:
        feedback.append("Average communication skills.")
    else:
        feedback.append("Needs improvement.")

    # Simple scores for result cards (hackathon-friendly logic)
    confidence_score = max(0, min(100, communication_score - filler_count))
    technical_score = min(100, 60 + min(total_words // 5, 40))

    if filler_count <= 3:
        emotion = "Calm"
    elif filler_count <= 8:
        emotion = "Neutral"
    else:
        emotion = "Nervous"

    return render_template(
        'result.html',
        transcript=transcript,
        total_words=total_words,
        filler_count=filler_count,
        score=communication_score,
        confidence=confidence_score,
        technical=technical_score,
        emotion=emotion,
        feedback=feedback
    )



@app.route('/practice_analyze', methods=['POST'])
def practice_analyze():
    # Accept multiple audio files from the practice flow
    files = request.files.getlist('audio')

    if not files:
        return "No audio uploaded"

    # Save and transcribe each file, concatenate transcripts
    transcripts = []
    total_words = 0
    filler_words = ['um', 'uh', 'like', 'actually', 'basically']
    filler_count = 0

    for f in files:
        if f.filename == '':
            continue
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], f.filename)
        f.save(filepath)
        result = model.transcribe(filepath)
        text = result.get('text', '')
        transcripts.append(text)

        words = text.split()
        total_words += len(words)
        for w in words:
            if w.lower() in filler_words:
                filler_count += 1

    transcript = '\n'.join(transcripts)

    # Score logic (same as /analyze)
    communication_score = 100

    if filler_count > 10:
        communication_score -= 20

    if total_words < 30:
        communication_score -= 20

    if total_words > 100:
        communication_score += 10

    if communication_score > 100:
        communication_score = 100

    feedback = []

    if filler_count > 10:
        feedback.append("Too many filler words used.")
    else:
        feedback.append("Good speaking clarity.")

    if total_words < 30:
        feedback.append("Answer is too short.")
    else:
        feedback.append("Answer length is good.")

    if communication_score >= 80:
        feedback.append("Excellent communication skills.")
    elif communication_score >= 60:
        feedback.append("Average communication skills.")
    else:
        feedback.append("Needs improvement.")

    confidence_score = max(0, min(100, communication_score - filler_count))
    technical_score = min(100, 60 + min(total_words // 5, 40))

    if filler_count <= 3:
        emotion = "Calm"
    elif filler_count <= 8:
        emotion = "Neutral"
    else:
        emotion = "Nervous"

    return render_template(
        'result.html',
        transcript=transcript,
        total_words=total_words,
        filler_count=filler_count,
        score=communication_score,
        confidence=confidence_score,
        technical=technical_score,
        emotion=emotion,
        feedback=feedback
    )


if __name__ == '__main__':
    app.run(debug=True)