document.addEventListener("DOMContentLoaded", () => {
    const source = document.getElementById("source");
    const destination = document.getElementById("destination");
    const swapButton = document.getElementById("swapStations");
    const form = document.getElementById("routeForm");
    const submitButton = document.getElementById("findRouteBtn");

    if (swapButton && source && destination) {
        swapButton.addEventListener("click", () => {
            const sourceValue = source.value;
            const destinationValue = destination.value;
            source.value = destinationValue;
            destination.value = sourceValue;
        });
    }

    if (form && submitButton) {
        form.addEventListener("submit", (event) => {
            if (!source?.value || !destination?.value) return;

            if (source.value === destination.value) {
                event.preventDefault();
                alert("Please choose different starting and destination stations.");
                return;
            }

            submitButton.disabled = true;
            submitButton.querySelector("span:first-child").textContent = "Calculating route...";
        });
    }
});
