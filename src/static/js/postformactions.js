function renderTextareaField() {
    const group = document.getElementById("group").value;
    let textareaContainer = document.getElementById("textareaContainer");
    textareaContainer.innerHTML = "";

    let textareaElement = document.createElement("textarea");
    textareaElement.id = "text";
    textareaElement.name = "text";
    textareaElement.rows = "10";
    textareaElement.className="form-control";
    if (group == 'articles') {
        textareaElement.placeholder="5000 characters max";
        textareaElement.maxlength="5000";
    }
    else if (group == 'news') {
        textareaElement.placeholder="500 characters max";
        textareaElement.maxlength="500";
    }
    textareaContainer.appendChild(textareaElement);
}

renderTextareaField()
