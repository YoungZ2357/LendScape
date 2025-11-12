// main function for item search
// This function will change
function makeSearch() {
    const query = document.getElementById("searchInput").value.trim();
    if (!query) {
        alert("Please enter a valid search query");
        return;
    }

    const resultDiv = document.getElementById("results");
    // `/api/search_items?search=${encodeURIComponent(query)}`
    const routeUrl = `/api/search_items?search=${encodeURIComponent(query)}`;
    // window.location.origin -> https://127.0.0.1:5000
    const fullUrl = window.location.origin + routeUrl;

    resultDiv.innerHTML = '';

    fetch(fullUrl)
        .then(
            response => {
                // see app/items/routes.py/api for item search
                console.log(`Response received. Status: ${response.status}`);
                if (!response.ok) {throw new Error(`HTTP status was ${response.status}`);}
                return response.json()
            }
        )
        .then(data => {
            document.getElementById('loading').style.display = 'none';
            displaySearch(data)
    })
        .catch(error => {
            document.getElementById('loading').style.display = 'none';
            resultDiv.innerHTML = '<p>Invalid search. Please try again</p>';
            console.error(error)
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
