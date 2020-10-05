const wordList = [];
let score = 0;

// Adds functionality to clicking on the submit button
$(".add-word").on("submit", async function handleClick(evt) {
  evt.preventDefault();
  const $word = $(".word");
  let word = $word.val();
  $word.val("");
  // return nothing if no word is present
  if (!word) {
    return;
  }
  // return message if word attempted has already been succesfully guessed
  if (wordList.includes(word)) {
    return $(".message").text(`You have already found ${word.toUpperCase()}`);
  }
  // sending word to use checking logic in boggle.py
  const response = await axios.get("/check-word", { params: { word: word } });
  let resp = response.data.response;

  // checking to see which response is sent back from server
  if (resp === "not-on-board") {
    return $(".message").text("not on the board");
  } else if (resp === "not-word") {
    return $(".message").text("not a word");
  } else {
    // if the word is valid, place word on board
    wordList.push(word);
    $(".word-list").append(`<li>${word.toUpperCase()}</li>`);
    // add score for words length
    score += word.length;
    $(".score").text(`Score: ${score}`);

    return $(".message").text(
      `${word.toUpperCase()} for ${word.length} points!`
    );
  }
});
// function to start a countdown timer when page is loaded
function timer() {
  let sec = 60;
  const timer = setInterval(function () {
    $(".timer").text(`Remaining Time: ${sec}`);
    sec--;
    if (sec < 0) {
      clearInterval(timer);
      endGame();
    }
  }, 1000);
}
// send points to database nad disable form
async function endGame() {
  $(".add-word :input").prop("disabled", true);
  const response = await axios.post("/post-score", { score });
  console.log(response);
}

window.onload = timer();
