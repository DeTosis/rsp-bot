window.addEventListener('load', createScheduleGraph)

async function createScheduleGraph() {
    let data;
    try {
        await fetch('http://192.168.0.11:7901', {
            method: 'POST',
            body: 'get-schedules-parsed'
        }).then(async (res) => {
            data = await res.json();
        });
    } catch { }

    const date = new Date();
    const firstDay = new Date(date.getFullYear(), date.getMonth(), 1);
    const days = new Date(date.getFullYear(), date.getMonth(), 0).getDate() + 1;

    let first_week_day = firstDay.getDay();

    first_week_day = first_week_day - 1 >= 0 ? first_week_day - 1 : first_week_day

    // Gathered avalable schedules data processing
    const sch_dates = [];
    for (var i in data) {
        sch_dates.push(dateToReadableFormat(data[i].day));
    }

    let holder = document.getElementById('celendar-holder');
    for (var i = 0; i < 5 * 7; i++) {
        let div = document.createElement('div');
        let span0 = document.createElement('span');
        span0.classList = 'tiny-small-font day-title';

        if (i < first_week_day) {
            div.classList = `day-block day-filler`;
        }
        else if (i > days + 1) {
            div.classList = `day-block day-filler`;
        }
        else {
            const target = new Date(date.getFullYear(), date.getMonth(), i - 1);
            let exists;
            try {
                exists = sch_dates.some(d => d.toISOString() === target.toISOString());
            } catch (ex) {
                console.log(ex)
            }

            if (exists) {
                div.classList = `day-block day-${i} scheduled`
            } else {
                div.classList = `day-block day-${i}`
            }

            span0.textContent = i - 1;
        }

        div.appendChild(span0);
        holder.appendChild(div);
    }
}

function dateToReadableFormat(input) {
    const year = new Date().getFullYear();
    const [day, monthName] = input.split(' ');
    const months = {
        января: 0,
        февраля: 1,
        марта: 2,
        апреля: 3,
        мая: 4,
        июня: 5,
        июля: 6,
        августа: 7,
        сентября: 8,
        октября: 9,
        ноября: 10,
        декабря: 11
    };
    const readable_date = new Date(year, months[monthName], parseInt(day));
    return readable_date;
}