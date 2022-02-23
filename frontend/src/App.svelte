<!-- JS -->
<script>
	import { onMount } from "svelte"
	import SearchBar from './components/SearchBar.svelte'

	let weather_card
	let city

	onMount(async () => {
		console.log('>>> ON MOUNT')
		const res = await fetch('http://localhost:5000/wttr/shanghai')
		const card_blob  = await res.blob()
		weather_card = URL.createObjectURL(card_blob)

		console.log(card_blob)


	})

	async function fetchWeather() {
		const res = await fetch(`http://localhost:5000/wttr/${city}`)
		const photo  = await res.blob()
		weather_card = URL.createObjectURL(photo)

		console.log(weather_card)
	}
</script>

<!-- HTML -->
<main>
	<img src="Cloudy.svg" alt="cloud :)" class="cloud">
	<h1>Weather Report</h1>
	<p>This is a web UI for my <a href="https://sam.freelancepolice.org/discord_bots/david_lynch">David Lynch Weather Report</a> discord bot.</p>

	<br>
	<img src={weather_card} alt="weather card shanghai" class="weather-card">
	<p>{weather_card}</p>

	<SearchBar bind:city={city} onClick={fetchWeather}/>
	

</main>