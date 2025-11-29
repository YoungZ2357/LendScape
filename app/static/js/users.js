let currentQuery = '';
let currentPage = 1;
let currentSize = 8;

let currentUserId = null;
let currentUserData = null;
let currentOrderPage = 1;
let currentOrderSize = 6;

let currentOwnershipPage = 1;
let currentOwnershipSize = 8;

// 添加全局变量存储评分状态
let userRatingLoaded = false;
let userRatingValue = null;

function makeSearchUser(page = 1, size = 8, resetQuery = false) {
    if (resetQuery) {
        currentQuery = document.getElementById("searchInput").value.trim();
    }

    currentPage = page;
    currentSize = size;

    const resultDiv = document.getElementById("results");

    let routeUrl = `/api/users?page=${page}&size=${size}`;
    if (currentQuery) {
        routeUrl += `&search=${encodeURIComponent(currentQuery)}`;
    }
    const fullUrl = window.location.origin + routeUrl;

    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
        loadingDiv.style.display = "block";
    }

    fetch(fullUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP status was ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            displaySearchUser(data);
        })
        .catch(error => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            resultDiv.innerHTML = '<p>Invalid search. Please try again</p>';
            const errorEl = document.createElement('p');
            errorEl.style.color = 'red';
            errorEl.textContent = `Error: ${error.message || error}`;
            resultDiv.appendChild(errorEl);
        });
}

function displaySearchUser(data) {
    const resultDiv = document.getElementById("results");

    if (data.count === 0) {
        resultDiv.innerHTML = `<p>No results relating to ${data.query}</p>`;
        const paginationDiv = document.getElementById("pagination");
        if (paginationDiv) {
            paginationDiv.innerHTML = ``;
        }
        return;
    }

    let html = `<p>${data.count} relating users found</p>`;
    console.log('Displaying users:', data.count);

    data.results.forEach(user => {
        html += `
        <div class="elem-card" data-user-id="${user.userId}">
            <h3>User Info</h3>
            <p>Full Name: ${user.firstName} ${user.lastName}</p>
            <p>Email: ${user.email}</p>
            <p>Location: ${user.location}</p>
            <p>Status: ${user.is_available}</p>
        </div>
        `;
    });

    resultDiv.innerHTML = html;

    const newResultDiv = resultDiv.cloneNode(true);
    resultDiv.parentNode.replaceChild(newResultDiv, resultDiv);

    newResultDiv.addEventListener('click', function(e) {
        const card = e.target.closest('.elem-card');
        if (card) {
            const userId = card.dataset.userId;
            console.log('Navigating to user profile:', userId);
            window.location.href = `/users/${userId}`;
        }
    });

    displayPagination(data, (newPage, newSize) => {
        makeSearchUser(newPage, newSize, false);
    });
}

function clearSearchUser() {
    clearSearchCommon(makeSearchUser);
}


function fetchUserDetail(userId = null, refresh = false) {

    if (!userId) {
        const match = window.location.pathname.match(/\/users\/(\d+)/);
        userId = match ? match[1] : document.getElementById('user-id')?.value;
    }

    if (!userId) {
        displayUserError('Failed to fetch user id');
        return;
    }

    currentUserId = userId;

    const routeUrl = `/api/users/${userId}`;
    const fullUrl = window.location.origin + routeUrl;

    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
        loadingDiv.style.display = "block";
    }

    Promise.all([
        fetch(fullUrl).then(response => {
            if (!response.ok) {
                throw new Error(`HTTP status was ${response.status}`);
            }
            return response.json();
        }),
        fetchUserOwnership(userId, currentOwnershipPage, currentOwnershipSize)
    ])
        .then(([userData, ownershipData]) => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            currentUserData = userData;
            console.log(userData)
            currentUserData.item_ownership = ownershipData;

            displayUserDetail(currentUserData);
        })
        .catch(error => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            displayUserError(error.message || error);
        });
}


function fetchUserOwnership(userId, page = 1, size = 8) {
    const routeUrl = `/api/items/ownership/${userId}?page=${page}&size=${size}`;
    const fullUrl = window.location.origin + routeUrl;

    return fetch(fullUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`Failed to fetch ownership data: ${response.status}`);
            }
            return response.json();
        })
        .catch(error => {
            console.error('Error fetching ownership data:', error);
            return { data: [], page: 1, size: 8, total: 0, pages: 0 };
        });
}

