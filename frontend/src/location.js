// This script fetches a user's city name by looking up their IP, then using that to get location info

export default async function getUserCity() {
    // Fetching user IP
    const ipRes = await fetch('https://json.geoiplookup.io/')

    // checking if the response is OK
    if (!ipRes.ok) {
        console.error('Error fetching user IP address')
        throw Error('Error fetching user IP address')
    }
    const ipData = await ipRes.json()

    // Fetching user city
    const cityRes = await fetch(`https://get.geojs.io/v1/ip/geo/${ipData.ip}.json`)

    // checking if the response is OK
    if (!cityRes.ok) {
        console.error(cityRes)
        throw Error('Error fetching user\'s location')
    }

    // Returning the user's city
    const cityData = await cityRes.json()
    return cityData.city
}