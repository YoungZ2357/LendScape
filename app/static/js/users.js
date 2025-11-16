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
        .then(
            response => {
                if (!response)
            }
        )
}