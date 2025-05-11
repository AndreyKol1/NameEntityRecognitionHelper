document.getElementById('clear-database').addEventListener('click', async function (event){
    event.preventDefault();

    const confirmation = confirm("Are you sure you want to clear the database?");
    if (confirmation){
        try{
            const response = await fetch("/drop_collection", {method: 'POST'});

            if (response.ok){
                alert("The database was cleared successfully");
            } else {
                const errorData = await response.json();
                alert("Error: " + errorData.error);
            }
        } catch(error){
            alert("An error occurred: " + error.message);
        }
    }
});