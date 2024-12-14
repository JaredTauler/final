const targetDiv = document.getElementById('target-div')

function populatePicker(data) {
    data.forEach(program =>{
        let new_e = document.createElement('div')
        new_e.textContent = program['name']
        new_e.classList.add(
            'node'
        )
        new_e.classList.add(
            'clickable_node'
        )
        new_e.setAttribute('depth', 0);

        new_e.onclick = () => {
            window.location = `/picker/${program['id']}`
        }
        targetDiv.appendChild(new_e)
    })
}

document.addEventListener("DOMContentLoaded", () => {
    // Function to fetch data from the server
    async function fetchData() {
        try {
            // Send a GET request to the server
            const response = await fetch(`/api/programs`);

            // Parse the JSON response
            const data = await response.json();
            console.log(response)
            if (data['error']) {
                alert(`Something went wrong.\nSomething: \"${data['error']}\"`)
            } else {



                populatePicker(data)
                // processNode(
                //     data,
                //     document.getElementsByClassName("node")[0]
                // )
                // Insert data into the table
                // populateTable(data);
            }
        } catch (error) {
            console.error("Error fetching data:", error);
        }
    }

    // Fetch data when the page loads
    fetchData();
});

