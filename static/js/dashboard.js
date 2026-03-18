async function loadDashboard() {

    const statsResponse = await fetch('/api/stats');

    const stats = await statsResponse.json();

    document.getElementById('total-threats').textContent = stats.total_threats;
    document.getElementById('avg-score').textContent = stats.average_abuse_score;
    document.getElementById('latest-threat').textContent = 
        stats.latest_threat.ip_address + ' (' + stats.latest_threat.country_code + ')';

    const countries = Object.keys(stats.top_countries);
    const counts = Object.values(stats.top_countries);


    new Chart(document.getElementById('countryChart'), {
        type: 'bar',
        data: {
            labels: countries,
            datasets: [{ // array of data series to plot 
                label: 'Threats',
                data: counts,
                backgroundColor: '#f85149',
                borderRadius: 4
            }]
        },

        options: { //customize the chart's appearance and behavior
            plugins: {
                legend: { display: false }
            },
            scales: {
                x: {
                    ticks: {color : '#8b949e'},
                    grid: {color : '#21262d'}
                },

                y: {
                    ticks: {color : '#8b949e'},
                    grid: {color : '#21262d'}
                }
            }
        }
    });


    const threatsResponse = await fetch('/api/threats');
    const threats = await threatsResponse.json();

    const tbody = document.getElementById('threats-table');
    tbody.innerHTML = ''; //clears the loading message by setting the inner html to empty
    

    threats.forEach(threat => {
        const row = document.createElement('tr');
        row.innerHTML = `
        <td>${threat.ipAddress}</td>
        <td>${threat.countryCode}</td>
        <td><span class="badge">${threat.abuseConfidenceScore}</span></td>
            <td>${threat.lastReportedAt.split('T')[0]}</td>
        `;
        tbody.appendChild(row);
    });
    

}
loadDashboard();
 

