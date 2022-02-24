<!-- JS -->
<script>
    export let selected

    const options = [
        {value: 'wttr', text: 'current conditions'},
        {value: 'tmrw', text: 'tomorrow\'s forecast'},
    ]
</script>

<!-- HTML -->
<select name="today or tomorrow" id="period" class="dropdown"
    bind:value={selected} on:change="{() => console.log(selected)}">
        {#each options as option}
            <option value={option}>{option.text}</option>
        {/each}
</select>