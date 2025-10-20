window.addEventListener('load', () => {
    requestRecent();
})

async function requestRecent() {
    const recent = document.getElementById('recent-list');
    while (recent.firstChild) {
        recent.removeChild(recent.firstChild);
    }

    try {
        await fetch('http://192.168.0.11:7901', {
            method: 'POST',
            body: 'get-recent'
        }).then(async (res) => {
            const data = await res.json();

            for (var i in data) {
                let li = document.createElement('li');
                let div0 = document.createElement('div');
                let div1 = document.createElement('div');
                let div2 = document.createElement('div');

                let span0 = document.createElement('span');
                let span1 = document.createElement('span');
                let span2 = document.createElement('span');
                let span3 = document.createElement('span');

                div0.classList = 'recent-user-data';
                div1.classList = 'recent-timestamp';
                div2.classList = 'recent-message';

                span0.classList = 'recent-name .auto-text';
                span1.classList = 'recent-id';
                span2.classList = 'recent-timestamp';
                span3.classList = 'recent-msg';

                span0.textContent = data[i].name;
                span1.textContent = data[i].id;

                let text_data = data[i].timestamp.split(' ');

                span2.textContent = text_data[1] + ' | ' + text_data[0];
                span3.textContent = data[i].msg;

                div0.appendChild(span0);
                div0.appendChild(span1);

                div1.appendChild(span2);

                div2.appendChild(span3);

                li.classList = 'recent-item';

                li.appendChild(div0);
                li.appendChild(div1);
                li.appendChild(div2);

                recent.appendChild(li);
            }

        });
    } catch { }
}