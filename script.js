async function getMarineForecast() {
  try {
    const response = await fetch('https://api.weather.gov/zones/marine/LEZ146/forecast');
    const data = await response.json();
    
    // Display the forecast data
    document.getElementById('forecast').innerHTML = `
      <h2>Marine Forecast</h2>
      <p>${data.properties.forecast}</p>
    `;
  } catch (error) {
    document.getElementById('forecast').innerHTML = `<p>Sorry, we couldn't fetch the forecast. Please try again later.</p>`;
    console.error('Error fetching forecast:', error);
  }
}

// Trigger the forecast update on button click
document.getElementById('updateBtn').addEventListener('click', getMarineForecast);
