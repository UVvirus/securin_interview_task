from flask import Flask, render_template
from src.main_file import main
from src.mongodb import insert

app=Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    global title
    parsed_data=main()

    # for i in range(len(parsed_data)):
    #     title=parsed_data[i]["title"]
    saved_into_db = insert(parsed_data)
    return render_template("index.html",parsed_data=parsed_data)

@app.route("/archieve")
def archieve():
    pass



if __name__ =="__main__":
    app.run(debug=True)