function displayUserDetail(data) {
    console.log("displayUserDetail triggered");
    displayUserInfo(data.user_info);
    displayUserStatistics(data.order_statistics);

    if (document.getElementById('borrowing-section')) {
        console.log("get borrower")
        displayUserOrders(data.borrower_orders, 'borrower');
    }
    if (document.getElementById('lending-section')) {
        displayUserOrders(data.lender_orders, 'lender');
    }

    if (document.getElementById('items-section')) {
        displayUserOwnership(data.item_ownership);
    }
}

function displayUserInfo(userInfo) {
    console.log("displayUserInfo triggered");
    const infoDiv = document.getElementById("profile-card");
    if (!infoDiv) return;

    let html = `
    <div class="profile-header" id="profile-card">
        <div class="profile-avatar" id="profile-avatar">-</div>
        <div class="profile-name" id="profile-name">${userInfo.username}</div>
        <div class="profile-username" id="profile-email">${userInfo.email}</div>
    </div>
    `;

    infoDiv.innerHTML = html;
    console.log(infoDiv.innerHTML);

    const titleElement = document.getElementById("page-title");
    if (titleElement) {
        titleElement.textContent = userInfo.username;
    }

    const profileName = document.getElementById("profile-name");
    if (profileName) {
        profileName.textContent = userInfo.username;
        console.log(profileName.textContent);
    }

    const profileEmail = document.getElementById("profile-email");
    if (profileEmail) {
        profileEmail.textContent = userInfo.email;
    }

    const initial = userInfo.username ? userInfo.username.charAt(0).toUpperCase() : '?';

    const profileAvatar = document.getElementById("profile-avatar");
    if (profileAvatar) {
        profileAvatar.textContent = initial;
    }

    const navAvatar = document.getElementById("nav-avatar");
    if (navAvatar) {
        const shouldKeep = navAvatar.dataset.keep === 'true' ||
            navAvatar.dataset.preserveLoggedIn === 'true';

        if (!shouldKeep && navAvatar.textContent === '-') {
            console.log('Nav avatar is default, not updating to preserve logged-in user initial');
        } else if (!shouldKeep) {
            console.log('Preserving nav-avatar for logged-in user');
        }
    }

    document.title = `${userInfo.username} - User Detail`;
}

function displayUserStatistics(statistics) {
    const statsDiv = document.getElementById("profile-stats");
    if (!statsDiv) return;

    console.log("displayUserStatistics triggered");
    console.log(statistics);

    const currentRatingElement = document.getElementById("user-rating");
    let currentRatingValue = "Loading...";
    let isRatingLoaded = false;

    if (currentRatingElement) {
        const ratingLoaded = currentRatingElement.getAttribute('data-rating-loaded') === 'true';
        if (ratingLoaded) {
            currentRatingValue = currentRatingElement.textContent;
            isRatingLoaded = true;
        } else if (userRatingLoaded && userRatingValue !== null) {
            currentRatingValue = userRatingValue;
            isRatingLoaded = true;
        }
    }

    let html = `
        <div class="stat">
            <div class="stat-value" id="items-count">${statistics.lender_count}</div>
            <div class="stat-label">Lending</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="total-orders">${statistics.borrower_count}</div>
            <div class="stat-label">Borrowing</div>
        </div>
        <div class="stat">
            <div class="stat-value" id="user-rating" data-rating-loaded="${isRatingLoaded}">${currentRatingValue}</div>
            <div class="stat-label">Rating</div>
        </div>
    `;

    statsDiv.innerHTML = html;

    if (isRatingLoaded && userRatingValue !== null) {
        const newRatingElement = document.getElementById("user-rating");
        if (newRatingElement) {
            newRatingElement.setAttribute('data-rating-loaded', 'true');
            newRatingElement.textContent = userRatingValue;
        }
    }

    const borrowerCount = document.getElementById("borrower-count");
    if (borrowerCount) {
        borrowerCount.textContent = statistics.borrower_count;
    }
    const lenderCount = document.getElementById("lender-count");
    if (lenderCount) {
        lenderCount.textContent = statistics.lender_count;
    }
    const totalOrders = document.getElementById("total-orders");
    if (totalOrders) {
        totalOrders.textContent = statistics.borrower_count;
    }
}

function updateUserRating(rating) {
    userRatingLoaded = true;
    userRatingValue = rating;

    const ratingElement = document.getElementById("user-rating");
    if (ratingElement) {
        ratingElement.textContent = rating;
        ratingElement.setAttribute('data-rating-loaded', 'true');
    }
}

