<!-- JS -->
<script>
	import { onMount } from "svelte"
	import SearchBar from './components/SearchBar.svelte'
	import Dropdown from './components/Dropdown.svelte'
	import ThemeToggle from './components/ThemeToggle.svelte'
	import FastAverageColor from 'fast-average-color'
	import getUserCity from './location'

	let weather_card = ''		// URL for the weather card image to display
	let city = ''				// name of the city requested by the user
	let prevCity = {wttr: '', tmrw: ''} // stores the previous cities requested for current weather and tomorrow's weather
	let command					// weather to get current conditions or tomorrow's forecast
	let forecastType = ''		// the text value of the LAST command requested
	let darkTheme = false		// Toggle Light/Dark theme

	// Dynamic CSS Accent Colour
	let accentColour = '#7fc5ff'
	$: cssVars = `--accent-colour: ${accentColour}`

	const fac = new FastAverageColor();

	async function getAccent(url) {
		fac.getColorAsync(url, {
			algorithm: 'dominant',
			ignoredColor: [
				[255, 255, 255, 255], // white
				[0, 0, 0, 255], // black
				[0, 0, 0, 0], // transparent
			]
		})
		.then(color => {
			console.log(color)
			accentColour = color.hex
		})
		.catch(e => {
			console.error(e)
		})
	}
	

	// Loading weather card for random location on start up
	onMount(async () => {
		console.log('>>> ON MOUNT')

		let userCity = null

		try {
			userCity = await getUserCity()
			console.log(userCity)
		} catch (error) {
			console.error(error)
			userCity = 'Los Angeles'
		}
		
		console.log(userCity)

		const res = await fetch('/wttr/' + userCity)
		const card_blob  = await res.blob()
		weather_card = URL.createObjectURL(card_blob)

		console.log(card_blob)
	})

	// Fetching the weather card PNG from the Flask API
	async function fetchWeather() {
		// input validation
		const cityName = city.replace(/\s+/g, ' ').trim()	// removes extras spaces from the string -> https://futurestud.io/tutorials/remove-extra-spaces-from-a-string-in-javascript-or-node-js

		// check if the input is empty or is the same as the last one or contains any special character/numbers
		if (cityName == '' ||
			// cityName.toLowerCase() == prevCity[command.value] ||
			!/^[A-Za-z\s]*$/.test(cityName)) {
				console.error('City name cannot be repeated, empty, nor contain special characters')
				alert('City name cannot be repeated, empty, nor contain special characters!')
				return
		}

		// remembers the last fetched city to avoid duplicate API calls
		prevCity[command.value] = city.toLowerCase()
		
		// fetching the data
		let url = `/${command.value}/${cityName}?transparent=${darkTheme}`
		const res = await fetch(url)

		// checking if the response is OK
		if (!res.ok) {
			console.error('City not found!')
			weather_card = 'XP.svg'
			return
		}

		// reading the data
		const photo  = await res.blob()
		weather_card = URL.createObjectURL(photo)
		await getAccent(weather_card)

		// resetting the input
		city = ''

		// setting the appropriate title
		forecastType = command.text
	}
</script>

<main style={cssVars}>
	<header>
		<img src="Cloudy.svg" alt="cloud :)" class="cloud">
		<h1>Weather Report</h1>
	</header>
	
	<p>This is a web UI for my <a href="https://sam.freelancepolice.org/discord_bots/david_lynch">David Lynch Weather Report</a> discord bot.</p>

	<!-- <h2>{forecastType}</h2> -->
	<Dropdown bind:selected={command} />
	
	<br>
	<img src={weather_card} alt="weather card {city}" class="weather-card">

	<SearchBar bind:city={city} onSubmit={fetchWeather}/>

	<ThemeToggle bind:darkTheme={darkTheme} />
</main>