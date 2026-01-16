// Dashboard functions
let minerStatus = {
    drops: false,
    points: false,
    uptime: 0
};

function startMiner() {
    fetch('/api/start', {method: 'POST'})
        .then(r => r.json())
        .then(data => {
            alert('Miner started!');
            updateStatus();
        })
        .catch(e => alert('Error: ' + e));
}

function stopMiner() {
    fetch('/api/stop', {method: 'POST'})
        .then(r => r.json())
        .then(data => {
            alert('Miner stopped!');
            updateStatus();
        })
        .catch(e => alert('Error: ' + e));
}

function updateStatus() {
    fetch('/api/status')
        .then(r => r.json())
        .then(data => {
            if(data.drops) {
                document.getElementById('drops-status').textContent = data.drops.status || 'Running';
                if(data.drops.progress) {
                    document.getElementById('drops-progress').style.width = data.drops.progress + '%';
                }
            }
            if(data.points) {
                document.getElementById('points-status').textContent = data.points.status || 'Running';
                document.getElementById('points-earned').textContent = data.points.earned || '0';
            }
        })
        .catch(e => console.error('Status error:', e));
}

function openSettings() {
    window.location.href = '/settings';
}

// Update status every 5 seconds
setInterval(updateStatus, 5000);

// Initial status load
window.addEventListener('load', function() {
    updateStatus();
});
