
document.getElementById('bt0').onclick = () => {
    fetch('http://localhost:7901', {
        method: 'POST',
        body: 'stopBot',
    })
}

document.getElementById('bt1').onclick = () => {
    fetch('http://localhost:7901', {
        method: 'POST',
        body: 'startBot',
    })
}
