chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message === 'send-summary') {
        const url = location.href;
        const apiURL = 'http://localhost:5000/api/summarize?youtube_url=' + url;

        fetch(apiURL, {
            method: 'GET',
            mode: 'cors'
        })
            .then((response) => response.json())
            .then((data) => {
                console.log('Success:', data);
                sendSummary(data);
            })
            .catch((error) => {
                console.error('Error:', error);
            });
    }
});

function sendSummary(summary) {
    chrome.runtime.sendMessage(summary, (response) => { });
}