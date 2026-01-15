const panel = document.getElementById("aiMentorPanel");
document.getElementById("aiMentorToggle").onclick = () =>
  panel.classList.toggle("hidden");

function updateAIMentorPanel(data) {
  document.getElementById("aiOutput").innerText =
    JSON.stringify(data, null, 2);
}
