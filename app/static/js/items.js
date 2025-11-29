let currentQuery = '';
let currentPage = 1;
let currentSize = 8;


function makeSearchCommon(page = 1, size = 8, resetQuery = false) {
    if (resetQuery) {
        currentQuery = document.getElementById("searchInput").value.trim();
    }

    currentPage = page;
    currentSize = size;

    const resultDiv = document.getElementById("results");
    let routeUrl = `/api/items?page=${page}&size=${size}`;

    if (currentQuery) {
        routeUrl += `&search=${encodeURIComponent(currentQuery)}`;
    }

    console.log(routeUrl);
    const fullUrl = window.location.origin + routeUrl;
    console.log(fullUrl);

    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
        loadingDiv.style.display = 'block';
        loadingDiv.innerHTML = '<div class="loading-spinner"></div><p>Searching items...</p>';
    }

    fetch(fullUrl)
        .then(response => {
            console.log(`Response received. Status: ${response.status}`);
            if (!response.ok) {
                throw new Error(`HTTP status was ${response.status}`);
            }
            return response.json();
        })
        .then(data => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
                loadingDiv.innerHTML = '';
            }
            displaySearchItem(data);
        })
        .catch(error => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
                loadingDiv.innerHTML = '';
            }
            resultDiv.innerHTML = `
                <div class="empty-state">
                    <div class="empty-icon">⚠️</div>
                    <div class="empty-title">Search Error</div>
                    <div class="empty-description">Invalid search. Please try again</div>
                </div>
            `;
            console.error(error);
        });
}


function displaySearchItem(data) {
    const resultDiv = document.getElementById("results");
    console.log(data.count);

    if (data.count === 0) {
        resultDiv.innerHTML = `
            <div class="empty-items">
                <div class="empty-items-icon">🔍</div>
                <div class="empty-title">No items found</div>
                <div class="empty-description">
                    ${currentQuery ? `No results found for "${currentQuery}"` : 'No items available at the moment'}
                </div>
            </div>
        `;

        const paginationDiv = document.getElementById('pagination');
        if (paginationDiv) {
            paginationDiv.innerHTML = '';
        }
        return;
    }

    let html = '';

    data.results.forEach(item => {
        // 生成随机头像首字母（基于用户ID或物品名称）
        const avatarLetter = item.itemName ? item.itemName.charAt(0).toUpperCase() : 'U';

        // 判断物品状态（使用is_available字段，默认为true）
        const isAvailable = item.is_available !== undefined ? item.is_available : true;
        const statusClass = isAvailable ? 'available' : 'rented';
        const statusText = isAvailable ? 'Available' : 'Rented';

        // 处理价格显示
        const priceDisplay = item.price ? `$${item.price}` : 'Free';
        const priceUnit = item.priceUnit || '/day';

        // 处理类别（如果没有类别字段，可以根据描述推断或使用默认值）
        const category = item.category || 'General';

        html += `
        <div class="item-card" onclick="window.location.href='/items/${item.itemId}'">
            <div class="item-image">
                ${item.imageUrl ?
            `<img src="${item.imageUrl}" alt="${item.itemName}">` :
            `<div style="font-size: 72px;">📦</div>`
        }
                <span class="item-status ${statusClass}">${statusText}</span>
            </div>
            <div class="item-content">
                <span class="item-category">${category}</span>
                <div class="item-name">${item.itemName || 'Unnamed Item'}</div>
                <div class="item-description">${item.description || 'No description available'}</div>
                <div class="item-footer">
                    <div class="item-price">
                        ${priceDisplay}
                        ${item.price ? `<span>${priceUnit}</span>` : ''}
                    </div>
                    <div class="item-actions">
                        <button class="item-action-btn view" onclick="event.stopPropagation(); window.location.href='/items/${item.itemId}'">
                            View
                        </button>
                        ${status === 'available' ?
            `<button class="item-action-btn rent" onclick="event.stopPropagation(); rentItem(${item.itemId})">
                                Rent
                            </button>` : ''
        }
                    </div>
                </div>
                <div class="item-owner">
                    <div class="owner-avatar">${avatarLetter}</div>
                    <span class="owner-name">User #${item.userId}</span>
                </div>
                ${item.location ?
            `<div class="item-location">${item.location}</div>` :
            '<div class="item-location">Location not specified</div>'
        }
            </div>
        </div>`;
    });

    resultDiv.innerHTML = html;

    // 显示分页
    displayPagination(data, (newPage, newSize) => {
        makeSearchCommon(newPage, newSize, false);
    });
}


function clearSearchItem() {
    // 清空搜索框
    const searchInput = document.getElementById("searchInput");
    if (searchInput) {
        searchInput.value = '';
    }
    currentQuery = '';

    // 重新搜索（显示所有物品）
    makeSearchCommon(1, currentSize, false);
}


function changePageSize(size) {
    currentSize = parseInt(size);
    makeSearchCommon(currentPage || 1, currentSize, false);
}


// 租借物品函数（可选）
function rentItem(itemId) {
    console.log('Renting item:', itemId);
    // 这里可以添加租借物品的逻辑
    alert(`Rent feature for item ${itemId} is not yet implemented`);
}