from flask import Flask, request, jsonify
from datetime import datetime
import os

app = Flask(__name__)

OUTPUT_DIR = "/app/output"
TEMPLATE_PATH = "/app/templates/welcome_template.txt"

os.makedirs(OUTPUT_DIR, exist_ok=True)


# Loads the template
def load_template():
    with open(TEMPLATE_PATH, "r", encoding="utf-8") as f:
        return f.read()


# Fills the template
def fill_template(template, customer):
    # Add dynamic fields
    customer["CURRENT_DATE"] = datetime.now().strftime("%Y-%m-%d")

    # Replace placeholders like {{FIRST_NAME}}
    for key, value in customer.items():
        placeholder = f"{{{{{key}}}}}"
        template = template.replace(placeholder, str(value))

    return template


# Will generate letters
@app.route("/generate", methods=["POST"])
def generate_letters():
    data = request.get_json()
    customers = data.get("customers", [])

    template = load_template()
    generated_files = []

    for customer in customers:
        if customer.get("LETTER_TYPE", "").lower() != "welcome":
            continue

        letter_text = fill_template(template, customer)

        filename = f"welcome_{customer['FIRST_NAME']}_{customer['LAST_NAME']}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(letter_text)

        generated_files.append(filename)

    return jsonify({
        "status": "success",
        "generated_count": len(generated_files),
        "files": generated_files
    })


# Status or health check
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "ok", "service": "template-letter"})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)
