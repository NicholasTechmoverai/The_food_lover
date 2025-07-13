<template>
    <div :style="{ '--theme-color': user?.theme || '#f97316' }"
        class="bg-white dark:bg-gray-900/70 transition-colors duration-300">
        <div class="parent relative overflow-hidden z-0 h-[500px] mt-50">
            <svg width="0" height="0" class="sr-only" aria-hidden="true" xmlns="http://www.w3.org/2000/svg"
                version="1.1">
                <defs>
                    <filter id="old-goo">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
                        <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 18 -7"
                            result="goo" />
                        <feBlend in="SourceGraphic" in2="goo" />
                    </filter>
                    <filter id="fancy-goo">
                        <feGaussianBlur in="SourceGraphic" stdDeviation="10" result="blur" />
                        <feColorMatrix in="blur" mode="matrix" values="1 0 0 0 0  0 1 0 0 0  0 0 1 0 0  0 0 0 19 -9"
                            result="goo" />
                        <feComposite in="SourceGraphic" in2="goo" operator="atop" />
                    </filter>
                </defs>
            </svg>
            <a class="bear-link" href="https://twitter.com/intent/follow?screen_name=jh3yy" target="_blank"
                rel="noreferrer noopener">
                <svg class="w-9 text-[var(--theme-color)]" viewBox="0 0 969 955" fill="currentColor"
                    xmlns="http://www.w3.org/2000/svg">
                    <circle cx="161.191" cy="320.191" r="133.191" stroke="currentColor" stroke-width="20"></circle>
                    <circle cx="806.809" cy="320.191" r="133.191" stroke="currentColor" stroke-width="20"></circle>
                    <circle cx="695.019" cy="587.733" r="31.4016" fill="currentColor"></circle>
                    <circle cx="272.981" cy="587.733" r="31.4016" fill="currentColor"></circle>
                    <path
                        d="M564.388 712.083C564.388 743.994 526.035 779.911 483.372 779.911C440.709 779.911 402.356 743.994 402.356 712.083C402.356 680.173 440.709 664.353 483.372 664.353C526.035 664.353 564.388 680.173 564.388 712.083Z"
                        fill="currentColor"></path>
                    <rect x="310.42" y="448.31" width="343.468" height="51.4986" fill="var(--theme-color)"></rect>
                    <path fill-rule="evenodd" clip-rule="evenodd"
                        d="M745.643 288.24C815.368 344.185 854.539 432.623 854.539 511.741H614.938V454.652C614.938 433.113 597.477 415.652 575.938 415.652H388.37C366.831 415.652 349.37 433.113 349.37 454.652V511.741L110.949 511.741C110.949 432.623 150.12 344.185 219.845 288.24C289.57 232.295 384.138 200.865 482.744 200.865C581.35 200.865 675.918 232.295 745.643 288.24Z"
                        fill="currentColor"></path>
                </svg>
            </a>
        </div>

        <div :style="{ '--theme-color': user?.theme || '#f97316' }" class="relative">
            <!-- Animated Background Elements -->
            <div class="fixed inset-0 overflow-hidden -z-10 opacity-10 dark:opacity-5">
                <svg width="100%" height="100%" class="absolute inset-0" xmlns="http://www.w3.org/2000/svg">
                    <defs>
                        <pattern id="bubble-pattern" x="0" y="0" width="100" height="100" patternUnits="userSpaceOnUse">
                            <circle cx="20" cy="20" r="5" fill="var(--theme-color)" opacity="0.3"></circle>
                            <circle cx="50" cy="50" r="7" fill="var(--theme-color)" opacity="0.2"></circle>
                            <circle cx="80" cy="20" r="6" fill="var(--theme-color)" opacity="0.25"></circle>
                            <circle cx="20" cy="80" r="8" fill="var(--theme-color)" opacity="0.15"></circle>
                            <circle cx="80" cy="80" r="4" fill="var(--theme-color)" opacity="0.3"></circle>
                        </pattern>
                    </defs>
                    <rect width="100%" height="100%" fill="url(#bubble-pattern)"></rect>
                </svg>
            </div>

            <div class="min-h-screen -mt-[850px] relative z-10">
                <!-- Profile Header -->
                <header v-if="!profile_loading"
                    class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 rounded-xl shadow-sm">
                    <div class="flex flex-col lg:flex-row gap-8 lg:gap-12">
                        <!-- Profile Section -->
                        <div class="flex-1 flex flex-col md:flex-row items-center md:items-start gap-8">
                            <!-- Avatar with animated border -->
                            <div class="relative group">
                                <div
                                    class="absolute -inset-1 rounded-full bg-gradient-to-r from-[var(--theme-color)] to-yellow-500 opacity-75 group-hover:opacity-100 blur transition-all duration-300">
                                </div>
                                <img :src="user_info.user.avatar"
                                    class="relative w-32 h-32 min-w-32 md:w-40 md:h-40 rounded-full border-4 border-white dark:border-gray-800 shadow-lg object-cover z-10"
                                    alt="Profile picture">
                                <button @click="changeAvatar"
                                    class="absolute -bottom-2 -right-2 bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 w-10 h-10 rounded-full flex items-center justify-center text-white shadow-md transition-all z-20 transform hover:scale-110 active:scale-95">
                                    <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                        viewBox="0 0 24 24" stroke="currentColor">
                                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                            d="M16.862 4.487l1.687-1.688a1.875 1.875 0 112.652 2.652L10.582 16.07a4.5 4.5 0 01-1.897 1.13L6 18l.8-2.685a4.5 4.5 0 011.13-1.897l8.932-8.931zm0 0L19.5 7.125M18 14v4.75A2.25 2.25 0 0115.75 21H5.25A2.25 2.25 0 013 18.75V8.25A2.25 2.25 0 015.25 6H10" />
                                    </svg>
                                </button>
                                  <div v-if="avatarChanged" class="absolute -bottom-9 left-0 flex gap-4 mt-4">
                                <button @click="saveProfileAvatar"
                                    class="flex items-center gap-2 px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition">
                                    <i class="pi pi-save"></i>
                                    Save
                                </button>

                                <button @click="reset_profile_avatar"
                                    class="flex items-center gap-2 px-4 py-2 bg-gray-300 text-gray-800 rounded-lg hover:bg-gray-400 transition">
                                    <i class="pi pi-times"></i>
                                    Cancel
                                </button>
                            </div>

                            </div>
                          


                            <!-- Profile Info -->
                            <div class="text-center md:text-left flex-1">
                                <!-- User Header Section -->
                                <div class="flex flex-row md:items-center gap-4 justify-center md:justify-start">
                                    <h1 class="text-3xl font-bold text-gray-900 dark:text-white">
                                        {{ user_info.user.username }}
                                    </h1>



                                    <!-- Verification Badge -->
                                    <div v-if="user_info.user.is_verified" class="flex items-center text-blue-500">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                                            fill="currentColor">
                                            <path fill-rule="evenodd"
                                                d="M6.267 3.455a3.066 3.066 0 001.745-.723 3.066 3.066 0 013.976 0 3.066 3.066 0 001.745.723 3.066 3.066 0 012.812 2.812c.051.643.304 1.254.723 1.745a3.066 3.066 0 010 3.976 3.066 3.066 0 00-.723 1.745 3.066 3.066 0 01-2.812 2.812 3.066 3.066 0 00-1.745.723 3.066 3.066 0 01-3.976 0 3.066 3.066 0 00-1.745-.723 3.066 3.066 0 01-2.812-2.812 3.066 3.066 0 00-.723-1.745 3.066 3.066 0 010-3.976 3.066 3.066 0 00.723-1.745 3.066 3.066 0 012.812-2.812zm7.44 5.252a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z"
                                                clip-rule="evenodd" />
                                        </svg>
                                        <span class="text-sm ml-1">Verified</span>
                                    </div>

                                    <!-- Chef Badge -->
                                    <div v-if="user_info.user.is_chef"
                                        class="flex items-center text-[var(--theme-color)]">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20"
                                            fill="currentColor">
                                            <path
                                                d="M13.586 3.586a2 2 0 112.828 2.828l-.793.793-2.828-2.828.793-.793zM11.379 5.793L3 14.172V17h2.828l8.38-8.379-2.83-2.828z" />
                                        </svg>
                                        <span class="text-sm ml-1">Chef</span>
                                    </div>
                                </div>

                                <!-- Stats Section -->
                                <div v-if="!editProfile" class="flex justify-center md:justify-start space-x-8 ">
                                    <div class="text-center">
                                        <span class="block text-3xl font-bold text-[var(--theme-color)]">
                                            {{ user_info.userMetadata.recipes_count }}
                                        </span>
                                        <span class="text-sm text-gray-500 dark:text-gray-400">Recipes</span>
                                    </div>

                                    <div v-if="user_info.user.is_chef" class="text-center">
                                        <span class="block text-3xl font-bold text-[var(--theme-color)]">
                                            {{ user_info.userMetadata.followers }}
                                        </span>
                                        <span class="text-sm text-gray-500 dark:text-gray-400">Followers</span>
                                    </div>

                                    <div class="text-center">
                                        <span class="block text-3xl font-bold text-[var(--theme-color)]">
                                            {{ user_info.userMetadata.following }}
                                        </span>
                                        <span class="text-sm text-gray-500 dark:text-gray-400">Following</span>
                                    </div>
                                </div>

                                <!-- User Details Section -->
                                <div v-if="!editProfile"
                                    class="flex flex-col justify-center items-center md:items-start mt-4 space-y-2">
                                    <span class="text-gray-500 dark:text-gray-400 text-sm">
                                        Joined {{ formatDate(user_info?.user?.created_at) }}
                                    </span>

                                    <p class="text-gray-600 dark:text-gray-200 text-lg font-semibold">
                                        <span><i class="fas fa-user"></i></span> {{ user_info.user.name || "N/A" }}
                                    </p>

                                    <p v-if="user_info.user.phone_number"
                                        class="text-gray-600 dark:text-gray-200 text-lg font-semibold">
                                        <span><i class="fas fa-phone"></i></span> {{ user_info.user.phone_number ||
                                            "N/A" }}
                                    </p>

                                    <p v-if="user_info.user.email"
                                        class="text-gray-500 dark:text-gray-50 text-lg font-semibold">
                                        <span><i class="fas fa-envelope"></i></span> {{ user_info.user.email || "N/A" }}
                                    </p>

                                    <!-- Bio Section -->
                                    <div class="w-full mt-3">
                                        <p class="text-gray-600 dark:text-gray-400 mb-1">*Bio*</p>
                                        <div v-html="user_info.user.bio || '<p class=\'text-gray-600 dark:text-gray-300\'>Food enthusiast sharing my favorite recipes</p>'"
                                            class="max-h-[200px] overflow-y-auto break-words text-gray-600 dark:text-gray-300 max-w-lg border rounded p-3 bg-gray-200/30 dark:bg-gray-700/30 border-gray-200 dark:border-gray-600">
                                        </div>
                                    </div>
                                </div>


                                <div v-if="editProfile && user_info.user.id === auth.user.id">
                                    <!-- Edit Profile Form -->
                                    <EditProfileCard ref="profile_editor" :user="user_info.user"
                                        @save="saveProfileChanges" @cancel="editProfile = false" />

                                </div>



                                <!-- Action Buttons Section -->
                                <div class="flex flex-wrap gap-3 mt-6 justify-center md:justify-start">
                                    <!-- Edit Profile Button -->
                                    <button v-if="!editProfile && user_info.user.id === auth.user.id"
                                        @click="editUserProfile"
                                        class="px-6 py-2 bg-white dark:bg-gray-700 border-2 border-[var(--theme-color)] text-[var(--theme-color)] dark:text-white rounded-full font-medium hover:bg-[var(--theme-color)] hover:text-white dark:hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                        Edit Profile
                                    </button>

                                    <button v-if="editProfile && user_info.user.id === auth.user.id"
                                        @click="saveProfileChanges"
                                        class="px-6 py-2 bg-[var(--theme-color)] text-white rounded-full font-medium hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                                        </svg>
                                        Save Changes
                                    </button>

                                    <!-- Share Profile Button -->
                                    <button @click="share"
                                        class="px-6 py-2 bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 rounded-full font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-2">
                                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                            viewBox="0 0 24 24" stroke="currentColor">
                                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                d="M8.684 13.342C8.886 12.938 9 12.482 9 12c0-.482-.114-.938-.316-1.342m0 2.684a3 3 0 110-2.684m0 2.684l6.632 3.316m-6.632-6l6.632-3.316m0 0a3 3 0 105.367-2.684 3 3 0 00-5.367 2.684zm0 9.316a3 3 0 105.368 2.684 3 3 0 00-5.368-2.684z" />
                                        </svg>
                                        Share
                                    </button>
                                    <div class="card flex justify-center">


                                        <Popover ref="op">
                                            <div class="flex flex-col gap-4 w-[25rem]">
                                                <!-- Copy Link Section -->
                                                <div>
                                                    <span class="font-medium block mb-2">Share this profile</span>
                                                    <InputGroup>
                                                        <InputText :value="profileUrl" readonly class="w-[25rem]" />
                                                        <InputGroupAddon class="cursor-pointer" @click="copyUrl()">
                                                            <i class="pi pi-copy" />
                                                        </InputGroupAddon>
                                                    </InputGroup>
                                                </div>

                                                <!-- Share Buttons -->
                                                <div>
                                                    <span class="font-medium block mb-2">Share on</span>
                                                    <ul class="list-none p-0 m-0 flex flex-col gap-3">
                                                        <li v-for="site in shares" :key="site.name"
                                                            class="flex items-center gap-3 hover:bg-gray-100 dark:hover:bg-gray-800 rounded px-2 py-1 cursor-pointer"
                                                            @click="shareOnSocial(site.name.toLowerCase())">
                                                            <i :class="site.icon" :style="{ color: site.color }"
                                                                class="text-xl w-6 text-center" />
                                                            <span class="font-medium text-sm">{{ site.name }}</span>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </Popover>
                                    </div>


                                    <!-- Theme Color Picker -->
                                    <div class="relative group">
                                        <button @click="showColorPicker = !showColorPicker"
                                            class="px-6 py-2 bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 rounded-full font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-2">
                                            <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" fill="none"
                                                viewBox="0 0 24 24" stroke="currentColor">
                                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                                    d="M7 21a4 4 0 01-4-4V5a2 2 0 012-2h4a2 2 0 012 2v12a4 4 0 01-4 4zm0 0h12a2 2 0 002-2v-4a2 2 0 00-2-2h-2.343M11 7.343l1.657-1.657a2 2 0 012.828 0l2.829 2.829a2 2 0 010 2.828l-8.486 8.485M7 17h.01" />
                                            </svg>
                                            Theme
                                        </button>

                                        <div v-if="showColorPicker"
                                            class="absolute z-20 mt-2 w-48 p-3 bg-white dark:bg-gray-800 rounded-lg shadow-xl border border-gray-200 dark:border-gray-700">
                                            <div class="grid grid-cols-5 gap-2">
                                                <button v-for="color in themeColors" :key="color.value"
                                                    @click="changeThemeColor(color.value)"
                                                    class="w-8 h-8 rounded-full focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-[var(--theme-color)]"
                                                    :class="[color.bg, user_info.user.theme === color.value ? 'ring-2 ring-offset-2 ring-[var(--theme-color)]' : '']"
                                                    :title="color.name">
                                                </button>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- Settings Panel -->
                        <div
                            class="lg:w-80 bg-gray-50/70 dark:bg-gray-800/30 backdrop-blur-sm rounded-xl p-6 shadow-inner border border-gray-200 dark:border-gray-800/50">
                            <h2
                                class="text-xl font-semibold text-gray-800 dark:text-white mb-6 flex items-center gap-2">
                                <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5 text-[var(--theme-color)]"
                                    fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z" />
                                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                        d="M15 12a3 3 0 11-6 0 3 3 0 016 0z" />
                                </svg>
                                Account Settings
                            </h2>

                            <div class="space-y-8 gap-1 flex flex-col">
                                <!-- Change Password -->
                                <button @click="changePassword"
                                    class="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-600/50 bg-white dark:bg-gray-700/50 text-gray-700 dark:text-gray-200 font-medium hover:bg-gray-50 dark:hover:bg-gray-600 hover:border-[var(--theme-color)] hover:text-[var(--theme-color)] transition-all">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M16.5 10.5V6.75a4.5 4.5 0 10-9 0v3.75m-.75 11.25h10.5a2.25 2.25 0 002.25-2.25v-6.75a2.25 2.25 0 00-2.25-2.25H6.75a2.25 2.25 0 00-2.25 2.25v6.75a2.25 2.25 0 002.25 2.25z" />
                                    </svg>
                                    Change Password
                                </button>

                                <!-- Notification Settings -->
                                <button @click="openNotificationSettings"
                                    class="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-gray-200 dark:border-gray-600/50 bg-white dark:bg-gray-700/50 text-gray-700 dark:text-gray-200 font-medium hover:bg-gray-50 dark:hover:bg-gray-600 hover:border-[var(--theme-color)] hover:text-[var(--theme-color)] transition-all">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M14.857 17.082a23.848 23.848 0 005.454-1.31A8.967 8.967 0 0118 9.75v-.7V9A6 6 0 006 9v.75a8.967 8.967 0 01-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 01-5.714 0m5.714 0a3 3 0 11-5.714 0" />
                                    </svg>
                                    Notifications
                                </button>

                                <!-- Request to be Chef -->
                                <button v-if="!user_info.user.is_chef" @click="requestChefRole"
                                    class="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-[var(--theme-color)]/50 bg-[var(--theme-color)]/5 text-[var(--theme-color)] font-medium hover:bg-[var(--theme-color)]/10 transition-all group">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M4.5 12.75l6 6 9-13.5" />
                                    </svg>
                                    <span>Request Chef Access</span>
                                    <span
                                        class="ml-auto text-xs bg-[var(--theme-color)] text-white px-2 py-1 rounded-full group-hover:bg-[var(--theme-color)]/90">Pro</span>
                                </button>

                                <!-- Verify Account -->
                                <button v-if="!user_info.user.is_verified" @click="startVerification"
                                    class="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-[var(--theme-color)]/50 bg-[var(--theme-color)]/5 text-[var(--theme-color)] font-medium hover:bg-[var(--theme-color)]/10 transition-all">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M9 12.75L11.25 15 15 9.75M21 12c0 1.268-.63 2.39-1.593 3.068a3.745 3.745 0 01-1.043 3.296 3.745 3.745 0 01-3.296 1.043A3.745 3.745 0 0112 21c-1.268 0-2.39-.63-3.068-1.593a3.746 3.746 0 01-3.296-1.043 3.745 3.745 0 01-1.043-3.296A3.745 3.745 0 013 12c0-1.268.63-2.39 1.593-3.068a3.745 3.745 0 011.043-3.296 3.746 3.746 0 013.296-1.043A3.746 3.746 0 0112 3c1.268 0 2.39.63 3.068 1.593a3.746 3.746 0 013.296 1.043 3.746 3.746 0 011.043 3.296A3.745 3.745 0 0121 12z" />
                                    </svg>
                                    Verify Account
                                </button>



                                <!-- Divider -->
                                <div class="border-t border-gray-200 dark:border-gray-600 my-3"></div>

                                <!-- Logout -->
                                <button @click="signOut"
                                    class="w-full flex items-center gap-3 px-4 py-3 rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 font-medium hover:bg-red-100 dark:hover:bg-red-900/50 transition-all">
                                    <svg class="w-5 h-5" fill="none" stroke="currentColor" stroke-width="1.5"
                                        viewBox="0 0 24 24">
                                        <path stroke-linecap="round" stroke-linejoin="round"
                                            d="M15.75 9V5.25A2.25 2.25 0 0013.5 3h-6a2.25 2.25 0 00-2.25 2.25v13.5A2.25 2.25 0 007.5 21h6a2.25 2.25 0 002.25-2.25V15m3 0l3-3m0 0l-3-3m3 3H9" />
                                    </svg>
                                    Sign Out
                                </button>
                            </div>
                        </div>
                    </div>
                </header>

                <div v-else class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <div class="flex items-center justify-center h-96">
                        <div class="animate-spin rounded-full h-16 w-16 border-t-2 border-[var(--theme-color)]"></div>
                    </div>
                </div>

                <!-- Enhanced Recipe Tabs -->
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-b border-gray-200 dark:border-gray-700">
                    <div class="flex overflow-x-auto">
                        <button @click="activeTab = 'myRecipes'"
                            :class="{ 'text-[var(--theme-color)] border-[var(--theme-color)] font-bold': activeTab === 'myRecipes', 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 border-transparent': activeTab !== 'myRecipes' }"
                            class="whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm transition-all relative group">
                            My Recipes
                            <span v-if="activeTab === 'myRecipes'"
                                class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1/2 h-1 bg-[var(--theme-color)] rounded-full"></span>
                        </button>
                        <button @click="activeTab = 'saved'"
                            :class="{ 'text-[var(--theme-color)] border-[var(--theme-color)] font-bold': activeTab === 'saved', 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 border-transparent': activeTab !== 'saved' }"
                            class="whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm transition-all relative group">
                            Saved Recipes
                            <span v-if="activeTab === 'saved'"
                                class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1/2 h-1 bg-[var(--theme-color)] rounded-full"></span>
                        </button>
                        <button @click="activeTab = 'liked'"
                            :class="{ 'text-[var(--theme-color)] border-[var(--theme-color)] font-bold': activeTab === 'liked', 'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-200 border-transparent': activeTab !== 'liked' }"
                            class="whitespace-nowrap py-4 px-6 border-b-2 font-medium text-sm transition-all relative group">
                            Liked Recipes
                            <span v-if="activeTab === 'liked'"
                                class="absolute bottom-0 left-1/2 transform -translate-x-1/2 w-1/2 h-1 bg-[var(--theme-color)] rounded-full"></span>
                        </button>
                    </div>
                </div>

                <!-- Recipe Grid -->
                <main class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                    <!-- Enhanced Empty State -->
                    <div class="text-center py-16">
                        <div
                            class="mx-auto w-48 h-48 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden mb-6 relative">
                            <div class="absolute inset-0 bg-gradient-to-br from-[var(--theme-color)]/10 to-transparent">
                            </div>
                            <img src="https://images.unsplash.com/photo-1547592180-85f173990554?w=500&auto=format"
                                class="w-full h-full object-cover opacity-70" alt="No recipes">
                        </div>
                        <h3 class="text-2xl font-bold text-gray-900 dark:text-white mb-3">
                            {{ activeTab === 'myRecipes' ? 'No recipes created yet' :
                                activeTab === 'saved' ? 'No saved recipes' : 'No liked recipes' }}
                        </h3>
                        <p class="text-gray-500 dark:text-gray-400 mb-8 max-w-md mx-auto">
                            {{ activeTab === 'myRecipes' ? 'Start sharing your culinary creations with the community' :
                                activeTab === 'saved' ? 'Save your favorite recipes to find them easily later' :
                                    'Like recipes to see them here' }}
                        </p>
                        <router-link :to="activeTab === 'myRecipes' ? '/create-recipe' : '/recipes'"
                            class="inline-flex items-center px-8 py-3 border border-transparent rounded-full shadow-sm text-white bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 font-medium">
                            {{ activeTab === 'myRecipes' ? 'Create Your First Recipe' : 'Browse Recipes' }}
                            <svg xmlns="http://www.w3.org/2000/svg" class="ml-2 -mr-1 h-5 w-5" fill="none"
                                viewBox="0 0 24 24" stroke="currentColor">
                                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2"
                                    d="M14 5l7 7m0 0l-7 7m7-7H3" />
                            </svg>
                        </router-link>
                    </div>
                </main>
            </div>
        </div>
        <Toast position="bottom-center" group="bc" />
        <input ref="fileInput" type="file" accept="image/jpeg, image/png, image/webp" class="hidden"
            @change="handleImageUpload" />
        <!-- Image Editor Dialog -->
        <Dialog v-model:visible="showImageEditor" header="Edit Cover Image"
            :style="{ width: '90vw', maxWidth: '800px' }" :modal="true" class="dark:bg-gray-800">
            <div class="space-y-4">
                <div class="relative h-[70vh] min-h-[400px] bg-gray-100 dark:bg-gray-700 rounded-lg">
                    <Cropper ref="cropper" :src="imageToEdit" :stencil-props="{ aspectRatio: 1 }"
                        class="w-full h-full" />
                </div>

                <div class="flex flex-wrap gap-2 justify-center">
                    <Button label="Rotate Left" icon="pi pi-undo" severity="secondary" @click="rotateImage(-90)"
                        class="dark:bg-gray-700" />
                    <Button label="Rotate Right" icon="pi pi-redo" severity="secondary" @click="rotateImage(90)"
                        class="dark:bg-gray-700" />
                    <!-- <Button label="Use Original" icon="pi pi-image" severity="secondary" @click="useOriginalImage"
                        class="dark:bg-gray-700" /> -->
                    <Button label="Crop & Save" icon="pi pi-check" @click="saveEditedImage"
                        :style="{ backgroundColor: user_info.user.theme, borderColor: user_info.user.theme }"
                        class="hover:opacity-90 transition-opacity" />
                    <Button label="Cancel" icon="pi pi-times" severity="secondary" @click="showImageEditor = false"
                        class="dark:bg-gray-700" />
                </div>
            </div>
        </Dialog>
    </div>
