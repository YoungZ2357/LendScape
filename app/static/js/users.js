

let currentQuery = '';
let currentPage = 1;
let currentSize = 8;

let currentUserId = null;
let currentUserData = null;
let currentOrderPage = 1;
let currentOrderSize = 6;

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
            <p>Status: ${user.status}</p>
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

// ============ 用户详情相关函数 ============

function fetchUserDetail(userId = null, refresh = false) {
    // 获取userId
    if (!userId) {
        const match = window.location.pathname.match(/\/users\/(\d+)/);
        userId = match ? match[1] : document.getElementById('user-id')?.value;
    }

    if (!userId) {
        displayUserError('Failed to fetch user id');
        return;
    }

    currentUserId = userId;

    // API路径是正确的
    const routeUrl = `/api/users/${userId}`;

    const fullUrl = window.location.origin + routeUrl;
    console.log(fullUrl);
    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
        loadingDiv.style.display = "block";
    }

    fetch(fullUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error(`HTTP status was ${response.status}`);
            }
            // console.log(response.json())
            return response.json();
        })
        .then(data => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            // console.log(data)
            currentUserData = data;
            console.log(currentUserData)
            displayUserDetail(data);
        })
        .catch(error => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            displayUserError(error.message || error);
        });
}

function displayUserDetail(data) {
    console.log("displayUserDetail triggered");
    displayUserInfo(data.user_info);
    displayUserStatistics(data.order_statistics);

    // 显示订单（如果页面有对应元素）
    if (document.getElementById('borrowing-section')) {
        console.log("get borrower")
        displayUserOrders(data.borrower_orders, 'borrower');
    }
    if (document.getElementById('lending-section')) {
        displayUserOrders(data.lender_orders, 'lender');
    }
}

function displayUserInfo(userInfo) {
    console.log("displayUserInfo triggered");
    const infoDiv = document.getElementById("profile-card");
    if (!infoDiv) return;

    // let html = `
    //     <div class="user-info-card">
    //         <h2>${userInfo.username}</h2>
    //         <div class="info-details">
    //             <p><strong>User ID:</strong> ${userInfo.userid}</p>
    //             <p><strong>邮箱:</strong> ${userInfo.email}</p>
    //         </div>
    //     </div>
    // `;
    let html = `
    <div class="profile-header" id="profile-card">
        <div class="profile-avatar" id="profile-avatar">-</div>
        <div class="profile-name" id="profile-name">${userInfo.username}</div>
        <div class="profile-username" id="profile-email">${userInfo.email}</div>
    </div>
    `

    infoDiv.innerHTML = html;
    console.log(infoDiv.innerHTML)
    // 更新页面标题
    const titleElement = document.getElementById("page-title");
    if (titleElement) {
        titleElement.textContent = userInfo.username;
    }

    // 更新profile name (用户详情页)
    const profileName = document.getElementById("profile-name");
    if (profileName) {
        profileName.textContent = userInfo.username;
        console.log(profileName.textContent)
    }

    // 更新email
    const profileEmail = document.getElementById("profile-email");
    if (profileEmail) {
        profileEmail.textContent = userInfo.email;
    }

    // 更新头像
    const initial = userInfo.username ? userInfo.username.charAt(0).toUpperCase() : '?';
    const profileAvatar = document.getElementById("profile-avatar");
    if (profileAvatar) {
        profileAvatar.textContent = initial;
    }
    const navAvatar = document.getElementById("nav-avatar");
    if (navAvatar) {
        navAvatar.textContent = initial;
    }

    document.title = `${userInfo.username} - User Detail`;
}

function displayUserStatistics(statistics) {
    const statsDiv = document.getElementById("profile-stats");
    if (!statsDiv) return;

    // let html = `
    //     <div class="stats-container">
    //         <h3>Orders</h3>
    //         <div class="stats-grid">
    //             <div class="stat-item">
    //                 <span class="stat-label">Borrowed</span>
    //                 <span class="stat-value">${statistics.borrower_count}</span>
    //             </div>
    //             <div class="stat-item">
    //                 <span class="stat-label">Lended</span>
    //                 <span class="stat-value">${statistics.lender_count}</span>
    //             </div>
    //             <div class="stat-item">
    //                 <span class="stat-label">Total</span>
    //                 <span class="stat-value">${statistics.total_count}</span>
    //             </div>
    //         </div>
    //     </div>
    // `;
    let html = `

        <div class="stat">
            <div class="stat-value" id="items-count">${statistics.lender_count}</div>
             <div class="stat-label">Items</div>
        </div>
            <div class="stat">
                <div class="stat-value" id="total-orders">${statistics.total_count}</div>
                    <div class="stat-label">Total</div>
                </div>
                <div class="stat">
                    <div class="stat-value" id="user-rating">TBD</div>
                    <div class="stat-label">Rating</div>
                </div>

    
    `
    console.log(statistics)
    statsDiv.innerHTML = html;

    // 更新侧边栏统计（用户详情页）
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
        totalOrders.textContent = statistics.total_count;
    }
}

function displayUserOrders(orders, type) {
    console.log("display orders triggerd")
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

    // 简单显示所有订单
    let html = '';
    orders.forEach(order => {
        const statusClass = order.item_status ? 'status-available' : 'status-unavailable';
        const statusText = order.item_status ? '✓ Available' : '✗ Not Available';
        console.log(order)
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
        fetchUserDetail(currentUserId, true);
    }
}

function clearUserDetail() {
    currentUserId = null;
    currentUserData = null;
    currentOrderPage = 1;
    window.location.href = '/users';
}