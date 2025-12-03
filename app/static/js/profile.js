// user_detail.js - 用户详情页面的JavaScript逻辑

let requestsData = {
    sent: [],
    received: []
};

document.addEventListener('DOMContentLoaded', function() {
    console.log('User detail page loaded');

    const currentPath = window.location.pathname;
    console.log('Current path:', currentPath);

    if (currentPath.match(/^\/users\/\d+$/)) {
        console.log('This is a user detail page');
        if (typeof fetchUserDetail === 'function') {
            fetchUserDetail();
        } else {
            console.error('fetchUserDetail function not found');
        }
        fetchUserRating();
        setupSidebarNavigation();
        initRequestsTabs();
    } else {
        console.log('Not a user detail page');
    }
});

// 设置侧边栏导航
function setupSidebarNavigation() {
    const navLinks = document.querySelectorAll('.nav-link');
    const sections = document.querySelectorAll('.orders-section, .items-section');

    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();

            navLinks.forEach(l => l.classList.remove('active'));
            sections.forEach(s => s.classList.remove('active'));

            this.classList.add('active');

            const sectionName = this.dataset.section;
            const section = document.getElementById(`${sectionName}-section`);
            if (section) {
                section.classList.add('active');


                if (sectionName === 'requests' && !requestsData.loaded) {
                    fetchUserRequests();
                } else if (sectionName === 'stats' && !section.dataset.loaded) {
                    fetchUserStats();
                    section.dataset.loaded = 'true';
                }
            }
        });
    });

    console.log('Sidebar navigation setup complete');
}

function initRequestsTabs() {
    const tabBtns = document.querySelectorAll('.request-tabs .tab-btn');
    const containers = document.querySelectorAll('.requests-container');

    tabBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            tabBtns.forEach(b => b.classList.remove('active'));
            containers.forEach(c => c.classList.remove('active'));

            this.classList.add('active');
            const tabName = this.dataset.tab;
            const container = document.getElementById(`${tabName}-requests`);
            if (container) {
                container.classList.add('active');
            }
        });
    });
}

async function fetchUserRequests() {
    try {
        const userIdElement = document.getElementById('user-id');
        let userId = userIdElement ? userIdElement.value : null;

        if (!userId) {
            const parts = window.location.pathname.split('/');
            userId = parts[parts.length - 1];
        }

        const response = await fetch(`/api/requests/${userId}`);

        if (!response.ok) {
            throw new Error('Failed to fetch requests');
        }

        const data = await response.json();
        requestsData = data;
        requestsData.loaded = true;

        document.getElementById('received-count').textContent = data.total_received || 0;
        document.getElementById('sent-count').textContent = data.total_sent || 0;
        document.getElementById('requests-count').textContent = (data.total_received || 0) + (data.total_sent || 0);

        renderReceivedRequests(data.received || []);
        renderSentRequests(data.sent || []);

    } catch (error) {
        console.error('Error fetching requests:', error);
        showRequestsError('Failed to load requests');
    }
}

