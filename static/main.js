Chart.defaults.color = "black";
Chart.defaults.backgroundColor = "blue"


const ctx1 = document.getElementById('myChart1').getContext('2d');
const myChart1 = new Chart(ctx1, {
    type: 'line',
    data: {
        labels: time,
        borderColor: 'pink',
        datasets: [{
            label: 'Текущая загрузка',
            data: value,
            scaleFontColor: "#FFFFFF"
        }]
    },
    options: {
        scales: {
            xAxis: {
                ticks: {
                    maxTicksLimit: 10
                }
            },
            y: {
                beginAtZero: true
            }
        },
        responsive : false
    }
});

const ctx2 = document.getElementById('myChart2').getContext('2d');
const myChart2 = new Chart(ctx2, {
    type: 'line',
    data: {
        labels: average_time,
        datasets: [{
            label: 'Среднее значение за 1 мин',
            data: average_value,
        }]
    },
    options: {
        scales: {
            xAxis: {
                ticks: {
                    maxTicksLimit: 10
                }
            },
            y: {
                beginAtZero: true
            }
        },
        responsive : false
    }
});

 