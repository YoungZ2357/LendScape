// top_users.js - Top Active Users Page Logic

let currentFilters = {
    minScore: null,
    page: 1,
    perPage: 50
};

let allUsersData = [];

// ==================== Utility Functions ====================

/**
 * Show loading state
 */
function showLoading() {
    document.getElementById('loading').style.display = 'block';
}

/**
 * Hide loading state
 */
function hideLoading() {
    document.getElementById('loading').style.display = 'none';
}

/**
 * Hide all sections
 */
function hideAllSections() {
    document.getElementById('podium-section').style.display = 'none';
    document.getElementById('top-ten-section').style.display = 'none';
    document.getElementById('other-users-section').style.display = 'none';
    document.getElementById('empty-state').style.display = 'none';
}

/**
 * Show empty state
 */
function showEmptyState() {
    document.getElementById('empty-state').style.display = 'block';
}

/**
 * Show error message
 */
function showError(message) {
    const emptyState = document.getElementById('empty-state');
    emptyState.style.display = 'block';
    emptyState.innerHTML = `
        <div class="empty-icon">⚠️</div>
        <div class="empty-title">Error</div>
        <div class="empty-description">${message}</div>
    `;
}

/**
 * Get user initials
 */
function getInitials(firstName, lastName) {
    const first = firstName ? firstName.charAt(0).toUpperCase() : '';
    const last = lastName ? lastName.charAt(0).toUpperCase() : '';
    return first + last || 'U';
}

/**
 * Navigate to user profile
 */
function goToUserProfile(userId) {
    window.location.href = `/users/${userId}`;
}

/**
 * Apply filters
 */
function applyFilters() {
    const minScore = document.getElementById('minScoreFilter').value;

    currentFilters.minScore = minScore ? parseFloat(minScore) : null;
    currentFilters.page = 1; // Reset to first page

    loadTopUsers();
}

/**
 * Clear filters
 */
function clearFilters() {
    document.getElementById('minScoreFilter').value = '';

    currentFilters.minScore = null;
    currentFilters.page = 1;

    loadTopUsers();
}

// ==================== Main Functions ====================

/**
 * Load top users data
 */
async function loadTopUsers() {
    try {
        showLoading();
        hideAllSections();

        // Build query parameters
        let queryParams = `page=${currentFilters.page}&per_page=${currentFilters.perPage}`;

        if (currentFilters.minScore !== null && currentFilters.minScore > 0) {
            queryParams += `&min_score=${currentFilters.minScore}`;
        }
        console.log(`/api/stats/api/top-active-users?${queryParams}`)
        const response = await fetch(`/api/stats/top-active-users?${queryParams}`);

        if (!response.ok) {
            throw new Error('Failed to fetch users');
        }

        const data = await response.json();

        if (!data.success) {
            throw new Error(data.message || 'Failed to load users');
        }

        allUsersData = data.data;

        hideLoading();

        if (allUsersData.length === 0) {
            showEmptyState();
        } else {
            displayUsers(allUsersData);
            updateHeroStats(data);

            // 直接使用 utils.js 中的 displayPagination
            if (data.pagination) {
                let insertAfterId = 'other-users-container';
                if (document.getElementById('other-users-section').style.display === 'none') {
                    insertAfterId = 'top-ten-container';
                }
                if (document.getElementById('top-ten-section').style.display === 'none') {
                    insertAfterId = 'podium-container';
                }

                const paginationData = {
                    page: data.pagination.page,
                    size: data.pagination.per_page,
                    total: data.pagination.total_users,
                    pages: data.pagination.total_pages,
                    query: currentFilters.minScore ? `Min Score: ${currentFilters.minScore}` : '',
                    results: data.data
                };

                window.displayPagination(paginationData, (newPage, newSize) => {
                    currentFilters.page = newPage;
                    currentFilters.perPage = newSize;
                    loadTopUsers();
                }, {
                    containerId: 'pagination',
                    containerClass: 'pagination-container',
                    insertAfterId: insertAfterId
                });
            }
        }

    } catch (error) {
        console.error('Error loading top users:', error);
        hideLoading();
        showError('Failed to load users. Please try again.');
    }
}

/**
 * Display users in different sections
 */
function displayUsers(users) {
    if (users.length === 0) {
        showEmptyState();
        return;
    }

    // Split users into categories
    const top3 = users.slice(0, 3);
    const top10 = users.slice(3, 10);
    const others = users.slice(10);

    // Display Top 3 (Podium)
    if (top3.length > 0) {
        displayPodiumUsers(top3);
        document.getElementById('podium-section').style.display = 'block';
    }

    // Display Top 4-10
    if (top10.length > 0) {
        displayTopTenUsers(top10);
        document.getElementById('top-ten-section').style.display = 'block';
    }

    // Display others
    if (others.length > 0) {
        displayOtherUsers(others);
        document.getElementById('other-users-section').style.display = 'block';
    }
}

/**
 * Display Top 3 users in podium style
 */
