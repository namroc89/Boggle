const wordList = [];
let score = 0;

$(".add-word").on("submit", async function handleClick(evt) {
  evt.preventDefault();
  const $word = $(".word");
  let word = $word.val();
  $word.val("");
  if (!word) {
    return;
  }
  if (wordList.includes(word)) {
    return $(".message").text(`You have already found ${word.toUpperCase()}`);
  }
  const response = await axios.get("/check-word", { params: { word: word } });
  let resp = response.data.response;

  if (resp === "not-on-board") {
    return $(".message").text("not on the board");
  } else if (resp === "not-word") {
    return $(".message").text("not a word");
  } else {
    wordList.push(word);
    $(".word-list").append(`<li>${word.toUpperCase()}</li>`);
    score += word.length;
    $(".score").text(`Score: ${score}`);

    return $(".message").text(
      `${word.toUpperCase()} for ${word.length} points!`
    );
  }
});

function timer() {
  let sec = 20;
  const timer = setInterval(function () {
    $(".timer").text(`Remaining Time: ${sec}`);
    sec--;
    if (sec < 0) {
      clearInterval(timer);
      endGame();
    }
  }, 1000);
}

async function endGame() {
  $(".add-word :input").prop("disabled", true);
  const response = await axios.post("/post-score", { score });
  console.log(response);
}

window.onload = timer();
