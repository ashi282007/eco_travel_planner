document.addEventListener("DOMContentLoaded", function () {

    const slidesContainer = document.querySelector(".slides");
    if (!slidesContainer) return;

    const slides = document.querySelectorAll(".slide");
    let currentIndex = 0;

    function nextSlide() {
        currentIndex++;
        if (currentIndex >= slides.length) {
            currentIndex = 0;
        }

        slidesContainer.style.transform = "translateX(-" + currentIndex * 100 + "%)";
    }

    setInterval(nextSlide, 3000);

});