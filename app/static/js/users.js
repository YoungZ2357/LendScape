function makeSearchUser(page = 1, size = 8, resetQuery = false) {
    if (resetQuery) {
        currentQuery = document.getElementById("searchInput").value.trim();
    }

    currentPage = page;
    currentSize = size;

    const resultDiv = document.getElementById("results");

    let routeUrl = `/api/users?page=${page}&size=${size}`;
    if (currentQuery) {
        routeUrl += `&kw=${encodeURIComponent(currentQuery)}`;
    }
    const fullUrl = window.location.origin + routeUrl;

    const loadingDiv = document.getElementById("loading");
    if (loadingDiv) {
        loadingDiv.style.display = "block";
    }

    fetch(fullUrl)
        .then(
            response => {
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
            const errorEl = document.createElement('p');   // 也可以用 'div'
            errorEl.style.color = 'red';                  // 让错误文字醒目
            errorEl.textContent = `Error: ${error.message || error}`; // 推荐用 textContent 防止 XSS


            resultDiv.appendChild(errorEl);
        })

}

function displaySearchUser(data) {
    const resultDiv = document.getElementById("results")
    if (data.count === 0) {
        resultDiv.innerHTML = `<p>No results relating to ${data.query}</p>`;

        const paginationDiv = document.getElementById("pagination");
        if (paginationDiv) {
            paginationDiv.innerHTML = ``;
        }
        return;
    }

    let html = `<p>${data.count} relating users found</p>`;
    console.log(html)
    data.results.forEach(user => {
        html += `
        <div class="user-card">
            <h3>User Info</h3>
            <p>Full Name: ${user.firstName} ${user.lastName}</p>
            <p></p>
        </div>
        `
    })
    resultDiv.innerHTML = html;
}

function clearSearchUser() {
    clearSearchCommon(makeSearchUser)
}