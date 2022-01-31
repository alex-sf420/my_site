function split_into_sessions(arr_time, arr_value, interval) {
    time_in_sessions = [];
    value_in_sessions = [];
    for(let i=0; i<arr_time.length; i++) {
        if((arr_time[i] != arr_time[0]) && (arr_time[i] - arr_time[i-1]) > interval*1.5) {
            time_in_sessions.push(null, arr_time[i]);
            value_in_sessions.push(null, arr_value[i]);
            console.log('я тут')
        } else {
            time_in_sessions.push(arr_time[i]);
            value_in_sessions.push(arr_value[i]);
        }
    }
    return [time_in_sessions, value_in_sessions];
}

function create_chart(chart_id, arr_time, arr_value) {
    const ctx = document.getElementById(chart_id).getContext('2d');
    const myChart = new Chart(ctx, {
        type: 'line',
        data: {
            labels: arr_time,
            datasets: [{
                label: 'Текущая загрузка',
                data: arr_value,
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
    })
};

let data = split_into_sessions(time, value, interval);
let time_for_chart = data[0];
let value_for_chart = data[1];
let average_data = split_into_sessions(average_time, average_value, interval);
let average_time_for_chart = average_data[0];
let average_value_for_chart = average_data[1];
console.log('value_for_chart', value_for_chart)
console.log('time_for_chart', time_for_chart)
console.log('average_time_for_chart', average_time_for_chart)
console.log('average_value_for_chart', average_value_for_chart)

Chart.defaults.color = "black";
Chart.defaults.backgroundColor = "blue"

let chart1 = create_chart('myChart1', time_for_chart, value_for_chart);
let chart2 = create_chart('myChart2', average_time_for_chart, average_value_for_chart)