function displayPodiumUsers(users) {
    const container = document.getElementById('podium-container');
    container.innerHTML = '';

    users.forEach((user, index) => {
        const rank = index + 1;
        const medal = rank === 1 ? '🥇' : rank === 2 ? '🥈' : '🥉';

        const podiumUser = document.createElement('div');
        podiumUser.className = `podium-user rank-${rank}`;
        podiumUser.onclick = () => goToUserProfile(user.user_id);

        podiumUser.innerHTML = `
            <div class="podium-card">
                <div class="podium-rank">${medal}</div>
                <div class="podium-avatar">
                    ${getInitials(user.first_name, user.last_name)}
                </div>
                <div class="podium-name">
                    ${user.first_name} ${user.last_name}
                </div>
                <div class="podium-email">${user.email}</div>
                <div class="podium-score">score:${user.activity_score}</div>
                <div class="podium-stats">
                    <div class="podium-stat">
                        <div class="podium-stat-value">${user.request_count}</div>
                        <div class="podium-stat-label">Requests</div>
                    </div>
                    <div class="podium-stat">
                        <div class="podium-stat-value">${user.total_orders}</div>
                        <div class="podium-stat-label">Orders</div>
                    </div>
                </div>
                ${user.location ? `
                    <div class="user-location">
                        📍 ${user.location.full_address || user.location.city}
                    </div>
                ` : ''}
            </div>
        `;

        container.appendChild(podiumUser);
    });
}

/**
 * Display Top 4-10 users
 */
function displayTopTenUsers(users) {
    const container = document.getElementById('top-ten-container');
    container.innerHTML = '';

    users.forEach(user => {
        const card = document.createElement('div');
        card.className = 'top-ten-card';
        card.onclick = () => goToUserProfile(user.user_id);

        card.innerHTML = `
            <div class="top-ten-header">
                <div class="top-ten-rank">#${user.rank}</div>
                <div class="top-ten-avatar">
                    ${getInitials(user.first_name, user.last_name)}
                </div>
                <div class="top-ten-info">
                    <div class="top-ten-name">
                        ${user.first_name} ${user.last_name}
                    </div>
                    <div class="top-ten-email">${user.email}</div>
                </div>
                <div class="top-ten-score">${user.activity_score}</div>
            </div>
            <div class="top-ten-stats">
                <div class="top-ten-stat">
                    <div class="top-ten-stat-value">${user.request_count}</div>
                    <div class="top-ten-stat-label">Requests</div>
                </div>
                <div class="top-ten-stat">
                    <div class="top-ten-stat-value">${user.borrower_count}</div>
                    <div class="top-ten-stat-label">Borrowed</div>
                </div>
                <div class="top-ten-stat">
                    <div class="top-ten-stat-value">${user.renter_count}</div>
                    <div class="top-ten-stat-label">Lent</div>
                </div>
            </div>
            ${user.location ? `
                <div class="user-location">
                    📍 ${user.location.full_address || user.location.city}
                </div>
            ` : ''}
        `;

        container.appendChild(card);
    });
}

/**
 * Display other users (rank 11+)
 */
function displayOtherUsers(users) {
    const container = document.getElementById('other-users-container');
    container.innerHTML = '';

    users.forEach(user => {
        const card = document.createElement('div');
        card.className = 'user-card';
        card.onclick = () => goToUserProfile(user.user_id);

        card.innerHTML = `
            <div class="user-header">
                <div class="user-rank">#${user.rank}</div>
                <div class="user-avatar">
                    ${getInitials(user.first_name, user.last_name)}
                </div>
                <div class="user-info">
                    <div class="user-name">
                        ${user.first_name} ${user.last_name}
                    </div>
                    <div class="user-email">${user.email}</div>
                </div>
                <div class="user-score">${user.activity_score}</div>
            </div>
            <div class="user-stats">
                <div class="user-stat">
                    <div class="user-stat-value">${user.request_count}</div>
                    <div class="user-stat-label">Requests</div>
                </div>
                <div class="user-stat">
                    <div class="user-stat-value">${user.borrower_count}</div>
                    <div class="user-stat-label">Borrowed</div>
                </div>
                <div class="user-stat">
                    <div class="user-stat-value">${user.renter_count}</div>
                    <div class="user-stat-label">Lent</div>
                </div>
            </div>
            ${user.location ? `
                <div class="user-location">
                    📍 ${user.location.full_address || user.location.city}
                </div>
            ` : ''}
        `;

        container.appendChild(card);
    });
}

/**
 * Update hero section statistics
 */
function updateHeroStats(data) {
    const totalUsers = data.pagination ? data.pagination.total_users : data.data.length;
    const activeUsers = data.data.filter(u => u.activity_score > 0).length;
    const avgScore = data.data.length > 0
        ? (data.data.reduce((sum, u) => sum + u.activity_score, 0) / data.data.length).toFixed(2)
        : 0;

    document.getElementById('total-users-count').textContent = totalUsers;
    document.getElementById('active-users-count').textContent = activeUsers;
    document.getElementById('avg-activity-score').textContent = avgScore;
}