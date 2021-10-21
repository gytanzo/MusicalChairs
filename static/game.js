var score = 0
var currentquestion = 1
var lastquestion = 10

function correct(answerKey){
    console.log(answerKey)
    if(currentquestion < lastquestion) {
        score += 1
        document.getElementById("score").innerHTML = score;

        currentquestion += 1
        document.getElementById("questionsRemaining").innerHTML = currentquestion + " / " + lastquestion;

        answerKey = setAnswers();
    }

    else if(currentquestion === lastquestion){
        score += 1
        document.getElementById("score").innerHTML = score;
        currentquestion += 1
    }
}

function wrong(answerKey){
    console.log(answerKey)
    if(currentquestion < lastquestion) {
        currentquestion += 1
        document.getElementById("questionsRemaining").innerHTML = currentquestion + " / " + lastquestion;

        answerKey = setAnswers();
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