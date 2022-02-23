<!-- JS -->
<script>
    export let onSubmit = () => {}
    export let city
    
    // Fetches the data when the Enter Key is pressed on the input field
    const onKeyDown = (event) => {
        if (event.key == "Enter") onSubmit();
    }
</script>

<!-- HTML -->
<div class="search-bar">
    <input type="text" name="" id="" placeholder="City" bind:value={city} on:keydown={onKeyDown}>
	<button on:click={onSubmit}>Get weather!!</button>
</div>