function displayUserOrders(orders, type) {
    console.log("display orders triggered");
    console.log("type", type);
    const containerDiv = document.getElementById(`${type}-orders`);
    const resultsDiv = document.getElementById(`${type}-orders-results`);
    const targetDiv = containerDiv || resultsDiv;

    if (!targetDiv) return;

    const title = type === 'borrower' ? 'Borrowed' : 'Lended';

    if (!orders || orders.length === 0) {
        targetDiv.innerHTML = `
            <div class="empty-state">
                <div class="empty-icon">📦</div>
                <div class="empty-title">No ${title} Orders</div>
                <div class="empty-description">You don't have any ${title.toLowerCase()} orders yet.</div>
            </div>
        `;
        return;
    }

    let html = '';
    orders.forEach(order => {
        const statusClass = order.item_status ? 'true' : 'false';
        const statusText = order.item_status ? '✔ Available' : '✗ Not Available';
        console.log(order);
        html += `
            <div class="order-card" data-order-id="${order.order_id}">
                <div class="order-info">
                    <div class="order-id">Order #${order.order_id}</div>
                    <div class="order-item-name">${order.item_name || 'Unnamed Item'}</div>
                    <div class="order-description">${order.item_description || 'No description'}</div>
                    <div class="order-date">${formatOrderDate(order.created_at)}</div>
                </div>
                <div class="order-status ${statusClass}">${statusText}</div>
            </div>
        `;
    });

    targetDiv.innerHTML = html;
}

function displayUserOwnership(ownershipData) {
    console.log("displayUserOwnership triggered", ownershipData);

    const containerDiv = document.getElementById('ownership-section') ||
        document.getElementById('user-items') ||
        document.getElementById('items-section');

    if (!containerDiv) {
        console.log("No ownership container found");
        return;
    }
    let resultsDiv = document.getElementById('ownership-results');
    if (!resultsDiv) {
        resultsDiv = document.createElement('div');
        resultsDiv.id = 'ownership-results';
        containerDiv.appendChild(resultsDiv);
    }

    let html = '<div class="items-grid">';

    const isOwnProfile = document.getElementById('add-item-btn') &&
        document.getElementById('add-item-btn').style.display !== 'none';

    if (isOwnProfile) {
        html += `
            <div class="add-item-card" onclick="window.location.href='/items/create'">
                <div class="add-item-content">
                    <div class="add-item-icon">+</div>
                    <div class="add-item-text">Add New Item</div>
                </div>
            </div>
        `;
    }

    if (!ownershipData || !ownershipData.data || ownershipData.data.length === 0) {
        if (isOwnProfile) {
            html += `
                <div style="grid-column: span 3; text-align: center; padding: 40px;">
                    <div class="empty-items-icon" style="font-size: 48px; opacity: 0.5;">📦</div>
                    <div style="color: #666; margin-top: 10px;">No items yet</div>
                    <div style="color: #999; font-size: 14px;">Click "Add New Item" to get started</div>
                </div>
            `;
        } else {
            html += `
                <div style="grid-column: span 4; text-align: center; padding: 40px;">
                    <div class="empty-items-icon" style="font-size: 48px; opacity: 0.5;">📦</div>
                    <div style="color: #666; margin-top: 10px;">This user hasn't added any items yet</div>
                </div>
            `;
        }
    } else {
        ownershipData.data.forEach(item => {
            const statusClass = item.is_available === true ? 'available' : 'rented';
            console.log("Loading Item Card")
            console.log(item)
            console.log(item.status)
            html += `
                <div class="item-card" data-item-id="${item.itemId}">
                    <div class="item-image">
                        ${item.image_url ?
                `<img src="${item.image_url}" alt="${item.itemName || 'UNNAMED'}">` :
                '📦'
            }
                        
                        <span class="item-status ${statusClass}">
                            ${item.is_available === true ? 'Available' : 'Unavailable'}
                        </span>
                    </div>
                    <div class="item-content">
                        <div class="item-name item-header">
                            <h3>${item.itemName || 'UNNAMED'}</h3>
                        </div>
                        <div class="item-description item-body">
                            <p>${item.description || 'NO DESCRIPTION'}</p>
                        </div>
                        <div class="item-footer">
                            <div class="item-price">
                                ${item.price ? `$${item.price} <span>/day</span>` : 'Price not set'}
                            </div>
                            ${isOwnProfile ? `
                            <div class="item-actions">
                                <button class="item-action-btn edit" onclick="editItem(${item.itemId})">Edit</button>
                                <button class="item-action-btn delete" onclick="deleteItem(${item.itemId})">Delete</button>
                            </div>
                            ` : ''}
                        </div>
                        <div class="item-meta" style="padding: 10px 0; border-top: 1px solid #eee; color: #999; font-size: 12px;">
                            <span class="item-id">ID: #${item.itemId}</span>
                            ${item.createdAt ? ` • <span class="item-date">${formatItemDate(item.createdAt)}</span>` : ''}
                        </div>
                    </div>
                </div>
            `;
        });
    }

    html += '</div>';
    resultsDiv.innerHTML = html;

    if (ownershipData && ownershipData.data && ownershipData.data.length > 0) {
        displayPagination(ownershipData, (newPage, newSize) => {
            changeOwnershipPage(newPage, newSize);
        }, {
            containerId: 'ownership-pagination',
            containerClass: 'pagination-container',
            insertAfterId: 'ownership-results'
        });
    } else {
        const paginationDiv = document.getElementById('ownership-pagination');
        if (paginationDiv) {
            paginationDiv.innerHTML = '';
        }
    }

    attachItemCardClickEvents();
}

