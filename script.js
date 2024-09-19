async function getMarineForecast() {
  try {
    const response = await fetch('https://api.weather.gov/zones/marine/LEZ148/forecast', {
      headers: {
        'User-Agent': '(myweatherapp.com, contact@myweatherapp.com)'
      }
    });
    
    if (!response.ok) {
      const errorData = await response.json(); // Get error response from the API
      throw new Error(errorData.detail || 'Network response was not ok'); // Use error message or fallback
    }
    
    const data = await response.json();
    
    // Display the forecast data
    document.getElementById('forecast').innerHTML = `
      <h2>Marine Forecast</h2>
      <p>${data.properties.forecast}</p>
    `;
  } catch (error) {
    // Display specific error message
    document.getElementById('forecast').innerHTML = `<p>Error: ${error.message}</p>`;
    console.error('Error fetching forecast:', error);
  }
}
