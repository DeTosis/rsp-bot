import { requestStatus } from "./status_request.js";

document.getElementById('shutdown-btn').onclick = async () => {
    shutdown();
}

async function shutdown() {
    try {
        await fetch('http://192.168.0.11:7901', {
            method: 'POST',
            body: 'stopBot',
        }).then(async (response) => {
            let data = await response.json();
            console.log(data);
            requestStatus();
        });
    } catch { }
}