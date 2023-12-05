function showDetails(imageUrl, description) {
    document.getElementById("modalImage").src = imageUrl;
    document.getElementById("modalDescription").innerHTML = description;
    document.getElementById("myModal").style.display = "flex";
}

function closeModal() {
    document.getElementById("myModal").style.display = "none";
}