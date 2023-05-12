// Создаем карту и добавляем ее на страницу
const map = L.map('map').setView([34.0536909, -118.242766], 10);
var mapOptions = {
  center: {lat: 34.0522, lng: -118.2437},
  zoom: 8
};
// Добавляем слой OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  attribution: 'Map data &copy; <a href="https://www.openstreetmap.org/">OpenStreetMap</a> contributors',
  maxZoom: 18
}).addTo(map);

// Создаем группу маркеров
const markers = new L.FeatureGroup().addTo(map);

// Функция для поиска координат по названию города
const searchCity = () => {
  const city = document.querySelector('#city').value;

  if (city.length === 0) {
    return;
  }

  const url = `https://nominatim.openstreetmap.org/search?format=json&q=${city}`;

  fetch(url)
    .then(response => response.json())
    .then(data => {
      if (data.length === 0) {
        alert('Город не найден');
        return;
      }

      const { lat, lon } = data[0];

      // Устанавливаем центр карты на найденную координату
      map.setView([lat, lon], 12);

      // Создаем маркер на найденной координате
      const marker = L.marker([lat, lon]).addTo(markers);
      marker.on('click', () => {
        document.querySelector('#coordinates').value = `${lat}, ${lon}`;
      });
      document.querySelector('#coordinates').value = `${lat}, ${lon}`;
    })
    .catch(error => console.error(error));
};

// Функция для установки маркера на карте
const setMarker = (e) => {
  const lat = e.latlng.lat.toFixed(5);
  const lng = e.latlng.lng.toFixed(5);

  // Удаляем предыдущие маркеры
  markers.clearLayers();

  // Создаем маркер на выбранной координате
  const marker = L.marker(e.latlng).addTo(markers);
  marker.on('click', () => {
    document.querySelector('#coordinates').value = `${lat}, ${lng}`;
  });
  document.querySelector('#coordinates').value = `${lat}, ${lng}`;
};

// Обработчики событий для поля ввода города и карты
document.querySelector('#city').addEventListener('input', searchCity);
map.on('click', setMarker);``