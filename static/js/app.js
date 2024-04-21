document.getElementById("userForm").onsubmit = function (event) {
  event.preventDefault();
  const formData = new FormData(this);
  fetch("/", { method: "POST", body: formData })
    .then((response) => response.text())
    .then((data) => {
      const chatbox = document.getElementById("chatbox");
      chatbox.innerHTML += "<div>" + data + "</div>";
      chatbox.scrollTop = chatbox.scrollHeight; // 滚动到最底部
    });
};
