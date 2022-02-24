<!-- JS -->
<script>
	import { onMount } from "svelte"
	import SearchBar from './components/SearchBar.svelte'
	import Dropdown from './components/Dropdown.svelte'

	let weather_card = ''		// URL for the weather card image to display
	let city = ''				// name of the city requested by the user
	let cityLast = ''			// the last requested city
	let command					// weather to get current conditions or tomorrow's forecast
	let forecastType = ''		// the text value of the LAST command requested

	// Loading weather card for random location on start up
	onMount(async () => {
		console.log('>>> ON MOUNT')
		const res = await fetch('http://localhost:5000/wttr/shanghai')
		const card_blob  = await res.blob()
		weather_card = URL.createObjectURL(card_blob)

		console.log(card_blob)
	})

	// Fetching the weather card PNG from the Flask API
	async function fetchWeather() {
		// input validation
		const cityName = city.replace(/\s+/g, ' ').trim()	// removes extras spaces from the string -> https://futurestud.io/tutorials/remove-extra-spaces-from-a-string-in-javascript-or-node-js

		// check if the input is empty or is the same as the last one or contains any special character/numbers
		if (cityName == '' || cityName == cityLast || !/^[A-Za-z\s]*$/.test(cityName)) {
			console.error('City name cannot be repeated, empty, nor contain special characters')
			alert('City name cannot be repeated, empty, nor contain special characters!')
			return
		}

		// remembers the last fetched city to avoid duplicate API calls
		cityLast = cityName
		
		// fetching the data
		const res = await fetch(`/${command.value}/${cityName}`)

		// checking if the response is OK
		if (!res.ok) {
			console.error('City not found!')
			weather_card = 'XP.svg'
			return
		}

		// reading the data
		const photo  = await res.blob()
		weather_card = URL.createObjectURL(photo)

		// resetting the input
		city = ''

		// setting the appropriate title
		forecastType = command.text
	}
</script>

<!-- HTML -->
<main>
	<header>
		<img src="Cloudy.svg" alt="cloud :)" class="cloud">
		<h1>Weather Report</h1>
	</header>
	
	<p>This is a web UI for my <a href="https://sam.freelancepolice.org/discord_bots/david_lynch">David Lynch Weather Report</a> discord bot.</p>

	<h2>{forecastType}</h2>
	
	<br>
	<img src={weather_card} alt="weather card shanghai" class="weather-card">
	<p>{weather_card}</p>

	<SearchBar bind:city={city} onSubmit={fetchWeather}/>

	<Dropdown bind:selected={command} />
</main>