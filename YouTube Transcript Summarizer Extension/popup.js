const button = document.querySelector('#btn');
const result = document.querySelector('#summary');
const container = document.querySelector('.container');
const loader = document.querySelector('.loader');
const heading = document.querySelector('#heading');

function summarize() {
    chrome.tabs.query({ active: true, currentWindow: true }, function (tabs) {
        chrome.tabs.sendMessage(tabs[0].id, 'send-summary', function (response) { });
    });
}

chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    loader.style = "display:none";
    result.innerText = message;
});

function styleChanges() {
    button.style = "display:none";
    container.style = "width: 300px; height: 250px; font-weight: 400";
    heading.style = "display:block";
    loader.style = "display:block";
}

button.addEventListener('click', () => {
    try {
        styleChanges();
        summarize();
    }
    catch (err) {
        console.log(err.message);
    }

});