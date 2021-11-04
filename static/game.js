var score = 0;
var currentquestion = 1;
var lastquestion = 10;

function pressedA(answerKey) {
    var value = answerKey[0];
    if (value == 0) return correct();
    else return wrong();
}

function pressedB(answerKey) {
    var value = answerKey[1];
    if (value == 0) return correct();
    else return wrong();
}

function pressedC(answerKey) {
    var value = answerKey[2];
    if (value == 0) return correct();
    else return wrong();
}

function pressedD(answerKey) {
    var value = answerKey[3];
    if (value == 0) return correct();
    else return wrong();
}

function correct() {
    let answerKey;
    if (currentquestion < lastquestion) {
        score = calculateScore(score);
        document.getElementById("score").innerHTML = score;

        currentquestion += 1
        document.getElementById("questionsRemaining").innerHTML = currentquestion + " / " + lastquestion;

        answerKey = setAnswers();
        return answerKey;
    }

    else if (currentquestion === lastquestion) {
        score = calculateScore(score);
        document.getElementById("score").innerHTML = score;
        currentquestion += 1

        // Sends score to backend
        storeScore(score);
    }
}

function wrong() {
    let answerKey;
    if (currentquestion < lastquestion) {
        currentquestion += 1
        document.getElementById("questionsRemaining").innerHTML = currentquestion + " / " + lastquestion;

        answerKey = setAnswers();
        return answerKey;
    }
    else if (currentquestion === lastquestion) {
        currentquestion += 1

        // Sends score to backend
        storeScore(score);
    }
}
// Below here is where a POST request will be sent to Python
// In order to store the final score into MongoDB
function storeScore(score) {
    const req = new XMLHttpRequest();
    score = JSON.stringify(score)
    req.open('POST', '/store/'+score);
    req.onload = () => {
        console.log(req.responseText)
    }
    req.send();
}
var x;
function countdownTime() {
    if (currentquestion == 11) { // If the user has answered all ten questions stop resetting the timer.~
        document.getElementById("countdown").innerHTML = "DONE";
        window.location.href = "endofgame.html?score=" + score;
        return; // This doesn't stop the music, which I guess it should, but that's much more work to accomplish. This is just a simple solution until Andrew makes a post-game page. 
    }

    var time = 31;
    clearInterval(x);
    test();
    x = setInterval(test, 1000);

    function test() {
        time -= 1;
        document.getElementById("countdown").innerHTML = time;
        if (time == 0) {
            clearInterval(x);
            answerKey = wrong(); // If they run out of time, move on to the next question.
            countdownTime(); 
            return answerKey;
        }
    }

    return answerKey; // By default, return the answerKey completely unchanged. 
}

function calculateScore(prevScore) {
    // Calculated Score = 1*e^(.1535t), where t = number of seconds remaining
    var time = parseInt(document.getElementById("countdown").innerHTML);
    var a = .1535 * time // .1535t
    var b = Math.round(1 * Math.exp(a)); // 1*e^.1535t
    var newScore = prevScore + b; // prevScore + 1e^.1535t
    return newScore;
}

/* The main functionality for playgame.html that was originally in the file but moved to here */

var A;
var B;
var C;
var D;

// Source: https://stackoverflow.com/questions/4959975/generate-random-number-between-two-numbers-in-javascript
function randomIntFromInterval(min, max) { // min and max included 
    return Math.floor(Math.random() * (max - min + 1) + min)
}