function renderReceivedRequests(requests) {
    const container = document.getElementById('received-requests-list');

    if (!requests || requests.length === 0) {
        container.innerHTML = `
            <div class="empty-requests">
                <div class="empty-requests-icon">📥</div>
                <div class="empty-title">No Received Requests</div>
                <div class="empty-description">You haven't received any borrowing requests yet</div>
            </div>
        `;
        return;
    }

    container.innerHTML = requests.map(request => `
        <div class="request-card" onclick="viewRequestDetail(${request.requestId})">
            <div class="request-header">
                <div class="request-info">
                    <div class="request-item-name">Item #${request.itemId}</div>
                    <div class="request-user">From: User #${request.requesterId}</div>
                </div>
                <span class="request-status ${request.status.toLowerCase()}">${request.status}</span>
            </div>

            <div class="request-details">
                <div class="request-detail-item">
                    <span class="request-detail-label">Start Date</span>
                    <span class="request-detail-value">${formatDate(request.startDate)}</span>
                </div>
                <div class="request-detail-item">
                    <span class="request-detail-label">End Date</span>
                    <span class="request-detail-value">${formatDate(request.endDate)}</span>
                </div>
                <div class="request-detail-item">
                    <span class="request-detail-label">Duration</span>
                    <span class="request-detail-value">${calculateDuration(request.startDate, request.endDate)} days</span>
                </div>
                ${request.orderId ? `
                <div class="request-detail-item">
                    <span class="request-detail-label">Order ID</span>
                    <span class="request-detail-value">#${request.orderId}</span>
                </div>
                ` : ''}
            </div>

            ${request.message ? `
            <div class="request-message">
                <div class="request-message-label">Message</div>
                <div class="request-message-text">${escapeHtml(request.message)}</div>
            </div>
            ` : ''}

            ${request.rejectionReason ? `
            <div class="request-message">
                <div class="request-message-label">Rejection Reason</div>
                <div class="request-message-text">${escapeHtml(request.rejectionReason)}</div>
            </div>
            ` : ''}

            ${request.status === 'PENDING' ? `
            <div class="request-actions">
                <button class="request-btn accept" onclick="acceptRequest(${request.requestId}, event)">
                    ✓ Accept
                </button>
                <button class="request-btn reject" onclick="rejectRequest(${request.requestId}, event)">
                    ✗ Reject
                </button>
            </div>
            ` : ''}
        </div>
    `).join('');
}

function renderSentRequests(requests) {
    const container = document.getElementById('sent-requests-list');

    if (!requests || requests.length === 0) {
        container.innerHTML = `
            <div class="empty-requests">
                <div class="empty-requests-icon">📤</div>
                <div class="empty-title">No Sent Requests</div>
                <div class="empty-description">You haven't sent any borrowing requests yet</div>
            </div>
        `;
        return;
    }

    container.innerHTML = requests.map(request => `
        <div class="request-card" onclick="viewRequestDetail(${request.requestId})">
            <div class="request-header">
                <div class="request-info">
                    <div class="request-item-name">Item #${request.itemId}</div>
                    <div class="request-user">To: User #${request.ownerId}</div>
                </div>
                <span class="request-status ${request.status.toLowerCase()}">${request.status}</span>
            </div>

            <div class="request-details">
                <div class="request-detail-item">
                    <span class="request-detail-label">Start Date</span>
                    <span class="request-detail-value">${formatDate(request.startDate)}</span>
                </div>
                <div class="request-detail-item">
                    <span class="request-detail-label">End Date</span>
                    <span class="request-detail-value">${formatDate(request.endDate)}</span>
                </div>
                <div class="request-detail-item">
                    <span class="request-detail-label">Duration</span>
                    <span class="request-detail-value">${calculateDuration(request.startDate, request.endDate)} days</span>
                </div>
                ${request.orderId ? `
                <div class="request-detail-item">
                    <span class="request-detail-label">Order ID</span>
                    <span class="request-detail-value">#${request.orderId}</span>
                </div>
                ` : ''}
            </div>

            ${request.message ? `
            <div class="request-message">
                <div class="request-message-label">Message</div>
                <div class="request-message-text">${escapeHtml(request.message)}</div>
            </div>
            ` : ''}

            ${request.rejectionReason ? `
            <div class="request-message">
                <div class="request-message-label">Rejection Reason</div>
                <div class="request-message-text">${escapeHtml(request.rejectionReason)}</div>
            </div>
            ` : ''}

            ${request.status === 'PENDING' ? `
            <div class="request-actions">
                <button class="request-btn edit" onclick="editRequest(${request.requestId}, event)">
                    ✏️ Edit
                </button>
                <button class="request-btn cancel" onclick="cancelRequest(${request.requestId}, event)">
                    ✗ Cancel
                </button>
            </div>
            ` : ''}
        </div>
    `).join('');
}

