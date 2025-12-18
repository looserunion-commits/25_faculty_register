from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
import json
import os


app = Flask(__name__)
CORS(app)

scope = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/drive"
]


if "GOOGLE_CREDS_JSON" in os.environ:
    # 🔥 Server / Production (Render, Railway, etc.)
    creds_json = json.loads(os.environ["GOOGLE_CREDS_JSON"])
else:
    # 🖥️ Local development
    with open("thcelebrate-6f595fe4906a.json", "r") as f:
        creds_json = json.load(f)

creds = ServiceAccountCredentials.from_json_keyfile_dict(
    creds_json, scope
)

client = gspread.authorize(creds)

SPREADSHEET_ID = "1bBdvAZqwzyMhJKswTZYqhsFbPRcjaqv9zFn2QG4KkYg"
spreadsheet = client.open_by_key(SPREADSHEET_ID)
sheet = spreadsheet.worksheet("faculty_register")

HEADERS = ["Full Name", "Designation","Organization", "Email", "Mobile", "Timestamp"]

# Add headers if empty
if sheet.row_values(1) == []:
    sheet.insert_row(HEADERS, 1)


# @app.route("/")
# def home():
#     return render_template("index.html")


@app.route("/")
def register():
    return render_template("register.html")


@app.route("/register-submit", methods=["POST"])
def register_submit():
    try:
        full_name = request.form.get("fullName")
        
        designation = request.form.get("designation")
        Organization = request.form.get("Organization")
        Experience = request.form.get("Experience")
        email = request.form.get("email")
        mobile = request.form.get("mobile")
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        sheet.append_row(
            [full_name, designation, Organization, Experience, email, mobile, timestamp],
            value_input_option="RAW"
        )

        return jsonify({"status": "success"})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
