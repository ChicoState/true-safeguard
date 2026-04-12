// Blacklist Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // DOM Elements
    const searchInput = document.getElementById('search-input');
    const ageFilter = document.getElementById('age-filter');
    const categoryFilter = document.getElementById('category-filter');
    const riskFilter = document.getElementById('risk-filter');
    const resetButton = document.getElementById('reset-filters');
    const clearSearchButton = document.getElementById('clear-search');
    const resultsCount = document.getElementById('results-count');
    const cardGrid = document.getElementById('card-grid');
    const noResults = document.getElementById('no-results');
    const learnMoreButtons = document.querySelectorAll('.btn-learn-more');
    const cards = document.querySelectorAll('.blacklist-card');

    // Filter functionality
    function filterCards() {
        const searchTerm = searchInput.value.toLowerCase().trim();
        const selectedAge = ageFilter.value;
        const selectedCategory = categoryFilter.value;
        const selectedRisk = riskFilter.value;

        let visibleCount = 0;

        cards.forEach(card => {
            const name = card.dataset.name;
            const age = card.dataset.age;
            const category = card.dataset.category;
            const risk = card.dataset.risk;

            // Check all filter conditions
            const matchesSearch = searchTerm === '' || name.includes(searchTerm);
            const matchesAge = selectedAge === '' || age === selectedAge;
            const matchesCategory = selectedCategory === '' || category === selectedCategory;
            const matchesRisk = selectedRisk === '' || risk === selectedRisk;

            // Show or hide card based on all conditions
            if (matchesSearch && matchesAge && matchesCategory && matchesRisk) {
                card.classList.remove('hidden');
                visibleCount++;
            } else {
                card.classList.add('hidden');
            }
        });

        // Update results count
        resultsCount.textContent = visibleCount;

        // Show/hide no results message
        if (visibleCount === 0) {
            noResults.style.display = 'block';
            cardGrid.style.display = 'none';
        } else {
            noResults.style.display = 'none';
            cardGrid.style.display = 'grid';
        }
    }

    // Reset all filters
    function resetFilters() {
        searchInput.value = '';
        ageFilter.value = '';
        categoryFilter.value = '';
        riskFilter.value = '';
        filterCards();
    }

    // Expand/collapse card details
    function toggleDetails(button) {
        const targetId = button.dataset.target;
        const details = document.getElementById(targetId);

        if (details) {
            const isExpanded = details.classList.contains('expanded');

            if (isExpanded) {
                details.classList.remove('expanded');
                button.classList.remove('active');
                button.querySelector('.btn-text').textContent = 'Learn More';
            } else {
                details.classList.add('expanded');
                button.classList.add('active');
                button.querySelector('.btn-text').textContent = 'Show Less';
            }
        }
    }

    // Event listeners for filters
    searchInput.addEventListener('input', filterCards);
    ageFilter.addEventListener('change', filterCards);
    categoryFilter.addEventListener('change', filterCards);
    riskFilter.addEventListener('change', filterCards);

    // Reset button listeners
    resetButton.addEventListener('click', resetFilters);
    if (clearSearchButton) {
        clearSearchButton.addEventListener('click', resetFilters);
    }

    // Learn More button listeners
    learnMoreButtons.forEach(button => {
        button.addEventListener('click', function() {
            toggleDetails(this);
        });
    });

    // Keyboard accessibility for expand/collapse
    learnMoreButtons.forEach(button => {
        button.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggleDetails(this);
            }
        });
    });

    // Initialize count on page load
    filterCards();
});