</template>

<script setup>
import { onMounted, ref, watch, computed } from 'vue';
import EditProfileCard from '../cards/EditProfile.vue';
import { make_a_post } from '../apis';
import { useAuthStore } from '../store/user';
import { formatDate } from '../reusables/index.js';
import { useToast } from 'primevue/usetoast'
import { useSiteStore } from '../config/siteConfig.js';
import { Cropper } from 'vue-advanced-cropper';
import 'vue-advanced-cropper/dist/style.css';
const { siteConfig } = useSiteStore()

const auth = useAuthStore();

const props = defineProps({
    username: {
        type: String,
        required: true
    }
})


const user_info = ref({
    user: {
        id: null,
        username: '',
        avatar: '',
        bio: '',
        name: '',
        email: '',
        created_at: '',
        phone_number: '',
        website: '',
        theme: '',
        is_verified: false,
        is_chef: false,
    },
    userMetadata: {
        star_rating: 0,
        recipes_count: 0,
        followers: 0,
        following: 0,
    }
});

const untouched_user_avatar = ref('');

const showImageEditor = ref(false);
const fileInput = ref(null);
const imageToEdit = ref('');
const activeTab = ref('myRecipes');
const userRecipes = ref([]);
const darkMode = ref(false);
const showColorPicker = ref(false);
const editProfile = ref(false);
const profile_loading = ref(false);
const toast = useToast();
const cropper = ref(null);
const saving_profile_avatar = ref(null)
const themeColors = [
    { name: 'Emerald', value: '#10B981', bg: 'bg-emerald-500' },
    { name: 'Blue', value: '#3B82F6', bg: 'bg-blue-500' },
    { name: 'Indigo', value: '#6366F1', bg: 'bg-indigo-500' },
    { name: 'Purple', value: '#8B5CF6', bg: 'bg-purple-500' },
    { name: 'Pink', value: '#EC4899', bg: 'bg-pink-500' },
    { name: 'Red', value: '#EF4444', bg: 'bg-red-500' },
    { name: 'Orange', value: '#F97316', bg: 'bg-orange-500' },
    { name: 'Yellow', value: '#F59E0B', bg: 'bg-yellow-500' },
    { name: 'Teal', value: '#14B8A6', bg: 'bg-teal-500' },
    { name: 'Cyan', value: '#06B6D4', bg: 'bg-cyan-500' }
];


