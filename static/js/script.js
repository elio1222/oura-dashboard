function generatePlot() {
    fetch("/database")
    .then(response => response.json())
    .then(data => {
        // seperating the sleep scores and dates from data
        let scores = []
        let dates = []

        for (let i = 0; i < data.length; i++) {
            scores.push(data[i][0]);
            dates.push(data[i][1]);
        }
    })
}

/* old code
function testing() {
    fetch("/oura/api")
    .then(response => response.json())
    .then(data => {
        let scores = []
        let dates = []

        console.log(data);

        for (let i = 0; i < data.length; i++) {
            scores.push(data[i]['data']['score']);
            dates.push(data[i]['data']['day']);
        }
        for (let i = 0; i < scores.length; i++) {
            console.log(scores[i]);
            console.log(dates[i]);
        }
    })
}
*/

//chatgpt code
function testing() {
    fetch("/oura/api/daily_sleep")
    .then(response => response.json())
    .then(data => {
        let rem_scores = [];
        let deep_scores = [];
        let dates = [];
        let canvas = 'rem-sleep-chart';
        let canvas2 = 'deep-sleep-chart';
        document.getElementById('lastNightSleepNumber').textContent = data.data[data.data.length-1].score;

        // data.data is the array of sleep entries
        for (let i = 0; i < data.data.length; i++) {
            rem_scores.push(data.data[i].contributors.rem_sleep);
            deep_scores.push(data.data[i].contributors.deep_sleep);
            dates.push(data.data[i].day);
        }

        /* check what got stored
        for (let i = 0; i < scores.length; i++) {
            console.log("Date:", dates[i], "Score:", scores[i]);
        }
        */
        createPlot(rem_scores, dates, canvas);
        createPlot(deep_scores, dates, canvas2);
    })
    .catch(error => console.error("Error fetching data:", error));
}

function createPlot(number, day, canvas) {
    let myChart = document.getElementById(`${canvas}`).getContext('2d');

    let sevenScoresChart = new Chart(myChart, {
        type: 'line',
        data: {
            labels: day,
            datasets: [{
                label: 'Scores',
                data: number,
            }]
        }
    })
}

function sleepTimes() {
    fetch("/oura/api/sleeptimes")
    .then(responese => responese.json())
    .then(data => {
        let times = [];
        let dates = [];
        let canvas = 'sleep-time-chart';

        for (let i = 0; i < data.data.length; i++) {
            let totalSleepDuration = Number(data.data[i].total_sleep_duration) / 60 / 60;
            totalSleepDuration = totalSleepDuration.toFixed(2);
            totalSleepDuration = Number(totalSleepDuration);
            times.push(totalSleepDuration);
            dates.push(data.data[i].day);
        }
        
        createPlot(times, dates, canvas);
    })
    .catch(error => console.error("Error fetching data:", error));
    
}

function mainChart() {
    const today = new Date();
    const year = today.getFullYear();
    const month = String(today.getMonth() + 1).padStart(2, '0');
    const day = String(today.getDate()).padStart(2, '0');
    const formattedDate = `${year}-${month}-${day}`;
    document.getElementById('end').setAttribute('max', formattedDate);
    document.getElementById('start').setAttribute('max', formattedDate);
    
    const startdate = new Date(document.getElementById('start').value);
    const endate = new Date(document.getElementById('end').value);

    fetch("/submit-date-sleep", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify(startdate)
    })
    .then(res => res.json())
    .then(data => {
        console.log('Response from FLASK: ', data);
    });
}

mainChart();
sleepTimes();
testing();
console.log('here');
