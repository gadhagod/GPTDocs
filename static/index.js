const responseBox = document.getElementById("response-box")
const questionBox = document.getElementById("question-box")
const submitBtn = document.getElementById("submit-btn")

submitBtn.addEventListener("click", async () => {
    let formData = new FormData();
    formData.append("question", questionBox.value);
    const res = await (await fetch(window.location.origin, {
        method: "POST",
        body: formData/*JSON.stringify({
            "question": questionBox.value
        })*/
    })).json();
    responseBox.innerText = res.response
})