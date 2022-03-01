<!-- Toggle button to switch between Tight mode and Dark mode -->

<!-- JS -->
<script>
    export let darkTheme = false

    const toggleTheme = () => {
        darkTheme = !darkTheme
        document.documentElement.setAttribute('dark-theme', darkTheme)
    }
</script>

<!-- HTML -->
<div class="theme-toggle" >
    <button on:click={toggleTheme}>
        <img src={darkTheme ? 'Sunny.svg' : 'Moon.svg'} alt="toggle between light/dark theme">
    </button>
</div>
