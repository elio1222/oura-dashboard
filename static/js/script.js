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
        let scores = [];
        let dates = [];

        // data.data is the array of sleep entries
        for (let i = 0; i < data.data.length; i++) {
            scores.push(data.data[i].score);
            dates.push(data.data[i].day);
        }

        /* check what got stored
        for (let i = 0; i < scores.length; i++) {
            console.log("Date:", dates[i], "Score:", scores[i]);
        }
        */
        createPlot(scores, dates)
    })
    .catch(error => console.error("Error fetching data:", error));
}

function createPlot(scoresArray, datesArray) {
    let myChart = document.getElementById('testing').getContext('2d');

    let sevenScoresChart = new Chart(myChart, {
        type: 'line',
        data: {
            labels: datesArray,
            datasets: [{
                label: 'Scores',
                data: scoresArray,
            }]
        }
    })
}

function sleepTimes() {
    fetch("/oura/api/sleeptimes")
    .then(responese => responese.json())
    .then(data => {
        let times = [];

        for (let i = 0; i < data.length; i++) {
            times.push(Number(data.data[i].total_sleep_duration) / 60 / 60);
        }
        for (let i = 0; i < times.length; i++) {
            console.log(times[i]);
        }
    })
    .catch(error => console.error("Error fetching data:", error));
    
}

sleepTimes();
testing();
console.log('here');
