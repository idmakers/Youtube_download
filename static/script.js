function downloadVideo() {
    const link = document.getElementById("link").value;

    fetch(`/download?link=${encodeURIComponent(link)}`)
        .then(response => {
            if (!response.ok) {
                throw new Error("Network response was not ok");
            }
            return response.text();
        })
        .then(result => {
            console.log(result);
            alert("Video downloaded successfully!");
        })
        .catch(error => {
            console.error("Error downloading video:", error);
            alert("Error downloading video. See console for details.");
        });
}