const changeThemeColor = (color) => {
    user.value.theme = color;
    showColorPicker.value = false;
    // Save to backend in real implementation
};

const editUserProfile = () => {
    editProfile.value = true;
    console.log('Edit profile clicked');
};

const profile_editor = ref(null)
const saving_profile = ref(false)
const saveProfileChanges = async () => {
    if (!profile_editor.value) return;
    saving_profile.value = true

    const res = await profile_editor.value.saveProfile();

    if (res?.success && res.data) {
        user_info.value.user = { ...res.data.user };
        auth.setUser({
            id: res.data.user.id,
            name: res.data.user.username,
            isVerified: res.data.user.is_verified,
            isChef: res.data.user.is_chef,
            profilePic: res.data.user.avatar,
        });

        toast.add({
            severity: 'success',
            summary: 'Profile Updated',
            detail: res.data.message,
            life: 3000,
            group: 'bc'
        });
    } else {
        toast.add({
            severity: 'error',
            summary: 'Update Failed',
            detail: res?.message || 'Failed to update profile. Please try again later.',
            life: 3000,
            group: 'bc'
        });
    }

    editProfile.value = false;
    saving_profile.value = false
};
const copyUrl = () => {
    if (!profileUrl.value) return;
    navigator.clipboard.writeText(profileUrl.value);
    toast.add({
        severity: 'success',
        summary: 'Copied!',
        detail: 'Recipe URL copied to clipboard',
        life: 2000,
        group: 'bc'
    });
};
const profileUrl = computed(() => {
    if (!props.username) return '';
    return `${window.location.origin}/${props.username}`;
});


