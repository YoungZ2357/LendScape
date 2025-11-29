
function displayPagination(data, onPageChange, options = {}) {

    const config = {
        containerId: 'pagination',
        containerClass: 'pagination-container',
        insertAfterId: 'results',
        ...options
    };

    let paginationDiv = document.getElementById(config.containerId);

    if (!paginationDiv) {
        paginationDiv = document.createElement('div');
        paginationDiv.id = config.containerId;
        paginationDiv.className = config.containerClass;

        const targetDiv = document.getElementById(config.insertAfterId);
        if (targetDiv) {
            targetDiv.parentNode.insertBefore(paginationDiv, targetDiv.nextSibling);
        } else {
            document.body.appendChild(paginationDiv);
        }
    }

    paginationDiv.innerHTML = '';

    // 统计信息部分
    const stats = document.createElement('div');
    stats.className = 'search-stats';
    const startRecord = data.total > 0 ? (data.page - 1) * data.size + 1 : 0;
    const endRecord = Math.min(data.page * data.size, data.total);

    stats.innerHTML = `
        <span class="page-info">
            Showing <strong>${startRecord} - ${endRecord}</strong> of <strong>${data.total}</strong> items
            ${data.query ? `<span style="color: #667eea; margin-left: 10px;">(Search: "${data.query}")</span>` : ''}
        </span>
    `;
    paginationDiv.appendChild(stats);

    // 分页控件部分
    if (data.pages > 1) {
        const pageControls = document.createElement('div');
        pageControls.className = 'page-controls';
        pageControls.style.cssText = 'display: flex; justify-content: center; align-items: center; gap: 5px; margin-top: 20px;';

        // Previous按钮
        const prevBtn = document.createElement('button');
        prevBtn.textContent = '← Previous';
        prevBtn.className = 'pagination-btn';
        prevBtn.disabled = data.page <= 1;
        prevBtn.onclick = () => onPageChange(data.page - 1, data.size);
        pageControls.appendChild(prevBtn);

        // 页码按钮
        const pageNumbers = generatePageNumbers(data.page, data.pages);
        pageNumbers.forEach(num => {
            if (num === '...') {
                const span = document.createElement('span');
                span.textContent = '...';
                span.className = 'page-ellipsis';
                pageControls.appendChild(span);
            } else {
                const pageBtn = document.createElement('button');
                pageBtn.textContent = num;
                // 使用page-number类，当前页添加active类
                pageBtn.className = num === data.page ? 'page-number active' : 'page-number';
                pageBtn.onclick = () => onPageChange(num, data.size);
                pageControls.appendChild(pageBtn);
            }
        });

        // Next按钮
        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next →';
        nextBtn.className = 'pagination-btn';
        nextBtn.disabled = data.page >= data.pages;
        nextBtn.onclick = () => onPageChange(data.page + 1, data.size);
        pageControls.appendChild(nextBtn);

        paginationDiv.appendChild(pageControls);

        // 添加页面跳转功能（可选）
        const jumpToPage = document.createElement('div');
        jumpToPage.className = 'jump-to-page';
        jumpToPage.style.cssText = 'display: flex; justify-content: center; align-items: center; gap: 10px; margin-top: 15px;';
        jumpToPage.innerHTML = `
            <span style="color: #666; font-size: 14px;">Jump to page:</span>
            <input type="number" 
                   id="pageJumpInput" 
                   min="1" 
                   max="${data.pages}" 
                   value="${data.page}"
                   style="width: 60px; padding: 5px 10px; border: 2px solid #ddd; font-size: 14px;">
            <button onclick="(() => {
                const input = document.getElementById('pageJumpInput');
                const page = parseInt(input.value);
                if (page >= 1 && page <= ${data.pages}) {
                    (${onPageChange})(page, ${data.size});
                } else {
                    alert('Please enter a valid page number (1-${data.pages})');
                }
            })()" 
                    style="padding: 5px 15px; background: #667eea; color: white; border: none; cursor: pointer; font-weight: 600;">
                Go
            </button>
        `;
        paginationDiv.appendChild(jumpToPage);
    }

    // 添加每页显示数量选择器（可选）
    if (data.total > 0) {
        const sizeSelector = document.createElement('div');
        sizeSelector.className = 'size-selector';
        sizeSelector.style.cssText = 'display: flex; justify-content: center; align-items: center; gap: 10px; margin-top: 15px;';

        const sizes = [8, 16, 24, 32];
        sizeSelector.innerHTML = `
            <span style="color: #666; font-size: 14px;">Items per page:</span>
            <select id="pageSizeSelect" 
                    onchange="(${onPageChange})(1, parseInt(this.value))"
                    style="padding: 5px 10px; border: 2px solid #ddd; font-size: 14px; cursor: pointer;">
                ${sizes.map(size =>
            `<option value="${size}" ${size === data.size ? 'selected' : ''}>${size}</option>`
        ).join('')}
            </select>
        `;

        // 只在有足够数据时显示
        if (data.total > sizes[0]) {
            paginationDiv.appendChild(sizeSelector);
        }
    }
}

function generatePageNumbers(current, total) {
    const delta = 2;  // 当前页前后显示的页码数量
    const range = [];
    const rangeWithDots = [];
    let l;

    // 确定要显示的页码
    for (let i = 1; i <= total; i++) {
        // 总是显示第一页、最后一页，以及当前页附近的页码
        if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
            range.push(i);
        }
    }

    // 添加省略号
    range.forEach(i => {
        if (l) {
            if (i - l === 2) {
                // 如果间隔只有一个页码，直接显示该页码
                rangeWithDots.push(l + 1);
            } else if (i - l !== 1) {
                // 如果间隔超过一个页码，显示省略号
                rangeWithDots.push('...');
            }
        }
        rangeWithDots.push(i);
        l = i;
    });

    return rangeWithDots;
}
function clearSearchCommon(searchMethod) {
    document.getElementById("searchInput").value = "";
    currentQuery = "";
    searchMethod(1, currentSize || 8, false);
}