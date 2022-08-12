from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import T5ForConditionalGeneration, T5Tokenizer
from flask_cors import CORS


app = Flask(__name__)
CORS(app)

model = T5ForConditionalGeneration.from_pretrained("t5-small")
tokenizer = T5Tokenizer.from_pretrained("t5-small", model_max_length=512)


def get_complete_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript_string = ""

    for transcript in transcript_list:
        transcript_string += transcript['text'] + " "

    return transcript_string


def get_summary_from_transcript(transcript):
    inputs = tokenizer.encode("summarize: " + transcript,
                              return_tensors="pt", max_length=512, truncation=True)

    outputs = model.generate(
        inputs,
        max_length=150,
        min_length=40,
        length_penalty=2.0,
        num_beams=4,
        early_stopping=True)

    summarized_transcript = tokenizer.decode(outputs[0])

    return summarized_transcript


@app.route('/api/summarize', methods=['GET'])
def summarize():
    args = request.args
    url = args.get("youtube_url")

    if '/watch?v=' in url:
        video_id = url.split('/watch?v=')[1]
    else:
        return jsonify("Invalid URL")

    transcript = get_complete_transcript(video_id)
    summarized_transcript = get_summary_from_transcript(transcript)

    return jsonify(summarized_transcript)


if __name__ == '__main__':
    app.run(debug=True)