const op = ref();
const shares = ref([
    {
        name: 'WhatsApp',
        icon: 'pi pi-whatsapp',
        color: '#25D366',
        url: `https://wa.me/?text=${encodeURIComponent(profileUrl.value)}`
    },
    {
        name: 'Facebook',
        icon: 'pi pi-facebook',
        color: '#3b5998',
        url: `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(profileUrl.value)}`
    },
    {
        name: 'Twitter',
        icon: 'pi pi-twitter',
        color: '#1DA1F2',
        url: `https://twitter.com/intent/tweet?url=${encodeURIComponent(profileUrl.value)}&text=Check this recipe!`
    },
    {
        name: 'Email',
        icon: 'pi pi-envelope',
        color: '#EA4335',
        url: `mailto:?subject=Check this recipe&body=${encodeURIComponent(profileUrl.value)}`
    }
]);


const share = (event) => {
    op.value.toggle(event);
}

const shareOnSocial = (platform) => {
    if (!profileUrl.value) return;

    let url = '';
    const text = `Check out my Profile on ${siteConfig.meta.siteName}`;

    switch (platform) {
        case 'facebook':
            url = `https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(profileUrl.value)}`;
            break;
        case 'twitter':
            url = `https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(profileUrl.value)}`;
            break;
        case 'whatsapp':
            url = `https://wa.me/?text=${encodeURIComponent(`${text} ${profileUrl.value}`)}`;
            break;
    }

    window.open(url, '_blank', 'noopener,noreferrer');
};

