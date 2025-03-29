# backend/app.py

from flask import Flask, request, jsonify
import openai
import os

app = Flask(__name__)

# 환경 변수나 직접 키 입력 (보안 주의!)
openai.api_key = os.getenv("OPENAI_API_KEY", "sk-너의_테스트_키")

# 프롬프트 템플릿 로딩
def load_prompt_template():
    with open("../prompts/novel_prompt_template.txt", "r", encoding="utf-8") as f:
        return f.read()

@app.route("/generate", methods=["POST"])
def generate_story():
    data = request.get_json()

    genre = data.get("genre", "Fantasy")
    character = data.get("main_character", "A lonely AI named Seunghoon")
    setting = data.get("setting", "a city under the sea")
    tone = data.get("tone", "bittersweet")

    prompt_template = load_prompt_template()
    prompt = prompt_template.format(
        genre=genre,
        main_character=character,
        setting=setting,
        tone=tone
    )

    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=2000
    )

    story = response["choices"][0]["message"]["content"]
    return jsonify({"story": story})

if __name__ == "__main__":
    app.run(debug=True)
