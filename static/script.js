const questions = [
  { key: 'gloss', text: '光沢がありますか？' },
  { key: 'diagonal', text: '斜めの織り目が見えますか？' },
  { key: 'breathable', text: '通気性はありますか？' },
  { key: 'surface', text: '表面に凹凸がありますか？' },
  { key: 'luxury', text: '高級感がありますか？' },
  { key: 'stretch', text: '少し伸縮性がありますか？' }
];

const answers = {};
let current = 0;

async function initializeApp() {
  try {
    await liff.init({ liffId: "2007543263-Q11rq7rm" });
    showQuestion();
  } catch (err) {
    console.error("LIFF初期化失敗:", err);
    document.getElementById("result").textContent = "LIFF初期化に失敗しました。";
  }
}

function showQuestion() {
  const q = questions[current];
  document.getElementById('question').textContent = q.text;
}

function submitAnswer(value) {
  const q = questions[current];
  answers[q.key] = value;

  current++;
  if (current < questions.length) {
    showQuestion();
  } else {
    fetch("/api/infer", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(answers)
    })
    .then(res => res.json())
    .then(data => {
      document.getElementById("quiz").style.display = "none";
      document.getElementById("result").innerHTML = `
        <p>あなたの織り方は「${data.result}」かもしれません</p>
        <p>この診断結果はイメージと合っていましたか？</p>
        <button onclick="submitFeedback(true)">はい</button>
        <button onclick="showCorrectionInput()">いいえ</button>
      `;

      const fb = document.getElementById("feedback");
      fb.style.display = "block";
      fb.dataset.predicted = data.result;
    })
    .catch(error => {
      console.error("診断エラー:", error);
      document.getElementById("result").textContent = "診断中にエラーが発生しました。";
    });
  }
}

function showCorrectionInput() {
  const fb = document.getElementById("feedback");
  fb.style.display = "block";
  const correction = document.getElementById("correction");
  correction.style.display = "block";
}

function submitFeedback(isCorrect) {
  const fb = document.getElementById("feedback");
  const predicted = fb.dataset.predicted;
  const expected = isCorrect ? predicted : document.getElementById("expectedText").value;

  fetch("/api/feedback", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      expected: expected,
      predicted: predicted,
      answers: answers
    })
  }).then(() => {
    fb.innerHTML = "<p>ご協力ありがとうございました！</p>";
  }).catch(err => {
    fb.innerHTML = "<p>送信に失敗しました。</p>";
  });
}

window.onload = initializeApp;
