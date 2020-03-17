/**
 * Create object with pictures for each rubiks move
 */
function creeatePicturesObject(){

    imgObj = Object();

    var colors = ['r', 'o', 'g', 'b', 'w', 'y'];
    var modes = ['', 'p', '2'];
    for (var i= 0; i < colors.length; i++){
        for (var j = 0; j < modes.length; j++){
            var id = colors[i]+modes[j];
            var img=document.getElementById(id);
            imgObj[id] = img;
        }
    }
    return imgObj;
}

/**
 * Draw solution
 */
function drawSolution(solution){

    const PICTURESIZE = 100 //dimension of each picture

    //canvas
    var canvasSol = document.getElementById("solCanvas"); 
    var context = canvasSol.getContext("2d"); 
    context.clearRect(0, 0, canvasSol.width, canvasSol.height); //clear canvas

    //buttons
    var nextBtn = document.getElementById('nextBtn') //nextBtn
    var prevBtn = document.getElementById('prevBtn') //prevBtn
    

    var picturesPerCanvas = canvasSol.width*canvasSol.height / PICTURESIZE**2 //number of Pictures that fit in canvas
    var startIndex = 0 //index for first picture in canvas

    var moves = creeatePicturesObject(); //moves contains images for each move
    var numberOfMoves = solution.length; //length of solution

    drawPictures();


    /**
     * Draws next pictures when next btn is clicked
     */
    function drawNext(){
        if (startIndex + picturesPerCanvas >= numberOfMoves)return;

        startIndex += picturesPerCanvas;
        drawPictures()
    }

    /**
     * Draws previous pictures when prev btn is clicked
     */
    function drawPrev(){
        if (startIndex - picturesPerCanvas < 0)return;

        startIndex -= picturesPerCanvas;
        drawPictures()
    }


    /**
     * Draw pictures on canvas
     */
    function drawPictures(){


        if (picturesPerCanvas%1 != 0){
            console.log('Wrong Dimensions');
            return;
        }
        context.clearRect(0, 0, canvasSol.width, canvasSol.height); //clear canvas

        var curIndex = startIndex;
        for (var i = 0; i < picturesPerCanvas; i++){

            if (curIndex >= numberOfMoves){return;}

            var x = (i * PICTURESIZE) % canvasSol.width;
            var y = Math.floor((i * PICTURESIZE) / canvasSol.width) * PICTURESIZE;
            context.drawImage(moves[solution[curIndex]], x, y, PICTURESIZE, PICTURESIZE);
            curIndex++;
        }

    }



    //add listeners
    prevBtn.addEventListener("click", drawPrev);
    nextBtn.addEventListener("click", drawNext);

}



// testSolution = ['r', 'b', 'o2', 'rp', 'wp', 'g', 'y', 'b2', 'b2', 'bp', 'o2'];
// drawSolution(testSolution);