async function acceptRequest(requestId, event) {
    event.stopPropagation();

    if (!confirm('Are you sure you want to accept this request?')) {
        return;
    }

    try {
        const response = await fetch(`/api/requests/${requestId}/accept`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            alert('Request accepted successfully!');
            fetchUserRequests();
        } else {
            const error = await response.json();
            alert(`Failed to accept request: ${error.error}`);
        }
    } catch (error) {
        console.error('Error accepting request:', error);
        alert('An error occurred while accepting the request');
    }
}

async function rejectRequest(requestId, event) {
    event.stopPropagation();

    const reason = prompt('Please provide a reason for rejection (optional):');
    if (reason === null) {
        return;
    }
    try {
        const response = await fetch(`/api/requests/${requestId}/reject`, {
            method: 'PUT',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ reason: reason || '' })
        });
        if (response.ok) {
            alert('Request rejected successfully');
            fetchUserRequests();
        } else {
            const error = await response.json();
            alert(`Failed to reject request: ${error.error}`);
        }
    } catch (error) {
        console.error('Error rejecting request:', error);
        alert('An error occurred while rejecting the request');
    }
}

async function cancelRequest(requestId, event) {
    event.stopPropagation();

    if (!confirm('Are you sure you want to cancel this request?')) {
        return;
    }

    try {
        const response = await fetch(`/api/requests/${requestId}`, {
            method: 'DELETE'
        });

        if (response.ok) {
            alert('Request cancelled successfully');
            fetchUserRequests();
        } else {
            const error = await response.json();
            alert(`Failed to cancel request: ${error.error}`);
        }
    } catch (error) {
        console.error('Error cancelling request:', error);
        alert('An error occurred while cancelling the request');
    }
}

function editRequest(requestId, event) {
    event.stopPropagation();
    window.location.href = `/requests/${requestId}`;
}

function handleRequestClick(requestId, type) {
    console.log(`Request #${requestId} clicked (${type})`);
}

async function fetchRequestDetail(requestId) {
    try {
        const response = await fetch(`/api/requests/${requestId}`);
        if (response.ok) {
            return await response.json();
        }
        throw new Error('Failed to fetch request detail');
    } catch (error) {
        console.error('Error fetching request detail:', error);
        return null;
    }
}

function refreshRequests() {
    fetchUserRequests();
}

// 显示错误信息
function showRequestsError(message) {
    const receivedContainer = document.getElementById('received-requests-list');
    const sentContainer = document.getElementById('sent-requests-list');

    const errorHtml = `
            <div class="error-message">
                <span>⚠️ ${message}</span>
            </div>
        `;

    receivedContainer.innerHTML = errorHtml;
    sentContainer.innerHTML = errorHtml;
}

