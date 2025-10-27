export async function requestStatus() {
    const pulse_circle = document.getElementById('pulse-circle');
    const status_dot = document.getElementById('dot-status');

    const update_time = document.getElementById('update-time');

    try {
        status_dot.classList.remove('online', 'offline', 'pending');
        pulse_circle.classList.remove('online', 'offline', 'pending');

        status_dot.classList.add('pending');
        pulse_circle.classList.add('pending');

        await fetch('http://192.168.0.11:7901', {
            method: 'POST',
            body: 'isAlive',
        }).then(async (response) => {
            const text = await response.text();

            status_dot.classList.remove('online', 'offline', 'pending');
            pulse_circle.classList.remove('online', 'offline', 'pending');

            if (text == 'True') {
                status_dot.classList.add('online');
                pulse_circle.classList.add('online');
            } else {
                status_dot.classList.add('offline');
                pulse_circle.classList.add('offline');
            }

            const date = new Date();

            let newDate = date.toLocaleDateString();
            newDate = newDate.replaceAll('/', '.');

            let time = date.toLocaleTimeString();
            time = time.replace('AM', '');
            time = time.replace('PM', '');

            update_time.textContent = `${time} | ${newDate}`;
        })
    }
    catch {
        status_dot.classList.remove('online', 'offline', 'pending');
        pulse_circle.classList.remove('online', 'offline', 'pending');

        status_dot.classList.add('offline');
        pulse_circle.classList.add('offline');

        const date = new Date();

        let newDate = date.toLocaleDateString();
        newDate = newDate.replaceAll('/', '.');

        let time = date.toLocaleTimeString();
        time = time.replace('AM', '');
        time = time.replace('PM', '');

        update_time.textContent = `${time} | ${newDate}`;
    }
}