function setAnswers() {
    var row = randomIntFromInterval(0, 39); // Grab the CSV row the player will be asked. 

    // These values will be used to make sure that we don't make two buttons the same answer.
    var assignedCorrect = false;
    var assignedIncorrect1 = false;
    var assignedIncorrect2 = false;
    var assignedIncorrect3 = false;
    var completeButtons = [-1, -1, -1, -1]; // This array will house the button IDs (0, 1, 2, 3) for the buttons we've added. So if A and C are done, this will be [0, 2]. 

    fetch("../static/songs.json")
        .then(response => {
            return response.json();
        })
        .then(data => {

            // Randomly generate a number between 0 and 3. 
            // If the first number is two, then A = Incorrect 2. 

            let i = 0; // This will count how many times we have added a button. 
            while (i != 4) {
                var value = randomIntFromInterval(0, 3); // Correct = 0, Incorrect1 = 1, Incorrect2 = 2, Incorrect3 = 3
                if (completeButtons[value] != -1) { // If the button has already been assigned
                    ; // Do nothing, get a new value 
                }

                else { // Else
                    if (assignedCorrect == false) { // First value generated is going to be the correct button
                        if (value == 0) {
                            document.getElementById('A').innerHTML = data[row].Correct;
                            completeButtons[0] = 0;
                        }

                        else if (value == 1) {
                            document.getElementById('B').innerHTML = data[row].Correct;
                            completeButtons[1] = 0;
                        }

                        else if (value == 2) {
                            document.getElementById('C').innerHTML = data[row].Correct;
                            completeButtons[2] = 0;
                        }

                        else if (value == 3) {
                            document.getElementById('D').innerHTML = data[row].Correct;
                            completeButtons[3] = 0;
                        }

                        assignedCorrect = true;
                        i++;
                    }

                    else if (assignedIncorrect1 == false) {
                        if (value == 0) {
                            document.getElementById('A').innerHTML = data[row]["Incorrect 1"];
                            completeButtons[0] = 1;
                        }

                        else if (value == 1) {
                            document.getElementById('B').innerHTML = data[row]["Incorrect 1"];
                            completeButtons[1] = 1;
                        }

                        else if (value == 2) {
                            document.getElementById('C').innerHTML = data[row]["Incorrect 1"];
                            completeButtons[2] = 1;
                        }

                        else if (value == 3) {
                            document.getElementById('D').innerHTML = data[row]["Incorrect 1"];
                            completeButtons[3] = 1;
                        }

                        assignedIncorrect1 = true;
                        i++;
                    }

                    else if (assignedIncorrect2 == false) {
                        if (value == 0) {
                            document.getElementById('A').innerHTML = data[row]["Incorrect 2"];
                            completeButtons[0] = 2;
                        }

                        else if (value == 1) {
                            document.getElementById('B').innerHTML = data[row]["Incorrect 2"];
                            completeButtons[1] = 2;
                        }

                        else if (value == 2) {
                            document.getElementById('C').innerHTML = data[row]["Incorrect 2"];
                            completeButtons[2] = 2;
                        }

                        else if (value == 3) {
                            document.getElementById('D').innerHTML = data[row]["Incorrect 2"];
                            completeButtons[3] = 2;
                        }

                        assignedIncorrect2 = true;
                        i++;
                    }

                    else if (assignedIncorrect3 == false) {
                        if (value == 0) {
                            document.getElementById('A').innerHTML = data[row]["Incorrect 3"];
                            completeButtons[0] = 3;
                        }

                        else if (value == 1) {
                            document.getElementById('B').innerHTML = data[row]["Incorrect 3"];
                            completeButtons[1] = 3;
                        }

                        else if (value == 2) {
                            document.getElementById('C').innerHTML = data[row]["Incorrect 3"];
                            completeButtons[2] = 3;
                        }

                        else if (value == 3) {
                            document.getElementById('D').innerHTML = data[row]["Incorrect 3"];
                            completeButtons[3] = 3;
                        }

                        assignedIncorrect3 = true;
                        i++;
                    }
                }
            }

            var source = document.getElementById('audioSource');
            source.src = data[row]["Song URL"]
            var audio = document.getElementById("my_audio");
            audio.volume = .05; // Lower the default audio so your eardrums don't literally explode. You're welcome. 
            audio.load();
            audio.play();
        })

    return completeButtons; // The correct ordering of the buttons gets returned so that the onClick properly works!
}