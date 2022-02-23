<!-- JS -->
<script>
	import { onMount } from "svelte"
	import SearchBar from './components/SearchBar.svelte'

	let weather_card
	let city = ''
	let cityLast = ''

	onMount(async () => {
		console.log('>>> ON MOUNT')
		const res = await fetch('http://localhost:5000/wttr/shanghai')
		const card_blob  = await res.blob()
		weather_card = URL.createObjectURL(card_blob)

		console.log(card_blob)


	})

	async function fetchWeather() {
		// input validation
		const cityName = city.replace(/\s+/g, ' ').trim()	// removes extras spaces from the string -> https://futurestud.io/tutorials/remove-extra-spaces-from-a-string-in-javascript-or-node-js

		// check if the input is empty or is the same as the last one
		if (cityName == '' || cityName == cityLast) {
			console.error('Invalid city!')
			return
		}

		// remembers the last fetched city to avoid duplicate API calls
		cityLast = cityName
		
		// fetching the data
		const res = await fetch(`http://localhost:5000/wttr/${cityName}`)
		const photo  = await res.blob()
		weather_card = URL.createObjectURL(photo)

		console.log(weather_card)
	}
</script>

<!-- HTML -->
<main>
	<header>
		<img src="Cloudy.svg" alt="cloud :)" class="cloud">
		<h1>Weather Report</h1>
	</header>
	
	<p>This is a web UI for my <a href="https://sam.freelancepolice.org/discord_bots/david_lynch">David Lynch Weather Report</a> discord bot.</p>

	<br>
	<img src={weather_card} alt="weather card shanghai" class="weather-card">
	<p>{weather_card}</p>

	<SearchBar bind:city={city} onClick={fetchWeather}/>
	

</main>