const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    // Check file size (max 5MB)
    if (file.size > 5 * 1024 * 1024) {
        alert('Image size should be less than 5MB');
        return;
    }

    // Check file type
    if (!file.type.match('image.(jpeg|png|webp)')) {
        alert('Please upload a JPG, PNG, or WEBP image');
        return;
    }

    const reader = new FileReader();
    reader.onload = (e) => {
        imageToEdit.value = e.target.result;
        showImageEditor.value = true;
    };
    reader.readAsDataURL(file);
};

const openImageEditor = () => {
    if (user_info.value.user.avatar) {
        imageToEdit.value = user_info.value.user.avatar;
        showImageEditor.value = true;
    }
};

const rotateImage = (degrees) => {
    if (cropper.value) {
        cropper.value.rotate(degrees);
    }
};

const useOriginalImage = () => {
    user_info.value.user.avatar = imageToEdit.value;
    showImageEditor.value = false;
};

const reset_profile_avatar = () => {
    user_info.value.user.avatar = untouched_user_avatar.value
}

const saveProfileAvatar = async () => {
    saving_profile_avatar.value = true;

    try {
        const res = await make_a_post(
            `/users/update/${user_info.value.user.username}`,
            auth.token,
            {
                email: user_info.value.user.email,
                user_id: user_info.value.user.id,
                avatar: user_info.value.user.avatar,
            }
        );

        if (res?.success && res.data) {
            // Update untouched user snapshot to reflect new avatar
            untouched_user_avatar.value = user_info.value.user.avatar
            toast.add({
                severity: 'success',
                summary: 'Avatar Updated',
                detail: 'Your profile picture was updated successfully.',
                life: 3000,
                group: 'bc',
            });
        } else {
            toast.add({
                severity: 'error',
                summary: 'Update Failed',
                detail: res?.message || 'Could not update avatar. Please try again later.',
                life: 3000,
                group: 'bc',
            });
        }
    } catch (error) {
        console.error('Error updating avatar:', error);
        toast.add({
            severity: 'error',
            summary: 'Error Occurred',
            detail: 'An unexpected error occurred. Please try again later.',
            life: 3000,
            group: 'bc',
        });
    } finally {
        saving_profile_avatar.value = false;
    }
};




