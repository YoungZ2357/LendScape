// main function for item search
// This function will change

let currentPage = 1;
let currentSize = 20;
let currentQuery = '';

// function makeSearch() {
//     const query = document.getElementById("searchInput").value.trim();
//     if (!query) {
//         alert("Please enter a valid search query");
//         return;
//     }
//
//     const resultDiv = document.getElementById("results");
//     // `/api/search_items?search=${encodeURIComponent(query)}`
//     const routeUrl = `/api/search_items?search=${encodeURIComponent(query)}`;
//     // window.location.origin -> https://127.0.0.1:5000
//     const fullUrl = window.location.origin + routeUrl;
//
//     resultDiv.innerHTML = '';
//
//     fetch(fullUrl)
//         .then(
//             response => {
//                 // see app/items/routes.py/api for item search
//                 console.log(`Response received. Status: ${response.status}`);
//                 if (!response.ok) {throw new Error(`HTTP status was ${response.status}`);}
//                 return response.json()
//             }
//         )
//         .then(data => {
//             document.getElementById('loading').style.display = 'none';
//             displaySearch(data)
//     })
//         .catch(error => {
//             document.getElementById('loading').style.display = 'none';
//             resultDiv.innerHTML = '<p>Invalid search. Please try again</p>';
//             console.error(error)
//         })
// }

function makeSearchCommon(page = 1, size = 20, resetQuery = false){
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
    console.log(routeUrl)
    const fullUrl = window.location.origin + routeUrl;
    console.log(fullUrl)
    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
        loadingDiv.style.display = 'block';
    }

    fetch(fullUrl)
        .then(
            response => {
                console.log(`Response received. Status: ${response.status}`);
                if (!response.ok) {throw new Error(`HTTP status was ${response.status}`);
                }
                return response.json();
            })
    .then(data => {
        if (loadingDiv){loadingDiv.style.display = 'none';}
        displaySearch(data);

    }).catch(error => {
        if (loadingDiv) {loadingDiv.style.display = 'none';
        resultDiv.innerHTML = '<p>Invalid search. Please try again</p>';
        console.error(error)}
    })



}


// Using structure from `models.Item` for each element in `data` since there is no modification for model in route logic
// This function will change <div> element directly so it is without a return value.
function displaySearch(data) {
    const resultDiv = document.getElementById("results");
    console.log(data.count);
    if (data.count === 0){
        resultDiv.innerHTML = `<p>No results relating to ${data.query}</p>`;
        return;
    }

    let html = `<p>${data.count} available items found</p>`;
    console.log(html)
    data.results.forEach(item => {
        html += `
        <div class="item-card">
            <h3>Item Name: ${item.itemName}</h3>
            <p>Description: ${item.description}</p>
            <p>Owner ID: ${item.userId}</p>
            <p>Price: ${item.price}</p>
        </div>`;

    });
    resultDiv.innerHTML = html;
}

function displayPagination(data) {
    let paginationDiv = document.getElementById('pagination');

    if (!paginationDiv) {
        paginationDiv = document.createElement('div');
        paginationDiv.id = 'pagination';
        paginationDiv.className = 'pagination-container';

        const resultsDiv = document.getElementById('results');
        resultsDiv.parentNode.insertBefore(paginationDiv, resultsDiv.nextSibling);
    }

    paginationDiv.innerHTML = '';

    const stats = document.createElement('div');
    stats.className = 'search-stats';
    const startRecord = data.total > 0 ? (data.page - 1) * data.size + 1 : 0;
    const endRecord = Math.min(data.page * data.size, data.total);

    stats.innerHTML = `
        <span>显示 ${startRecord} - ${endRecord} 共 ${data.total} 条记录</span>
        <span>${data.query ? `(Searching: "${data.query}")` : '(All items)'}</span>
    `;
    paginationDiv.appendChild(stats);

    if (data.pages > 1) {
        const pageControls = document.createElement('div');
        pageControls.className = 'page-controls';

        const prevBtn = document.createElement('button');
        prevBtn.textContent = 'Previous';
        prevBtn.disabled = data.page <= 1;
        prevBtn.onclick = () => makeSearchCommon(data.page - 1, data.size);
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
                pageBtn.onclick = () => makeSearchCommon(num, data.size);
                pageControls.appendChild(pageBtn);
            }
        });


        const nextBtn = document.createElement('button');
        nextBtn.textContent = 'Next';
        nextBtn.disabled = data.page >= data.pages;
        nextBtn.onclick = () => makeSearchCommon(data.page + 1, data.size);
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