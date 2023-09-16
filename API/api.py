from flask import Flask, render_template,request
from src.main_file import main
from src.mongodb import insert, query_from_database

app=Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    global title
    parsed_data=main()
    saved_into_db = insert(parsed_data)
    return render_template("index.html",parsed_data=parsed_data)

@app.route("/archive", methods=["GET","POST"])
def archieve():
    return render_template("archive.html")

@app.route("/process", methods=["POST"])
def process():
    user_input = request.form.get("user_input")
    output = query_from_database(user_input)
    return render_template("success.html",output=output, user_input=user_input)



if __name__ =="__main__":
    app.run(debug=True)