const saveEditedImage = () => {
    if (cropper.value) {
        const { canvas } = cropper.value.getResult();
        if (canvas) {
            user_info.value.user.avatar = canvas.toDataURL('image/webp', 0.9);
        } else {
            user_info.value.user.avatar = imageToEdit.value;
        }
        showImageEditor.value = false;
    }
};

const changeAvatar = () => {
    fileInput.value.click();
    console.log('Change avatar clicked');
};

const changePassword = () => {
    console.log('Change password clicked');
};

const openNotificationSettings = () => {
    console.log('Notification settings clicked');
};

const requestChefRole = () => {
    console.log('Request chef role clicked');
};

const startVerification = () => {
    console.log('Start verification clicked');
};

const signOut = () => {
    auth.setToken(null)
    auth.setUser(null)
};

const load_user = async () => {
    profile_loading.value = true;
    if (!props.username) {
        toast.add({
            severity: 'error',
            summary: 'Failed to load user',
            detail: 'Username prop is required',
            life: 5000,
            group: 'bc'
        })
        return;
    }
    if (!auth.token) {
        toast.add({
            severity: 'error',
            summary: 'Authentication Error',
            detail: 'You must be logged in to view this profile.',
            life: 5000,
            group: 'bc'
        });
        return;
    }

    try {
        const res = await make_a_post(`/users/${props.username}`, auth.token, {});
        if (res.success) {
            user_info.value = res.data;
            untouched_user_avatar.value = user_info.value.user.avatar;

        } else {
            if (res?.message) {
                toast.add({
                    severity: 'error',
                    summary: 'Failed to load user',
                    detail: res.message,
                    life: 5000,
                    group: 'bc'
                })
            }
            console.error('Failed to load user:', res.message);
        }
    } catch (error) {
        console.error('Error loading user:', error);
    }
    profile_loading.value = false;
};
const avatarChanged = computed(() => user_info.value.user.avatar !== untouched_user_avatar.value);

