/**
 * Разбивает график на сессии, приводит время в формат "ЧЧ:ММ"
 * @param {Array} arr_time массив записей времени
 * @param {Array} arr_value массив записей величины загрузки ЦП
 * @param {number} interval интервал внесения записей в БД
 * @returns массив, содержащий массив записей времени и массив
 * записей величины загрузки ЦП
 */
function split_into_sessions(arr_time, arr_value, interval) {
    time_in_sessions = [];
    value_in_sessions = [];
    for(let i=0; i<arr_time.length; i++) {
        // если разница между записями времени больше, чем полтора
        // значения интервала
        if((arr_time[i] != arr_time[0]) && (arr_time[i] - arr_time[i-1]) > interval*1.5) {
            // добавляем null для разделения сеансов записей в БД
            time_in_sessions.push(null, arr_time[i]);
            value_in_sessions.push(null, arr_value[i]);
        } else {
            time_in_sessions.push(arr_time[i]);
            value_in_sessions.push(arr_value[i]);
        }
    }
    for(let i=0; i<time_in_sessions.length; i++) {
        if(time_in_sessions[i]==null) {continue};
        // преобразуем дату из Unix time в строковые значения формата "ЧЧ:ММ"
        time_in_sessions[i] = new Date(time_in_sessions[i]);
        time_in_sessions[i] = `${time_in_sessions[i].toTimeString().slice(0, 5)}`
    };
    return [time_in_sessions, value_in_sessions];
}

/**
 * Создает графики
 * @param {string} chart_id 
 * @param {Array} arr_time 
 * @param {Array} arr_value 
 */
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
                        maxTicksLimit: 6
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
// время и величина загрузки ЦП для первого графика
let time_for_chart = data[0];
let value_for_chart = data[1];
let interval_for_2_chart = 60000 // интервал для отображения на втором графике
let average_data = split_into_sessions(average_time, average_value, interval_for_2_chart);
// // время и величина загрузки ЦП для второго графика
let average_time_for_chart = average_data[0];
let average_value_for_chart = average_data[1];

Chart.defaults.color = "black";
Chart.defaults.backgroundColor = "blue"

let chart1 = create_chart('myChart1', time_for_chart, value_for_chart);
let chart2 = create_chart('myChart2', average_time_for_chart, average_value_for_chart)
