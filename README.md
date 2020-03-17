This project consists on a Flask application to solve the Rubik's cube using the beginner's method.
The application is deployed <a href="https://rubikscubewebapp.herokuapp.com/" target="_blank"> here</a>.

I used the JavaScript library <a href="https://threejs.org/" target="_blank">Three.js</a> to create 
a 3d animation of the Rubik's cube where the user can enter the state of the cube. 
When the user clicks on the 'solve' button, the input will be sent to the python server, which (if the
input is valid) will compute the solution using the beginner's method, and then, the computed solution 
will be displayed. 

Current Limitations:
- Currently, the only cube solving algorithm I have implemented is the beginner's method which takes a lot of moves to solve the cube. I will potentially implement more powerful, algorithms in the future.
