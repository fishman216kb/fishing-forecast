async function getMarineForecast() {
  try {
    const response = await fetch('https://api.weather.gov/zones/marine/LEZ148/forecast', {
      headers: {
        'User-Agent': '(myweatherapp.com, contact@myweatherapp.com)'
      }
    });
    if (!response.ok) {
      throw new Error('Network response was not ok: ' + response.statusText);
    }
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
