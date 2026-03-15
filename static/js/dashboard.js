async function loadDashboard() {

    const statsResponse = await fetch('/api/stats');

    const stats = await statsResponse.json();

    document.getElementById('total-users').textContent = stats.total_threats;
    document.getElementById('avg-score').textContent = stats.average_abuse_score;
    document.getElementById('latest-threats').textContent = 
        stats.latest_threat.ip_address + ' (' + stats.latest_threat.country_code + ')';

    const countries = Object.keys(stats.top_countries);
    const c