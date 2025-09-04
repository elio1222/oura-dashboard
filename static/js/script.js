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
        //document.getElementById('lastNightSleepNumber').textContent = data.data[data.data.length-1].score;

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
        canvas = 'deep-sleep-chart';
        createPlot(deep_scores, dates, canvas);
    })
    .catch(error => console.error("Error fetching data:", error));
}

function createPlot(number, day, canvas, type) {
    let myChart = document.getElementById(`${canvas}`).getContext('2d');
    let colorBORDER = null;
    let colorBACKGROUND = null;
    let label = 'Scores'
    if (canvas === 'rem-sleep-chart') {
        colorBORDER = '#f4d35e';
        colorBACKGROUND = '#f4d35e';
    } else if (canvas === 'deep-sleep-chart') {
        colorBORDER = '#06d6a0'
        colorBACKGROUND = '#06d6a0'
    } else if (canvas === 'sleep-time-chart') {
        label = 'Hours'
        colorBORDER = '#8338ec';
        colorBACKGROUND = '#8338ec';
    } else if (canvas === 'main-plot') {
        colorBORDER = '#3a86ff';
        colorBACKGROUND = '#3a86ff';
    }
    let sevenScoresChart = new Chart(myChart, {
        type: 'line',
        data: {
            labels: day,
            datasets: [{
                label: label,
                data: number,
                borderColor: colorBORDER,
                backgroundColor: colorBACKGROUND
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
    
    /*
    const startdate = new Date(document.getElementById('start').value);
    const enddate = new Date(document.getElementById('end').value);
    */

    const startDate = document.getElementById('start');
    const START = startDate.value;

    const endDate = document.getElementById('end');
    const END = endDate.value;
    

    fetch("/submit-date-sleep", {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            start_date: START,
            end_end: END
        })
    })
    .then(res => res.json())
    .then(data => {
        let scores = [];
        let dates = [];
        let canvas = 'main-plot'
        console.log(data);

        for (let i = 0; i < data.data.length; i++) {
            scores.push(data.data[i].score);
            dates.push(data.data[i].day);
        }

        console.log(scores);
        console.log(dates);

        createPlot(scores, dates, canvas);
        /* checks what type of data we got from the backend
        console.log('Response from FLASK: ', data);
        */

    });
}

function getPieChartData() {
    fetch('oura/api/sleep_routes')
    .then(response => response.json())
    .then(data => {
        let rem_sleep = [];
        let deep_sleep = [];
        let light_sleep = [];
        let awake_time = [];

        let all_sleep_times = [];


        for (let i = 0; i < data.data.length; i++) {
            let total_rem_sleep = Number(data.data[i].rem_sleep_duration) / 60 / 60;
            total_rem_sleep = total_rem_sleep.toFixed(2);
            total_rem_sleep = Number(total_rem_sleep);
            all_sleep_times.push(total_rem_sleep);
            let total_deep_sleep = Number(data.data[i].deep_sleep_duration) / 60 / 60;
            total_deep_sleep = total_deep_sleep.toFixed(2);
            all_sleep_times.push(Number(total_deep_sleep));
            let total_light_sleep = Number(data.data[i].light_sleep_duration) / 60 /60;
            total_light_sleep = total_light_sleep.toFixed(2);
            all_sleep_times.push(Number(total_light_sleep));
            let total_awake_time = Number(data.data[i].awake_time) / 60 / 60;
            total_awake_time = total_awake_time.toFixed(2);
            all_sleep_times.push(Number(total_awake_time));


        }

        for (let i = 0; i < awake_time.length; i++) {
            console.log(awake_time[i]);
        }
        createPieChart(all_sleep_times);
    })
}

function createPieChart(all_sleep_times) {
    let myChart = document.getElementById('pie');   
    let pieChart = new Chart(myChart, {
        type: 'pie',
        data: {
            labels: ['Awake Time', 'Light Sleep', 'Deep Sleep', 'REM Sleep'],
            datasets: [
                {
                    label: 'Dataset1',
                    data: all_sleep_times,
                    backgroundColor: ['#f4d35e','#ef476f', '#06d6a0', '#ff9f1c'],
                    borderColor: 
                    ['#f4d35e','#ef476f', '#06d6a0', '#ff9f1c']
            
                }

            ]
        },
        options: {
            responsive: true,
            layout: {
                padding: 20
            },
            plugins: {
                legend: {
                    position: 'top',
                },
                title: {
                    display: true,
                    text: 'Sleep Breakdown'
                }
            }
        },

    })
}

getPieChartData();
mainChart();
sleepTimes();
testing();
