
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

    const stats = document.createElement('div');
    stats.className = 'search-stats';
    const startRecord = data.total > 0 ? (data.page - 1) * data.size + 1 : 0;
    const endRecord = Math.min(data.page * data.size, data.total);

    stats.innerHTML = `
        <span>Showing ${startRecord} - ${endRecord} totally ${data.total} Records</span>
        <span>${data.query ? `(Searching: "${data.query}")` : '(All items)'}</span>
    `;
    paginationDiv.appendChild(stats);


    if (data.pages > 1) {
        const pageControls = document.createElement('div');
        pageControls.className = 'page-controls';


        const prevBtn = document.createElement('button');
        prevBtn.textContent = 'Previous';
        prevBtn.disabled = data.page <= 1;
        prevBtn.onclick = () => onPageChange(data.page - 1, data.size);
        pageControls.appendChild(prevBtn);


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
                pageBtn.className = num === data.page ? 'active' : '';
                pageBtn.onclick = () => onPageChange(num, data.size);
                pageControls.appendChild(pageBtn);
            }
        });

        // Next按钮
        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next';
        nextBtn.disabled = data.page >= data.pages;
        nextBtn.onclick = () => onPageChange(data.page + 1, data.size);
        pageControls.appendChild(nextBtn);

        paginationDiv.appendChild(pageControls);
    }
}

function generatePageNumbers(current, total) {
    const delta = 2;
    const range = [];
    const rangeWithDots = [];
    let l;

    for (let i = 1; i <= total; i++) {
        if (i === 1 || i === total || (i >= current - delta && i <= current + delta)) {
            range.push(i);
        }
    }

    range.forEach(i => {
        if (l) {
            if (i - l === 2) {
                rangeWithDots.push(l + 1);
            } else if (i - l !== 1) {
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