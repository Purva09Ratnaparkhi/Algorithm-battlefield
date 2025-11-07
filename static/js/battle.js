/* Battle Page Specific JavaScript */

let battleInProgress = false;
let result1 = null;
let result2 = null;

function startBattle() {
    if (battleInProgress) return;
    
    battleInProgress = true;
    console.log('Starting battle...');
    
    // Show progress bars
    document.querySelectorAll('.progress-section').forEach(section => {
        section.style.display = 'block';
    });
    
    // Reset and start animations
    const barFills = document.querySelectorAll('.bar-fill');
    barFills.forEach(bar => {
        bar.style.animation = 'none';
        setTimeout(() => {
            bar.style.animation = 'barFill 3s ease-in-out';
        }, 10);
    });
    
    // Execute algorithms
    executeBattle();
}

function executeBattle() {
    $.ajax({
        url: '/battle',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify({}),
        timeout: 30000,
        success: function(response) {
            if (response.success) {
                result1 = response.result1;
                result2 = response.result2;
                
                console.log('Battle results:', result1, result2);
                
                // Update UI with results
                updateBattleResults();
                
                // Redirect to results page
                setTimeout(() => {
                    window.location.href = '/result';
                }, 2000);
            } else {
                handleBattleError(response.error);
            }
        },
        error: function(xhr, status, error) {
            console.error('Battle error:', error);
            handleBattleError('Battle execution failed: ' + error);
        }
    });
}

function updateBattleResults() {
    // Update Player 1 results
    if (result1.status === 'success') {
        document.getElementById('p1-time').textContent = result1.time + 'ms';
        document.getElementById('p1-memory').textContent = result1.memory + 'KB';
        document.getElementById('p1-stats').style.display = 'block';
        document.querySelector('.player-1-battle .progress-section').innerHTML = '✓ Complete';
    } else {
        document.querySelector('.player-1-battle .progress-section').innerHTML = '✗ Error';
    }
    
    // Update Player 2 results
    if (result2.status === 'success') {
        document.getElementById('p2-time').textContent = result2.time + 'ms';
        document.getElementById('p2-memory').textContent = result2.memory + 'KB';
        document.getElementById('p2-stats').style.display = 'block';
        document.querySelector('.player-2-battle .progress-section').innerHTML = '✓ Complete';
    } else {
        document.querySelector('.player-2-battle .progress-section').innerHTML = '✗ Error';
    }
    
    // Update status text
    document.getElementById('status-text').textContent = 'Battle Complete! Redirecting to results...';
}

function handleBattleError(message) {
    console.error(message);
    document.getElementById('status-text').textContent = 'Error: ' + message;
    battleInProgress = false;
    
    setTimeout(() => {
        // Show retry button
        const retryBtn = document.createElement('button');
        retryBtn.className = 'btn btn-danger mt-3';
        retryBtn.textContent = 'Retry Battle';
        retryBtn.onclick = startBattle;
        document.querySelector('main').appendChild(retryBtn);
    }, 2000);
}

// Add event listeners when page loads
document.addEventListener('DOMContentLoaded', () => {
    // Start battle automatically
    setTimeout(startBattle, 500);
});

// Handle page unload
window.addEventListener('beforeunload', () => {
    if (battleInProgress) {
        return 'Battle in progress. Are you sure you want to leave?';
    }
});
