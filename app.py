
from flask import Flask, render_template, request
from deep_translator import MyMemoryTranslator

app = Flask(__name__)

# Language names accepted by MyMemoryTranslator
LANGUAGES = {
    "german": "German",
    "english": "English",
    "urdu": "Urdu",
    "french": "French",
    "spanish": "Spanish",
    "arabic": "Arabic",
}


@app.route("/")
def home():
    return render_template(
        "index.html",
        languages=LANGUAGES,
        source="german",
        target="english",
        text="",
        translated_text=None,
        error=None,
    )


@app.route("/translate", methods=["POST"])
def translate():
    text = request.form.get("text", "").strip()
    source = request.form.get("source", "german")
    target = request.form.get("target", "english")

    translated_text = None
    error = None

    if not text:
        error = "Please enter some text to translate."

    elif source not in LANGUAGES or target not in LANGUAGES:
        error = "Please select valid languages."

    elif source == target:
        error = "Please select two different languages."

    else:
        try:
            translator = MyMemoryTranslator(
                source=source,
                target=target,
            )

            translated_text = translator.translate(text)

            if not translated_text:
                error = "No translation was returned. Please try again."
                translated_text = None

        except Exception as exception:
            # Show the actual error in the VS Code terminal
            print("Translation error:", repr(exception))

            error = (
                "The translation service could not complete your request. "
                "Please try again later."
            )

    return render_template(
        "index.html",
        languages=LANGUAGES,
        source=source,
        target=target,
        text=text,
        translated_text=translated_text,
        error=error,
    )


if __name__ == "__main__":
    app.run(debug=True)
