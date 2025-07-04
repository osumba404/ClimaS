// Dynamic % display for deforestation slider
const deforestationSlider = document.getElementById('deforestation_factor');
const deforestationValue = document.getElementById('deforestation_value');

if (deforestationSlider) {
    deforestationSlider.addEventListener('input', () => {
        deforestationValue.textContent = Math.round(deforestationSlider.value * 100) + "%";
    });
}
