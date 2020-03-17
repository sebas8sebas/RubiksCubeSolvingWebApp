from flask import  Flask, render_template, url_for, request, redirect, jsonify
from beginnersMethod import BeginnersCube

#https://www.speedsolving.com/wiki/index.php/Kociemba's_Algorithm

app = Flask(__name__)



@app.route('/')
def index():


    return render_template('index.html') #the folder is called template for a reason lol


@app.route('/solve', methods=['POST'])
def solve():


    cubeDict = request.get_json() # parse as JSON
    cube = BeginnersCube(cubeDict)
    #print(cubeDict)
    #print(cube)
    isValid = cube.solve()
    if isValid: return jsonify({"valid": True, "solution": cube.movesDone})
    else: return jsonify({"valid": False})


if __name__ == "__main__":
    app.run(debug=True)    #set to false when you want to debug lol