function formatDate(dateString) {
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function calculateDuration(startDate, endDate) {
    const start = new Date(startDate);
    const end = new Date(endDate);
    const diffTime = Math.abs(end - start);
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
    return diffDays;
}

function escapeHtml(text) {
    const map = {
        '&': '&amp;',
        '<': '&lt;',
        '>': '&gt;',
        '"': '&quot;',
        "'": '&#039;'
    };
    return text.replace(/[&<>"']/g, m => map[m]);
}

async function fetchUserRating() {
    console.log("fetchUserRating triggered");

    try {
        const parts = window.location.pathname.split("/");
        const userid = parts[parts.length - 1];
        console.log(`Fetching rating for user: ${userid}`);

        const response = await fetch(`/api/users/rating/${userid}`);

        if (!response.ok) {
            if (typeof updateUserRating === 'function') {
                updateUserRating("N/A");
            } else {
                const ratingElement = document.getElementById("user-rating");
                if (ratingElement) {
                    ratingElement.textContent = "N/A";
                    ratingElement.setAttribute('data-rating-loaded', 'true');
                }
            }
            console.log(`Rating fetch failed: no record`);
            return;
        }

        const data = await response.json();
        console.log("Rating data received:", data);

        const rating = data.averageRating;

        let displayRating;
        if (rating === null || rating === undefined || rating === 'None' || rating === 'null') {
            displayRating = "N/A";
            console.log("No rating available");
        } else {
            displayRating = Number(rating).toFixed(2);
            console.log("Rating formatted:", displayRating);
        }

        if (typeof updateUserRating === 'function') {
            updateUserRating(displayRating);
        } else {
            const ratingElement = document.getElementById("user-rating");
            if (ratingElement) {
                ratingElement.textContent = displayRating;
                ratingElement.setAttribute('data-rating-loaded', 'true');
            }
        }

    } catch (err) {
        console.error("Error fetching rating:", err);

        if (typeof updateUserRating === 'function') {
            updateUserRating("Error");
        } else {
            const ratingElement = document.getElementById("user-rating");
            if (ratingElement) {
                ratingElement.textContent = "Error";
                ratingElement.setAttribute('data-rating-loaded', 'true');
            }
        }
    }
}

function toggleAddressForm() {
    const form = document.getElementById('address-form');
    form.classList.toggle('active');
}

async function saveAddress() {
    const street = document.getElementById('street').value;
    const city = document.getElementById('city').value;
    const state = document.getElementById('state').value;
    const zip = document.getElementById('zip').value;

    if (!street || !city || !state || !zip) {
        alert('Please fill in all fields');
        return;
    }

    try {
        const userResponse = await fetch('/api/users/current');
        const userData = await userResponse.json();

        let response;
        if (userData.locationId) {
            console.log(userData)
            response = await fetch(`/api/locations/${userData.locationId}`, {
                method: 'PUT',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    street: street,
                    city: city,
                    state: state,
                    zip: zip,
                    country: 'USA'
                })
            });
        } else {
            response = await fetch('/api/locations', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    street: street,
                    city: city,
                    state: state,
                    zip: zip,
                    country: 'USA'
                })
            });
        }

        if (response.ok) {
            const result = await response.json();
            alert('Address saved successfully!');
            toggleAddressForm();
        } else {
            const error = await response.json();
            alert('Error: ' + error.error);
        }
    } catch (error) {
        alert('An error occurred: ' + error.message);
    }
}

async function logout() {
    if (!confirm('Are you sure you want to sign out?')) {
        return;
    }

    try {
        const response = await fetch('/auth/logout', {
            method: 'POST',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            window.location.href = '/';
        } else {
            alert('Logout failed. Please try again.');
        }
    } catch (error) {
        alert('An error occurred: ' + error.message);
    }
}

function confirmDeleteAccount() {
    const confirmText = prompt('This action cannot be undone. Type "DELETE" to confirm:');

    if (confirmText === 'DELETE') {
        if (confirm('Are you absolutely sure? Your account and all data will be permanently deleted.')) {
            deleteAccount();
        }
    }
}

async function deleteAccount() {
    try {
        const response = await fetch('/api/user/delete', {
            method: 'DELETE',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
            }
        });

        if (response.ok) {
            alert('Your account has been deleted.');
            window.location.href = '/';
        } else {
            alert('Failed to delete account. Please try again.');
        }
    } catch (error) {
        alert('An error occurred: ' + error.message);
    }
}

function refreshUserDetail() {
    if (typeof fetchUserDetail === 'function') {
        fetchUserDetail();
        fetchUserRating();
    }
}

function viewRequestDetail(requestId) {
    window.location.href = `/requests/${requestId}`;
}

// Profile Stats

async function fetchUserStats() {
    try {
        const userIdElement = document.getElementById('user-id');
        let userId = userIdElement ? userIdElement.value : null;

        if (!userId) {
            const parts = window.location.pathname.split('/');
            userId = parts[parts.length - 1];
        }

        console.log('Fetching stats for user:', userId);

        const [avgRentalResponse, activityResponse, successRateResponse] = await Promise.all([
            fetch('/api/stats/user/average-rental-times'),
            fetch(`/api/stats/user/activity-last-three-months/${userId}`),
            fetch(`/api/stats/user/lending-success-rate/${userId}`)
        ]);


        if (avgRentalResponse.ok) {
            const avgRentalData = await avgRentalResponse.json();
            if (avgRentalData.success) {
                updateAverageRentalTimes(avgRentalData.data);
            }
        }


        if (activityResponse.ok) {
            const activityData = await activityResponse.json();
            if (activityData.success) {
                updateActivityStats(activityData.data);
            }
        }


        if (successRateResponse.ok) {
            const successRateData = await successRateResponse.json();
            if (successRateData.success) {
                updateSuccessRate(successRateData.data);
            }
        }

    } catch (error) {
        console.error('Error fetching user stats:', error);
        showStatsError('Failed to load statistics');
    }
}