function editItem(itemId) {
    console.log('Edit item:', itemId);
    window.location.href = `/items/edit/${itemId}`;
}

function deleteItem(itemId) {
    if (!confirm('Are you sure you want to delete this item?')) {
        return;
    }
    console.log('Delete item:', itemId);

    fetch(`/api/items/${itemId}`, {
        method: 'DELETE',
        headers: {
            'Content-Type': 'application/json',
        }
    })
        .then(response => {
            if (response.ok) {
                alert('Item deleted successfully!');
                if (typeof fetchUserDetail === 'function') {
                    fetchUserDetail();
                } else if (typeof loadUserItems === 'function') {
                    loadUserItems();
                }
            } else {
                alert('Failed to delete item. Please try again.');
            }
        })
        .catch(error => {
            console.error('Error deleting item:', error);
            alert('An error occurred while deleting the item.');
        });
}

function changeOwnershipPage(page, size = currentOwnershipSize) {
    currentOwnershipPage = page;
    currentOwnershipSize = size;

    if (!currentUserId) {
        console.error('No user ID available');
        return;
    }

    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
        loadingDiv.style.display = "block";
    }

    fetchUserOwnership(currentUserId, page, size)
        .then(ownershipData => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            displayUserOwnership(ownershipData);
        })
        .catch(error => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            console.error('Error changing ownership page:', error);
        });
}

function formatOrderDate(dateString) {
    if (!dateString) return 'Unknown date';

    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;

    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function formatItemDate(dateString) {
    if (!dateString) return '';

    const date = new Date(dateString);
    const now = new Date();
    const diff = now - date;
    const days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) return 'Today';
    if (days === 1) return 'Yesterday';
    if (days < 7) return `${days} days ago`;
    if (days < 30) return `${Math.floor(days / 7)} weeks ago`;
    if (days < 365) return `${Math.floor(days / 30)} months ago`;

    return date.toLocaleDateString('zh-CN', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

function attachItemCardClickEvents() {
    const itemCards = document.querySelectorAll('.item-card');
    itemCards.forEach(card => {
        card.addEventListener('click', function(e) {
            if (e.target.classList.contains('item-action-btn')) {
                e.stopPropagation();
                return;
            }

            const itemId = this.dataset.itemId;
            if (itemId) {
                console.log('Clicked item:', itemId);
                window.location.href = `/items/${itemId}`;
            }
        });
    });
}

function displayUserError(message) {
    const errorDiv = document.getElementById("error-message");
    if (errorDiv) {
        errorDiv.innerHTML = `
            <div class="error-container">
                <p class="error-title">加载失败</p>
                <p class="error-detail">错误: ${message}</p>
                <button onclick="fetchUserDetail(null, true)">重试</button>
            </div>
        `;
        errorDiv.style.display = 'block';
    }

    ['user-info', 'order-statistics', 'borrower-orders', 'lender-orders'].forEach(id => {
        const div = document.getElementById(id);
        if (div) div.innerHTML = '';
    });
}

function refreshUserDetail() {
    if (currentUserId) {
        currentOrderPage = 1;
        currentOwnershipPage = 1;

        const ratingElement = document.getElementById('user-rating');
        if (ratingElement && ratingElement.getAttribute('data-rating-loaded') === 'true') {
            userRatingLoaded = true;
            userRatingValue = ratingElement.textContent;
        }

        fetchUserDetail(currentUserId, true);
    }
}

function clearUserDetail() {
    currentUserId = null;
    currentUserData = null;
    currentOrderPage = 1;
    userRatingLoaded = false;
    userRatingValue = null;
    window.location.href = '/users';
}