<template>
    <div>
        <h1 class="text-2xl font-bold mb-4">Preference Settings</h1>
        <p class="mb-6">Customize your preferences below:</p>

        <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-4">Notification Settings</h2>
                <label class="block mb-2">
                    <input type="checkbox" class="mr-2" />
                    Email Notifications
                </label>
                <label class="block mb-2">
                    <input type="checkbox" class="mr-2" />
                    SMS Notifications
                </label>
            </div>

            <div class="bg-white p-6 rounded-lg shadow">
                <h2 class="text-xl font-semibold mb-4">Privacy Settings</h2>
                <label class="block mb-2">
                    <input type="checkbox" class="mr-2" />
                    Share Data with Third Parties
                </label>
                <label class="block mb-2">
                    <input type="checkbox" class="mr-2" />
                    Enable Location Tracking
                </label>
            </div>
        </div>

        <button class="mt-6 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors">
            Save Preferences
        </button>
    </div>
</template>