//https://threejsfundamentals.org/threejs/lessons/threejs-fundamentals.html
//https://threejsfundamentals.org/threejs/lessons/threejs-align-html-elements-to-3d.html

var createCubeAnimation = function () {

  const ROTATIONSPEED = 3; //cube rotation speed


  //x and y axis
  var xAxis = new THREE.Vector3(1, 0, 0)
  var yAxis = new THREE.Vector3(0, 1, 0)

  //canvas
  var canvas = document.getElementById("canv");

  //Solve btn
  var solveBtn = document.getElementById("solveBtn");

  //indexes of centers (in Three each square is formed out of 2 trialngles, so we need 2 indexes for each piece of the cube)
  const Centers = {
    white1: 44, white2: 45, yellow1: 62, yellow2: 63, blue1: 80, blue2: 81,
    green1: 98, green2: 99, red1: 26, red2: 27, orange1: 8, orange2: 9
  };

  //mouse control
  var mousePressed = false;
  var deltaMouse = new THREE.Vector2(); //vector for chage in mouse position
  var mouse = new THREE.Vector2(); //vector for cur mouse position
  var raycaster = new THREE.Raycaster();
  var cubeRotated = false; //whether the cube was rotated on current mouse click

  //set up            
  var scene = new THREE.Scene();
  var camera = new THREE.PerspectiveCamera(75, canvas.width / canvas.height, 0.1, 1000);
  var renderer = new THREE.WebGLRenderer({ canvas });
  renderer.setSize(canvas.width, canvas.height);

  //create cube
  var geometry = new THREE.BoxGeometry(2, 2, 2, 3, 3, 3);
  var material = new THREE.MeshBasicMaterial({ vertexColors: THREE.FaceColors });
  var cube = new THREE.Mesh(geometry, material);


  //initialize cube colors/rotation
  initializeCube();

  scene.add(cube);

  //Need to move camera away because cube is on 0,0,0
  camera.position.z = 5;

  /**
   * animation function
   */
  var animate = function () {
    requestAnimationFrame(animate);
    renderer.render(scene, camera);
  };


  /**
   * Initialize cube colors and rotation
   */
  function initializeCube() {
    cube.geometry.faces.forEach(element => element.color.setColorName('gray'));

    cube.geometry.faces[Centers.white1].color.setColorName('white');
    cube.geometry.faces[Centers.white2].color.setColorName('white');
    cube.geometry.faces[Centers.yellow1].color.setColorName('yellow');
    cube.geometry.faces[Centers.yellow2].color.setColorName('yellow');
    cube.geometry.faces[Centers.blue1].color.setColorName('blue');
    cube.geometry.faces[Centers.blue2].color.setColorName('blue');
    cube.geometry.faces[Centers.green1].color.setColorName('green');
    cube.geometry.faces[Centers.green2].color.setColorName('green');
    cube.geometry.faces[Centers.red1].color.setColorName('red');
    cube.geometry.faces[Centers.red2].color.setColorName('red');
    cube.geometry.faces[Centers.orange1].color.setColorName('orange');
    cube.geometry.faces[Centers.orange2].color.setColorName('orange');

    cube.rotation.x = 0.3;
    cube.rotation.y = 0.4;
  }

  /**
   * Rotate cube is mouse is pressed
   */
  function onMouseMove(event) {


    // calculate mouse position in normalized device coordinates
    // (-1 to +1) for both components

    var rect = canvas.getBoundingClientRect();

    deltaMouse.x = ((event.clientX - rect.left) / canvas.height) * 2 - 1 - mouse.x;
    deltaMouse.y = - ((event.clientY - rect.top) / canvas.width) * 2 + 1 - mouse.y;

    mouse.x += deltaMouse.x;
    mouse.y += deltaMouse.y;


    if (mousePressed) {
      if (deltaMouse.x != 0 && deltaMouse.y != 0) {
        //cube.rotation.y += ROTATIONSPEED *(deltaMouse.x);
        //cube.rotation.x -= ROTATIONSPEED *(deltaMouse.y);
        cube.rotateOnWorldAxis(yAxis, ROTATIONSPEED * (deltaMouse.x));
        cube.rotateOnWorldAxis(xAxis, -ROTATIONSPEED * (deltaMouse.y));

        cubeRotated = true;
      }
    } else {
      cubeRotated = false;
    }

  }

  /**
   * handle mouse click (change cube colors)
   */
  function onMouseClick(event) {
    //return if cube was rotated
    if (cubeRotated) return;

    // update the picking ray with the camera and mouse position
    raycaster.setFromCamera(mouse, camera);

    // calculate objects intersecting the picking ray
    var intersects = raycaster.intersectObjects(scene.children);

    //return if nothing intersects ray
    if (intersects.length == 0) return;

    //intersects[0].object.material.color.set( 0xff0000 );
    //get relevant face indexes for intersection
    var faceIndex = intersects[0].faceIndex;
    var faceIndex2 = faceIndex + (-1) ** (faceIndex); //face index for the other relevant face

    //console.log(faceIndex);
    //console.log(faceIndex2);

    //Center colors cant be changed
    if (Object.values(Centers).includes(faceIndex)) return;

    //update color
    var nextColor = getNextColor(cube.geometry.faces[faceIndex].color.getHex());
    cube.geometry.faces[faceIndex].color.setColorName(nextColor);
    cube.geometry.faces[faceIndex2].color.setColorName(nextColor);
    cube.geometry.colorsNeedUpdate = true;  //If you dont do this, colors dont update 
  }

  /**
   * Get next color based on Hex code for cur color
   */
  function getNextColor(curColor) {
    if (curColor == THREE.Color.NAMES.gray) {
      return 'white'
    } else if (curColor == THREE.Color.NAMES.white) {
      return 'yellow'
    } else if (curColor == THREE.Color.NAMES.yellow) {
      return 'blue'
    } else if (curColor == THREE.Color.NAMES.blue) {
      return 'green'
    } else if (curColor == THREE.Color.NAMES.green) {
      return 'red'
    } else if (curColor == THREE.Color.NAMES.red) {
      return 'orange'
    } else if (curColor == THREE.Color.NAMES.orange) {
      return 'white'
    }


  }



  /**
   * set mouse pressed to true
   */
  function mouseDown(event) {
    mousePressed = true;
  }

  /**
   * set mouse pressed to false
   */
  function mouseUp(event) {
    mousePressed = false;
  }



  /**
 * Generate cube object that will be sent as json to server
 * Returns null if there are missing pieces
 * The format of each color array is the following:
 *        up
 *       0 1 2 
 * left  3 4 5 right
 *       6 7 8
 *       down
 */
  function generateCubeObect() {

    var cubeObject = {
      "w": {
        "up": "g",
        "right": "o",
        "down": "b",
        "left": "r",
        "colors": []
      },
      "y": {
        "up": "b",
        "right": "o",
        "down": "g",
        "left": "r",
        "colors": []
      },
      "b": {
        "up": "w",
        "right": "o",
        "down": "y",
        "left": "r",
        "colors": []
      },
      "g": {
        "up": "w",
        "right": "r",
        "down": "y",
        "left": "o",
        "colors": []
      },
      "o": {
        "up": "w",
        "right": "g",
        "down": "y",
        "left": "b",
        "colors": []
      },
      "r": {
        "up": "w",
        "right": "b",
        "down": "y",
        "left": "g",
        "colors": []
      }
    };


    for (var i = 0; i < Object.keys(Centers).length; i += 2) {  //if the +2 is confusing, see how Centers is structured
      var curFace = Object.keys(Centers)[i];

      var curFaceCenterInex = Centers[curFace];   //index of center piece of current face
      curFace = curFace.substring(0, 1); //get only the first letter of the color, this is how it is prefresented in the cubeObject

      for (var j = curFaceCenterInex - 8; j <= curFaceCenterInex + 8; j += 2) { //j+=2 because each piece has to faces in the cube object
        var curPieceColor = colorHexToString(cube.geometry.faces[j].color.getHex());
        if (curPieceColor == "gray") { return null; }
        else {
          cubeObject[curFace].colors.push(curPieceColor);
        }
      }

    }
    return cubeObject;

  }


  /**
 * Converts hex color value to string
 */
  function colorHexToString(curColor) {
    if (curColor == THREE.Color.NAMES.gray) {
      return 'gray'
    } else if (curColor == THREE.Color.NAMES.white) {
      return 'w'
    } else if (curColor == THREE.Color.NAMES.yellow) {
      return 'y'
    } else if (curColor == THREE.Color.NAMES.blue) {
      return 'b'
    } else if (curColor == THREE.Color.NAMES.green) {
      return 'g'
    } else if (curColor == THREE.Color.NAMES.red) {
      return 'r'
    } else if (curColor == THREE.Color.NAMES.orange) {
      return 'o'
    }
  }


  /**
   * Action taken when solve button is clicked
   */
  function solveCube(){
    var cubeObject = generateCubeObect(cube)
    sendCubeToServer(cubeObject)
  }

  //mouse event listeners
  canvas.addEventListener('mousemove', onMouseMove, false);
  canvas.addEventListener('mousedown', mouseDown, false);
  canvas.addEventListener('mouseup', mouseUp, false);
  canvas.addEventListener('mouseup', onMouseClick, false);
  solveBtn.addEventListener("click", solveCube);


  //run animation function
  animate();
}



/**
 * Send request to server to solve cube
 */
function sendCubeToServer(cubeObject) {

  if (cubeObject == null){
      alert("Error: Cube not completed");
      return;
  }


  // POST
  fetch('/solve', {

      // Specify the method
      method: 'POST',

      headers: {
          'Content-Type': 'application/json;charset=utf-8'
      },
      body: JSON.stringify(cubeObject)
  }).then(function (response) {
      return response.text();
  }).then(function (text) {

      //Here it should display solution :)
      solution = JSON.parse(text)
      if (!solution.valid){
        alert('Invalid input');
      }
      else{
        drawSolution(solution.solution)
      }

      //console.log('POST response: ');
      //console.log(text);
  });

}



createCubeAnimation();