onMounted(() => {
    load_user();
});

watch(() => props.username, (newVal) => {
    if (newVal) {
        load_user();
    }
}, { immediate: true });

</script>

<script>
export default {
    components: {
        EditProfileCard
    }
}
</script>


<style>
/* Add any custom styles here if needed */
</style>
<style scoped>
@import url("https://unpkg.com/normalize.css") layer(normalize);

@layer normalize, base, demo;


@layer base {

    *,
    *:after,
    *:before {
        box-sizing: border-box;
    }

    .parent {
        display: grid;
        place-items: center;
        min-height: 100vh;
        font-family: "SF Pro Text", "SF Pro Icons", "AOS Icons", "Helvetica Neue",
            Helvetica, Arial, sans-serif, system-ui;
    }

    .parent::before {
        --size: 45px;
        --line: color-mix(in lch, canvasText, transparent 70%);
        content: "";
        height: 100vh;
        width: 100vw;
        position: fixed;
        background: linear-gradient(90deg,
                var(--line) 1px,
                transparent 1px var(--size)) 50% 50% / var(--size) var(--size),
            linear-gradient(var(--line) 1px, transparent 1px var(--size)) 50% 50% / var(--size) var(--size);
        mask: linear-gradient(-20deg, transparent 50%, white);
        top: 0;
        transform-style: flat;
        pointer-events: none;
        z-index: -1;
    }

    .bear-link {
        color: canvasText;
        position: fixed;
        top: 1rem;
        left: 1rem;
        width: 48px;
        aspect-ratio: 1;
        display: grid;
        place-items: center;
        opacity: 0.8;
        z-index: 9999;
    }

    :where(.x-link, .bear-link):is(:hover, :focus-visible) {
        opacity: 1;
    }

    .bear-link svg {
        width: 75%;
    }

    /* Utilities */
    .sr-only {
        position: absolute;
        width: 1px;
        height: 1px;
        padding: 0;
        margin: -1px;
        overflow: hidden;
        clip: rect(0, 0, 0, 0);
        white-space: nowrap;
        border-width: 0;
    }
}
</style>