function updateAverageRentalTimes(data) {
    const avgBorrowDays = document.getElementById('avg-borrow-days');
    const avgLendDays = document.getElementById('avg-lend-days');

    if (avgBorrowDays) {
        avgBorrowDays.textContent = data.average_borrow_days || '0';
    }
    if (avgLendDays) {
        avgLendDays.textContent = data.average_lend_days || '0';
    }
}


function updateActivityStats(data) {
    const borrowRequests = document.getElementById('borrow-requests');
    const lendRequests = document.getElementById('lend-requests');
    const totalActivity = document.getElementById('total-activity');
    const periodStart = document.getElementById('activity-period-start');

    if (borrowRequests) {
        borrowRequests.textContent = data.borrow_requests || '0';
    }
    if (lendRequests) {
        lendRequests.textContent = data.lend_requests || '0';
    }
    if (totalActivity) {
        totalActivity.textContent = data.total_activity || '0';
    }
    if (periodStart && data.period_start) {
        periodStart.textContent = formatDate(data.period_start);
    }
}

/**
 * 更新借出成功率显示(包含圆形进度条动画)
 */
function updateSuccessRate(data) {
    const successRateValue = document.getElementById('success-rate-value');
    const acceptedCount = document.getElementById('accepted-count');
    const rejectedCount = document.getElementById('rejected-count');
    const totalProcessed = document.getElementById('total-processed');
    const progressCircle = document.getElementById('success-rate-circle');

    const rate = data.success_rate || 0;

    if (successRateValue) {
        successRateValue.textContent = rate.toFixed(1);
    }
    if (acceptedCount) {
        acceptedCount.textContent = data.accepted_requests || '0';
    }
    if (rejectedCount) {
        rejectedCount.textContent = data.rejected_requests || '0';
    }
    if (totalProcessed) {
        totalProcessed.textContent = data.total_processed_requests || '0';
    }


    if (progressCircle) {
        const radius = 52;
        const circumference = 2 * Math.PI * radius;
        const offset = circumference - (rate / 100) * circumference;


        progressCircle.style.transition = 'stroke-dashoffset 1s ease-in-out';
        progressCircle.style.strokeDashoffset = offset;

        if (rate >= 80) {
            progressCircle.style.stroke = '#4CAF50'; // 绿色
        } else if (rate >= 50) {
            progressCircle.style.stroke = '#FFC107'; // 黄色
        } else {
            progressCircle.style.stroke = '#F44336'; // 红色
        }
    }
}


function showStatsError(message) {
    const statsContainer = document.querySelector('#stats-section .stats-container');
    if (statsContainer) {
        statsContainer.innerHTML = `
            <div class="error-message">
                <span>⚠️ ${message}</span>
            </div>
        `;
    }
}


function refreshStats() {
    fetchUserStats();
}


function setupStatsNavigation() {
    const statsNavLink = document.querySelector('.nav-link[data-section="stats"]');
    if (statsNavLink) {
        statsNavLink.addEventListener('click', function(e) {
            e.preventDefault();

            // 移除其他active状态
            document.querySelectorAll('.nav-link').forEach(l => l.classList.remove('active'));
            document.querySelectorAll('.orders-section').forEach(s => s.classList.remove('active'));

            // 激活stats
            this.classList.add('active');
            const statsSection = document.getElementById('stats-section');
            if (statsSection) {
                statsSection.classList.add('active');
                // 首次点击时加载数据
                if (!statsSection.dataset.loaded) {
                    fetchUserStats();
                    statsSection.dataset.loaded = 'true';
                }
            }
        });
    }
}
