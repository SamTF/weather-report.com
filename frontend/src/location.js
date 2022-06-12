// This script fetches a user's city name by looking up their IP, then using that to get location info

export default async function getUserCity() {
    // Fetching user city
    const cityRes = await fetch(`https://get.geojs.io/v1/ip/geo.json`)

    // checking if the response is OK
    if (!cityRes.ok) {
        console.error(cityRes)
        throw Error('Error fetching user\'s location')
    }

    // Returning the user's city
    const cityData = await cityRes.json()
    return cityData.city
}