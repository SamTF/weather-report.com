<!-- JS -->
<script>
    export let onClick
    export let city
</script>

<!-- HTML -->
<div class="search-bar">
    <input type="text" name="" id="" placeholder="City" bind:value={city}>
	<button on:click={onClick}>Get weather!!</button>
</div>
