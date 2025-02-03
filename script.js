// Visitor counter
let visitorCount = localStorage.getItem('visitorCount') || 0;
visitorCount = parseInt(visitorCount) + 1;
localStorage.setItem('visitorCount', visitorCount);
document.getElementById('visitorCount').textContent = visitorCount;

// Search functionality
function searchProducts() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    if (searchTerm) {
        // Store search term
        localStorage.setItem('lastSearch', searchTerm);
        // Redirect to products page
        window.location.href = 'pages/products.html';
    }
}

// Handle enter key in search
document.getElementById('searchInput')?.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
        searchProducts();
    }
});
