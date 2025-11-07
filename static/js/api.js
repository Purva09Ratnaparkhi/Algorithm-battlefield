/* API and AJAX Utilities */

const API = {
    // Base URL (adjust if needed)
    baseUrl: window.location.origin,
    
    // Generic POST request
    post: async function(endpoint, data) {
        try {
            const response = await fetch(this.baseUrl + endpoint, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(data)
            });
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API POST error:', error);
            throw error;
        }
    },
    
    // Generic GET request
    get: async function(endpoint) {
        try {
            const response = await fetch(this.baseUrl + endpoint);
            
            if (!response.ok) {
                throw new Error(`HTTP ${response.status}`);
            }
            
            return await response.json();
        } catch (error) {
            console.error('API GET error:', error);
            throw error;
        }
    },
    
    // Select category
    selectCategory: function(player, category) {
        return this.post('/select_category', { player, category });
    },
    
    // Select algorithm
    selectAlgorithm: function(player, algorithm) {
        return this.post('/select_algorithm', { player, algorithm });
    },
    
    // Generate random input
    generateInput: function(size, category) {
        return this.post('/input', { 
            action: 'generate', 
            size, 
            category 
        });
    },
    
    // Submit manual input
    submitInput: function(inputText, category) {
        return this.post('/input', { 
            action: 'manual', 
            input_text: inputText, 
            category 
        });
    },
    
    // Execute battle
    battle: function() {
        return this.post('/battle', {});
    }
};

// Global error handler for fetch
window.addEventListener('unhandledrejection', event => {
    console.error('Unhandled promise rejection:', event.reason);
    showNotification('An error occurred. Please try again.', 'danger');
});

// Monitor network connection
window.addEventListener('online', () => {
    showNotification('Connection restored', 'success', 2000);
});

window.addEventListener('offline', () => {
    showNotification('Connection lost. Some features may not work.', 'warning');
});

// Provide offline feedback
if (!navigator.onLine) {
    showNotification('You appear to be offline', 'warning');
}
