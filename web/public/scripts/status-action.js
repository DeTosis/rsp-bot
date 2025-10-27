import { requestStatus } from "./status_request.js";

window.addEventListener('load', () => {
    requestStatus();
})

document.getElementById('status-reload-btn').onclick = async () => {
    await requestStatus();
}