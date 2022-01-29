const ctx = document.getElementById('myChart').getContext('2d');
const myChart = new Chart(ctx, {
    type: 'line',
    data: {
        labels: time,
        datasets: [{
            label: '# of Votes',
            data: values,
        }]
    },
    options: {
        scales: {
            y: {
                beginAtZero: true
            }
        },
        responsive : false
    }
});