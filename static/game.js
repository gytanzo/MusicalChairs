var score = 0
var currentquestion = 1
var lastquestion = 10

function pressedA(answerKey){
    var value = answerKey[0];

    if (value == 0) {
        return correct();
    }

    else {
        return wrong();
    }
}

function pressedB(answerKey){
    var value = answerKey[1];

    if (value == 0) {
        return correct();
    }

    else {
        return wrong();
    }
}

function pressedC(answerKey){
    var value = answerKey[2];

    if (value == 0) {
        return correct();
    }

    else {
        return wrong();
    }
}

function pressedD(answerKey){
    var value = answerKey[3];

    if (value == 0) {
        return correct();
    }

    else {
        return wrong();
    }
}

function correct(){
    let answerKey;
    if(currentquestion < lastquestion) {
        score += 1
        document.getElementById("score").innerHTML = score;

        currentquestion += 1
        document.getElementById("questionsRemaining").innerHTML = currentquestion + " / " + lastquestion;

        answerKey = setAnswers();
        return answerKey;
    }

    else if(currentquestion === lastquestion){
        score += 1
        document.getElementById("score").innerHTML = score;
        currentquestion += 1
    }
}

function wrong(){
    let answerKey;
    if(currentquestion < lastquestion) {
        currentquestion += 1
        document.getElementById("questionsRemaining").innerHTML = currentquestion + " / " + lastquestion;

        answerKey = setAnswers();
        return answerKey;
    }
    else if(currentquestion === lastquestion){
        document.getElementById("score").innerHTML = score;
        currentquestion += 1
    }
}

var x;
function countdownTime() {
    var time = 30;
    clearInterval(x);
    x = setInterval(function() {
        document.getElementById("countdown").innerHTML = time;
        time -= 1;
        if(time == 0) {
            clearInterval(x);
            document.getElementById("countdown").innerHTML = "FAILED";
        }
    }, 1000);
}