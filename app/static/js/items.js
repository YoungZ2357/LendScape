
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
            }
            displaySearchItem(data);
        })
        .catch(error => {
            if (loadingDiv) {
                loadingDiv.style.display = 'none';
            }
            resultDiv.innerHTML = '<p>Invalid search. Please try again</p>';
            console.error(error);
        });
}


function displaySearchItem(data) {
    const resultDiv = document.getElementById("results");
    console.log(data.count);

    if (data.count === 0) {
        resultDiv.innerHTML = `<p>No results relating to ${data.query}</p>`;

        const paginationDiv = document.getElementById('pagination');
        if (paginationDiv) {
            paginationDiv.innerHTML = '';
        }
        return;
    }

    let html = `<p>${data.count} available items found</p>`;
    console.log(html);

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


    displayPagination(data, (newPage, newSize) => {
        makeSearchCommon(newPage, newSize, false);
    });
}


function clearSearch() {
    document.getElementById("searchInput").value = "";
    currentQuery = "";
    makeSearchCommon(1, currentSize || 8, false);
}


function changePageSize(size) {
    currentSize = parseInt(size);
    makeSearchCommon(currentPage || 1, currentSize, false);
}