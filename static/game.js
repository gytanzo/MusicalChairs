var score = 0
var currentquestion = 1
var lastquestion = 10

function correct(){
    if(currentquestion < lastquestion) {
    score += 1
    document.getElementById("score").innerHTML = score;

    currentquestion += 1
        document.getElementById("questionsRemaining").innerHTML = currentquestion + " / " + lastquestion;

    }
    else if(currentquestion === lastquestion){
        score += 1
        document.getElementById("score").innerHTML = score;
        currentquestion += 1
    }
}

function wrong(){
    if(currentquestion < lastquestion) {
        currentquestion += 1
        document.getElementById("questionsRemaining").innerHTML = currentquestion + " / " + lastquestion;

    }
    else if(currentquestion === lastquestion){
        document.getElementById("score").innerHTML = score;
        currentquestion += 1
    }
}