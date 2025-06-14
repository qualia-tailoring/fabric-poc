<!DOCTYPE html>
<html>
<head>
  <title>織り判別ミニアプリ</title>
  <meta charset="UTF-8">
  <script src="https://static.line-scdn.net/liff/edge/2/sdk.js"></script>
  <script>
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
    let diagnosisResult = "";

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
          diagnosisResult = data.result;
          document.getElementById("quiz").style.display = "none";
          document.getElementById("result").textContent = `あなたの織り方は「${diagnosisResult}」かもしれません`;
          document.getElementById("confirmation").style.display = "block";
        })
        .catch(error => {
          console.error("診断エラー:", error);
          document.getElementById("result").textContent = "診断中にエラーが発生しました。";
        });
      }
    }

    function confirmResult(value) {
      document.getElementById("confirmation").style.display = "none";

      if (value === "yes") {
        document.getElementById("result").textContent += "（ユーザーも納得しています）";
      } else {
        document.getElementById("feedback").style.display = "block";
      }
    }

    function submitFeedback() {
      const userText = document.getElementById("userFeedback").value;

      fetch("/api/feedback", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          expected: userText,
          predicted: diagnosisResult,
          answers: answers
        })
      })
      .then(() => {
        document.getElementById("feedback").innerHTML = "<p>ご意見ありがとうございます！</p>";
      })
      .catch(error => {
        console.error("フィードバック送信エラー:", error);
        document.getElementById("feedback").innerHTML = "<p>送信中にエラーが発生しました。</p>";
      });
    }

    window.onload = initializeApp;
  </script>
</head>
<body>
  <h2>生地診断PoC</h2>
  <label>生地のイメージをヒアリングします</label>

  <div id="quiz">
    <p id="question"></p>
    <button onclick="submitAnswer('yes')">はい</button>
    <button onclick="submitAnswer('no')">いいえ</button>
  </div>

  <p id="result"></p>

  <!-- 結果確認（はい・いいえ） -->
  <div id="confirmation" style="display:none;">
    <p>この診断結果は合っていますか？</p>
    <button onclick="confirmResult('yes')">はい</button>
    <button onclick="confirmResult('no')">いいえ</button>
  </div>

  <!-- フィードバック -->
  <div id="feedback" style="display:none;">
    <p>どの織り方をイメージしていましたか？</p>
    <input type="text" id="userFeedback" placeholder="例: サテン、鹿の子など">
    <button onclick="submitFeedback()">送信</button>
  </div>
</body>
</html>
