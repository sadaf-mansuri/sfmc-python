// Import Axios
const axios = require('axios');

// Function to call the JSONPlaceholder API and get posts
async function fetchPosts() {
    try {
        // Make a GET request to the JSONPlaceholder API
        const response = await axios.get('https://jsonplaceholder.typicode.com/posts');
        
        // Display the result in the console
        console.log("Posts Data:", response.data);
    } catch (error) {
        // Handle errors
        console.error("Error fetching data:", error);
    }
}

// Call the function
fetchPosts();
