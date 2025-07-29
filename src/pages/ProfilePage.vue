<template>
    <div :style="{ '--theme-color': user_info.user?.theme || '#f97316' }"
        class="bg-white  dark:bg-gray-900/70 transition-colors duration-300">
        <div ref="topElementRef" class="parent relative overflow-hidden h-screen z-0  ">
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

        <div :style="{ '--theme-color': user_info.user?.theme || '#f97316', marginTop: `-${topHeight}px` }"
            class="relative b_content">
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

            <div class="min-h-screen  relative z-10">
                <!-- Profile Header -->
                <header v-if="!profile_loading"
                    class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 md:py-12 rounded-xl shadow-sm">
                    <div class="flex flex-col lg:flex-row gap-8 lg:gap-12">
                        <!-- ========== PROFILE SECTION ========== -->
                        <div class="flex-1 flex flex-col md:flex-row items-center md:items-start gap-6 md:gap-8">
                            <!-- Avatar Container -->
                            <div class="relative group shrink-0">
                                <!-- Glowing Background Effect -->
                                <div
                                    class="absolute -inset-1 rounded-full bg-gradient-to-r from-[var(--theme-color)] to-yellow-500 opacity-70 group-hover:opacity-100 blur transition-all duration-300">
                                </div>

                                <!-- Avatar Image -->
                                <img :src="user_info.user.avatar"
                                    class="relative w-28 h-28 sm:w-32 sm:h-32 md:w-40 md:h-40 rounded-full border-4 border-white dark:border-gray-800 shadow-lg object-cover z-10"
                                    alt="Profile picture" />

                                <!-- Edit Avatar Button (Visible to owner) -->
                                <button v-if="user_info.user.id === auth.user.id" @click="changeAvatar"
                                    class="absolute -bottom-2 -right-2 bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 w-9 h-9 sm:w-10 sm:h-10 rounded-full flex items-center justify-center text-white shadow-md transition-transform duration-200 z-20 transform hover:scale-110 active:scale-95">
                                    <i class="pi pi-pencil text-sm sm:text-base"></i>
                                </button>

                                <!-- Avatar Action Buttons (When editing) -->
                                <div v-if="avatarChanged && user_info.user.id === auth.user.id"
                                    class="absolute -bottom-12 left-1/2 -translate-x-1/2 flex gap-2 sm:gap-3 bg-white dark:bg-gray-900 px-3 py-1.5 sm:px-4 sm:py-2 rounded-xl shadow-md z-30 mt-4 animate-fade-in">
                                    <button @click="saveProfileAvatar"
                                        class="flex items-center gap-1 sm:gap-2 px-3 py-1 sm:px-4 sm:py-1.5 bg-green-600 hover:bg-green-700 text-white rounded-lg shadow transition-transform duration-200 hover:scale-105 text-sm sm:text-base">
                                        <i class="pi pi-save text-xs sm:text-sm"></i>
                                        <span>Save</span>
                                    </button>

                                    <button @click="reset_profile_avatar"
                                        class="flex items-center gap-1 sm:gap-2 px-3 py-1 sm:px-4 sm:py-1.5 bg-gray-200 hover:bg-gray-300 text-gray-800 rounded-lg shadow transition-transform duration-200 hover:scale-105 text-sm sm:text-base">
                                        <i class="pi pi-times text-xs sm:text-sm"></i>
                                        <span>Cancel</span>
                                    </button>
                                </div>
                            </div>

                            <!-- Profile Information -->
                            <div class="text-center md:text-left flex-1 w-full">
                                <!-- User Header -->
                                <div
                                    class="flex flex-col sm:flex-row sm:items-center gap-2 sm:gap-4 justify-center md:justify-start">
                                    <h1 class="text-2xl sm:text-3xl font-bold text-gray-900 dark:text-white">
                                        {{ user_info.user.username }}
                                    </h1>

                                    <!-- Badges -->
                                    <div class="flex items-center justify-center gap-2 sm:gap-4">
                                        <!-- Verification Badge -->
                                        <div v-if="user_info.user.is_verified" class="flex items-center text-blue-500">
                                            <i class="pi pi-verified text-sm sm:text-base"></i>
                                            <span class="text-xs sm:text-sm ml-1">Verified</span>
                                        </div>

                                        <!-- Chef Badge -->
                                        <div v-if="user_info.user.is_chef"
                                            class="flex items-center text-[var(--theme-color)]">
                                            <i class="pi pi-users text-sm sm:text-base"></i>
                                            <span class="text-xs sm:text-sm ml-1">Chef</span>
                                        </div>
                                    </div>
                                </div>

                                <!-- ========== STATS SECTION ========== -->
                                <div v-if="!editProfile"
                                    class="flex justify-center md:justify-start space-x-4 sm:space-x-6 md:space-x-8 mt-4">
                                    <!-- Recipes Count -->
                                    <div class="text-center">
                                        <span class="block text-2xl sm:text-3xl font-bold text-[var(--theme-color)]">
                                            {{ user_info.userMetadata.recipes_count }}
                                        </span>
                                        <span class="text-xs sm:text-sm text-gray-500 dark:text-gray-400">Recipes</span>
                                    </div>

                                    <!-- Followers (Chefs only) -->
                                    <div v-if="user_info.user.is_chef" class="text-center">
                                        <span class="block text-2xl sm:text-3xl font-bold text-[var(--theme-color)]">
                                            {{ user_info.userMetadata.followers }}
                                        </span>
                                        <span @click="toggle_followers"
                                            class="underline cursor-pointer text-xs sm:text-sm text-gray-500 dark:text-gray-400">
                                            Followers
                                        </span>

                                        <!-- Followers Popover -->
                                        <Popover ref="follwrs">
                                            <div
                                                class="flex flex-col max-h-96 overflow-y-auto p-4 w-72 bg-white dark:bg-gray-900 rounded-lg shadow-lg">
                                                <span class="font-semibold text-lg mb-3">Followers</span>

                                                <ul v-if="loading_followers">
                                                    <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
                                                </ul>

                                                <ul v-else class="space-y-2">
                                                    <li v-for="follower in followers" :key="follower.id"
                                                        class="flex items-center gap-3 p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer transition">
                                                        <img :src="follower.avatar" alt="avatar"
                                                            class="w-10 h-10 rounded-full object-cover" />

                                                        <router-link :to="`${follower.username}`" class="flex-1">
                                                            <div
                                                                class="font-medium text-sm text-gray-900 dark:text-white">
                                                                {{ follower.name }}
                                                            </div>
                                                            <div class="text-xs text-gray-500 dark:text-gray-400">
                                                                @{{ follower.username }}
                                                            </div>
                                                        </router-link>

                                                        <!-- Follow/Unfollow Button -->
                                                        <button v-if="follower.isChef && follower.id !== auth.user.id"
                                                            @click.stop="toggleFollow(follower.id)"
                                                            class="text-xs px-3 py-1 rounded-full font-semibold transition duration-200"
                                                            :class="follower.isFollowing ? 'bg-red-100 text-red-600 hover:bg-red-200' : 'bg-blue-100 text-blue-600 hover:bg-blue-200'">
                                                            {{ follower.isFollowing ? 'Unfollow' : 'Follow' }}
                                                        </button>
                                                    </li>
                                                </ul>

                                                <!-- Pagination Controls -->
                                                <div class="flex justify-between items-center mt-4 gap-4">
                                                    <button v-if="followers && followers_offset >= followers_limit"
                                                        @click="fetch_followers(followers_limit, followers_offset - followers_limit)"
                                                        class="px-4 py-1 text-sm rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200">
                                                        Prev
                                                    </button>

                                                    <button
                                                        v-if="followers_offset + followers_limit < user_info.userMetadata.followers"
                                                        @click="fetch_followers(followers_limit, followers_offset + followers_limit)"
                                                        class="px-4 py-1 text-sm rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200">
                                                        Next
                                                    </button>
                                                </div>
                                            </div>
                                        </Popover>
                                    </div>

                                    <!-- Following -->
                                    <div class="text-center">
                                        <span class="block text-2xl sm:text-3xl font-bold text-[var(--theme-color)]">
                                            {{ user_info.userMetadata.following }}
                                        </span>
                                        <span @click="toggle_followings"
                                            class="underline cursor-pointer text-xs sm:text-sm text-gray-500 dark:text-gray-400">
                                            Following
                                        </span>

                                        <!-- Following Popover -->
                                        <Popover ref="follwng">
                                            <div
                                                class="flex flex-col max-h-96 overflow-y-auto p-4 w-72 bg-white dark:bg-gray-900 rounded-lg shadow-lg">
                                                <span class="font-semibold text-lg mb-3">Following</span>

                                                <ul v-if="loading_following">
                                                    <i class="pi pi-spin pi-spinner" style="font-size: 2rem"></i>
                                                </ul>

                                                <ul v-else class="space-y-2">
                                                    <li v-for="follower in following" :key="follower.id"
                                                        class="flex items-center gap-3 p-2 hover:bg-gray-100 dark:hover:bg-gray-800 rounded-lg cursor-pointer transition">
                                                        <img :src="follower.avatar" alt="avatar"
                                                            class="w-10 h-10 rounded-full object-cover" />

                                                        <router-link :to="`${follower.username}`" class="flex-1">
                                                            <div
                                                                class="font-medium text-sm text-gray-900 dark:text-white">
                                                                {{ follower.name }}
                                                            </div>
                                                            <div class="text-xs text-gray-500 dark:text-gray-400">
                                                                @{{ follower.username }}
                                                            </div>
                                                        </router-link>

                                                        <!-- Follow/Unfollow Button -->
                                                        <button v-if="follower.id !== auth.user.id"
                                                            @click.stop="toggleFollow(follower)"
                                                            class="text-xs px-3 py-1 rounded-full font-semibold transition duration-200"
                                                            :class="follower.isFollowing ? 'bg-red-100 text-red-600 hover:bg-red-200' : 'bg-blue-100 text-blue-600 hover:bg-blue-200'">
                                                            {{ follower.isFollowing ? 'Unfollow' : 'Follow' }}
                                                        </button>
                                                    </li>
                                                </ul>

                                                <!-- Pagination Controls -->
                                                <div class="flex justify-between items-center mt-4 gap-4">
                                                    <button v-if="following && following_offset >= following_limit"
                                                        @click="fetch_following(following_limit, following_offset - following_limit)"
                                                        class="px-4 py-1 text-sm rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200">
                                                        Prev
                                                    </button>

                                                    <button
                                                        v-if="following_offset + following_limit < user_info.userMetadata.following"
                                                        @click="fetch_following(following_limit, following_offset + following_limit)"
                                                        class="px-4 py-1 text-sm rounded bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 text-gray-800 dark:text-gray-200">
                                                        Next
                                                    </button>
                                                </div>
                                            </div>
                                        </Popover>
                                    </div>

                                    <!-- Follow Button -->
                                    <div v-if="user_info?.user.id !== auth.user.id">
                                        <!-- Follow / Unfollow Button -->
                                        <Button
                                            v-if="!NowFollowing && (user_info?.userMetadata?.isFollowing || user_info?.user?.is_chef)"
                                            @click="follow(user_info?.user.id)"
                                            :label="user_info?.userMetadata?.isFollowing ? 'Unfollow' : 'Follow'"
                                            :severity="user_info?.userMetadata?.isFollowing ? 'danger' : 'primary'"
                                            variant="outlined" :class="[
                                                'text-xs px-3 py-1 rounded-full border transition',
                                                'border-[var(--theme-color)] text-[var(--theme-color)]',
                                                'hover:bg-[var(--theme-color)] hover:text-white'
                                            ]"
                                            :style="!user_info?.userMetadata?.isFollowing ? { color: user_info?.user?.theme } : {}" />

                                        <!-- Loading State -->
                                        <span v-else-if="NowFollowing"
                                            class="text-xs px-3 py-1 rounded-full border border-[var(--theme-color)] text-[var(--theme-color)] opacity-70 cursor-not-allowed">
                                            <span v-if="user_info?.userMetadata?.isFollowing">Unfollowing...</span>
                                            <span v-else>Following...</span>
                                        </span>
                                    </div>

                                </div>



                                <!-- ========== USER DETAILS SECTION ========== -->
                                <div v-if="!editProfile"
                                    class="flex flex-col justify-center items-center md:items-start mt-4 space-y-1 sm:space-y-2">
                                    <span class="text-gray-500 dark:text-gray-400 text-xs sm:text-sm">
                                        Joined {{ formatDate(user_info?.user?.created_at) }}
                                    </span>

                                    <p class="text-gray-600 dark:text-gray-200 text-base sm:text-lg font-semibold">
                                        <i class="pi pi-user text-sm sm:text-base mr-1"></i>
                                        {{ user_info.user.name || "N/A" }}
                                    </p>

                                    <p v-if="user_info.user.phone_number"
                                        class="text-gray-600 dark:text-gray-200 text-base sm:text-lg font-semibold">
                                        <i class="pi pi-phone text-sm sm:text-base mr-1"></i>
                                        {{ user_info.user.phone_number || "N/A" }}
                                    </p>

                                    <p v-if="user_info.user.email"
                                        class="text-gray-500 dark:text-gray-50 text-base sm:text-lg font-semibold">
                                        <i class="pi pi-envelope text-sm sm:text-base mr-1"></i>
                                        {{ user_info.user.email || "N/A" }}
                                    </p>

                                    <!-- Bio Section -->
                                    <div class="w-full mt-2 sm:mt-3">
                                        <p class="text-gray-600 dark:text-gray-400 mb-1 text-sm sm:text-base">*Bio*</p>
                                        <div v-html="user_info.user.bio || '<p class=\'text-gray-600 dark:text-gray-300\'>Food enthusiast sharing my favorite recipes</p>'"
                                            class="max-h-[200px] overflow-y-auto break-words text-gray-600 dark:text-gray-300 max-w-lg border rounded p-2 sm:p-3 bg-gray-200/30 dark:bg-gray-700/30 border-gray-200 dark:border-gray-600 text-sm sm:text-base">
                                        </div>
                                    </div>
                                </div>

                                <!-- Edit Profile Form -->
                                <div v-if="editProfile && user_info.user.id === auth.user.id">
                                    <EditProfileCard ref="profile_editor" :user="user_info.user"
                                        @save="saveProfileChanges" @cancel="editProfile = false" />
                                </div>

                                <!-- ========== ACTION BUTTONS ========== -->
                                <div class="flex flex-wrap gap-2 sm:gap-3 mt-4 sm:mt-6 justify-center md:justify-start">
                                    <!-- Edit Profile Button -->
                                    <button v-if="!editProfile && user_info.user.id === auth.user.id"
                                        @click="editUserProfile"
                                        class="px-4 py-1.5 sm:px-6 sm:py-2 bg-white dark:bg-gray-700 border-2 border-[var(--theme-color)] text-[var(--theme-color)] dark:text-white rounded-full font-medium hover:bg-[var(--theme-color)] hover:text-white dark:hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-1 sm:gap-2 text-sm sm:text-base">
                                        <i class="pi pi-pencil text-sm sm:text-base"></i>
                                        Edit Profile
                                    </button>

                                    <!-- Save Changes Button -->
                                    <button v-if="editProfile && user_info.user.id === auth.user.id"
                                        @click="saveProfileChanges"
                                        class="px-4 py-1.5 sm:px-6 sm:py-2 bg-[var(--theme-color)] text-white rounded-full font-medium hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-1 sm:gap-2 text-sm sm:text-base">
                                        <i class="pi pi-save text-sm sm:text-base"></i>
                                        Save Changes
                                    </button>

                                    <!-- Share Profile Button -->
                                    <button @click="share"
                                        class="px-4 py-1.5 sm:px-6 sm:py-2 bg-white dark:bg-gray-700 border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 rounded-full font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-1 sm:gap-2 text-sm sm:text-base">
                                        <i class="pi pi-share-alt text-sm sm:text-base"></i>
                                        Share
                                    </button>

                                    <!-- Share Popover -->
                                    <div class="card flex justify-center">
                                        <Popover ref="op">
                                            <div class="flex flex-col gap-4 w-[20rem] sm:w-[25rem]">
                                                <!-- Copy Link Section -->
                                                <div>
                                                    <span class="font-medium block mb-2 text-sm sm:text-base">Share this
                                                        profile</span>
                                                    <InputGroup>
                                                        <InputText :value="profileUrl" readonly
                                                            class="w-[20rem] sm:w-[25rem] text-sm sm:text-base" />
                                                        <InputGroupAddon class="cursor-pointer" @click="copyUrl()">
                                                            <i class="pi pi-copy text-sm sm:text-base" />
                                                        </InputGroupAddon>
                                                    </InputGroup>
                                                </div>

                                                <!-- Social Share Buttons -->
                                                <div>
                                                    <span class="font-medium block mb-2 text-sm sm:text-base">Share
                                                        on</span>
                                                    <ul class="list-none p-0 m-0 flex flex-col gap-3">
                                                        <li v-for="site in shares" :key="site.name"
                                                            class="flex items-center gap-3 hover:bg-gray-100 dark:hover:bg-gray-800 rounded px-2 py-1 cursor-pointer"
                                                            @click="shareOnSocial(site.name.toLowerCase())">
                                                            <i :class="site.icon" :style="{ color: site.color }"
                                                                class="text-lg sm:text-xl w-6 text-center" />
                                                            <span class="font-medium text-xs sm:text-sm">{{ site.name
                                                                }}</span>
                                                        </li>
                                                    </ul>
                                                </div>
                                            </div>
                                        </Popover>
                                    </div>

                                    <!-- Theme Picker Button -->
                                    <div class="relative group">
                                        <button
                                            class="px-4 py-1.5 sm:px-6 sm:py-2 bg-[var(--theme-color)] border-2 border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-200 rounded-full font-medium hover:bg-gray-50 dark:hover:bg-gray-600 transition-all transform hover:scale-105 active:scale-95 shadow-sm flex items-center gap-1 sm:gap-2 text-sm sm:text-base">
                                            <i class="pi pi-palette text-sm sm:text-base"></i>
                                            Theme
                                        </button>
                                    </div>
                                </div>
                            </div>
                        </div>

                        <!-- ========== SETTINGS PANEL ========== -->
                        <div v-if="user_info.user.id === auth.user.id"
                            class="lg:w-80 bg-gray-50/70 dark:bg-gray-800/30 backdrop-blur-sm rounded-xl p-4 sm:p-6 shadow-inner border border-gray-200 dark:border-gray-800/50 mt-6 lg:mt-0">
                            <h2
                                class="text-lg sm:text-xl font-semibold text-gray-800 dark:text-white mb-4 sm:mb-6 flex items-center gap-2">
                                <i class="pi pi-cog text-[var(--theme-color)] text-sm sm:text-base"></i>
                                Account Settings
                            </h2>

                            <div class="space-y-6 gap-1 flex flex-col">
                                <!-- Change Password -->
                                <button @click="changePassword"
                                    class="w-full flex items-center gap-2 sm:gap-3 px-3 py-2 sm:px-4 sm:py-3 rounded-lg border border-gray-200 dark:border-gray-600/50 bg-white dark:bg-gray-700/50 text-gray-700 dark:text-gray-200 font-medium hover:bg-gray-50 dark:hover:bg-gray-600 hover:border-[var(--theme-color)] hover:text-[var(--theme-color)] transition-all text-sm sm:text-base">
                                    <i class="pi pi-lock text-sm sm:text-base"></i>
                                    Change Password
                                </button>

                                <!-- Notification Settings -->
                                <button @click="openNotificationSettings"
                                    class="w-full flex items-center gap-2 sm:gap-3 px-3 py-2 sm:px-4 sm:py-3 rounded-lg border border-gray-200 dark:border-gray-600/50 bg-white dark:bg-gray-700/50 text-gray-700 dark:text-gray-200 font-medium hover:bg-gray-50 dark:hover:bg-gray-600 hover:border-[var(--theme-color)] hover:text-[var(--theme-color)] transition-all text-sm sm:text-base">
                                    <i class="pi pi-bell text-sm sm:text-base"></i>
                                    Notifications
                                </button>

                                <!-- Request Chef Role -->
                                <button v-if="!user_info.user.is_chef" @click="requestChefRole(user_info.user)"
                                    class="w-full flex items-center gap-2 sm:gap-3 px-3 py-2 sm:px-4 sm:py-3 rounded-lg border border-[var(--theme-color)]/50 bg-[var(--theme-color)]/5 text-[var(--theme-color)] font-medium hover:bg-[var(--theme-color)]/10 transition-all group text-sm sm:text-base">
                                    <i class="pi pi-user-plus text-sm sm:text-base"></i>
                                    <span>Request Chef Access</span>
                                    <span
                                        class="ml-auto text-xs bg-[var(--theme-color)] text-white px-2 py-0.5 sm:px-2 sm:py-1 rounded-full group-hover:bg-[var(--theme-color)]/90">Pro</span>
                                </button>

                                <!-- Verify Account -->
                                <button v-if="!user_info.user.is_verified" @click="startVerification"
                                    class="w-full flex items-center gap-2 sm:gap-3 px-3 py-2 sm:px-4 sm:py-3 rounded-lg border border-[var(--theme-color)]/50 bg-[var(--theme-color)]/5 text-[var(--theme-color)] font-medium hover:bg-[var(--theme-color)]/10 transition-all text-sm sm:text-base">
                                    <i class="pi pi-check-circle text-sm sm:text-base"></i>
                                    Verify Account
                                </button>

                                <!-- Divider -->
                                <div class="border-t border-gray-200 dark:border-gray-600 my-1 sm:my-3"></div>

                                <!-- Logout Button -->
                                <button @click="signOut"
                                    class="w-full flex items-center gap-2 sm:gap-3 px-3 py-2 sm:px-4 sm:py-3 rounded-lg border border-red-200 dark:border-red-800 bg-red-50 dark:bg-red-900/30 text-red-600 dark:text-red-400 font-medium hover:bg-red-100 dark:hover:bg-red-900/50 transition-all text-sm sm:text-base">
                                    <i class="pi pi-sign-out text-sm sm:text-base"></i>
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

                <!-- Enhanced Recipe Tabs with Smooth Transitions -->
                <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 border-b border-gray-200 dark:border-gray-700">
                    <div class="flex overflow-x-auto scrollbar-hide">
                        <button @click="activeTab = 'myRecipes'" :class="{
                            'text-[var(--theme-color)] dark:text-[var(--theme-color)] font-semibold': activeTab === 'myRecipes',
                            'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300': activeTab !== 'myRecipes'
                        }"
                            class="whitespace-nowrap py-4 px-6 font-medium text-sm transition-all duration-300 relative group flex flex-col items-center">
                            <span v-if="user_info.user.id === auth.user.id">My Recipes ({{
                                user_info.userMetadata.recipes_count }})</span>
                            <span v-else>Posted Recipes ({{ user_info.userMetadata.recipes_count }})</span>
                            <span :class="activeTab === 'myRecipes' ? 'w-full scale-100' : 'w-0 scale-0'"
                                class="absolute bottom-0 h-0.5 bg-[var(--theme-color)] rounded-full transition-all duration-300 origin-center"></span>
                        </button>

                        <button v-if="user_info.user.id === auth.user.id" @click="activeTab = 'saved'" :class="{
                            'text-[var(--theme-color)] dark:text-[var(--theme-color)] font-semibold': activeTab === 'saved',
                            'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300': activeTab !== 'saved'
                        }"
                            class="whitespace-nowrap py-4 px-6 font-medium text-sm transition-all duration-300 relative group flex flex-col items-center">
                            Saved Recipes
                            <span :class="activeTab === 'saved' ? 'w-full scale-100' : 'w-0 scale-0'"
                                class="absolute bottom-0 h-0.5 bg-[var(--theme-color)] rounded-full transition-all duration-300 origin-center"></span>
                        </button>

                        <button @click="activeTab = 'cooking-tips'" :class="{
                            'text-[var(--theme-color)] dark:text-[var(--theme-color)] font-semibold': activeTab === 'cooking-tips',
                            'text-gray-500 dark:text-gray-400 hover:text-gray-700 dark:hover:text-gray-300': activeTab !== 'cooking-tips'
                        }"
                            class="whitespace-nowrap py-4 px-6 font-medium text-sm transition-all duration-300 relative group flex flex-col items-center">
                            <span v-if="user_info.user.id === auth.user.id">My Cooking Tips</span>
                            <span v-else>Posted Cooking Tips</span>
                            <span :class="activeTab === 'cooking-tips' ? 'w-full scale-100' : 'w-0 scale-0'"
                                class="absolute bottom-0 h-0.5 bg-[var(--theme-color)] rounded-full transition-all duration-300 origin-center"></span>
                        </button>
                    </div>
                </div>

                <div class="relative" v-if="!profile_loading">
                    <!-- My Recipes Tab -->
                    <transition enter-active-class="transition-opacity duration-300 ease-out"
                        enter-from-class="opacity-0" enter-to-class="opacity-100"
                        leave-active-class="transition-opacity duration-200 ease-in" leave-from-class="opacity-100"
                        leave-to-class="opacity-0">
                        <div v-show="activeTab === 'myRecipes'" class="py-4 md:px-2 lg:px-5">
                            <MainRecipeCardsParent v-if="activeTab === 'myRecipes' && user_info.user.id"
                                :user_id="user_info.user.id" :public_only="true" @recipes_count="update_fetched_user_recipes" />

                            <!-- Empty State for Posted Recipes -->
                            <div v-if="totalPostedRecipes < 1" class="text-center py-12">
                                <router-link v-if="user_info.user.isChef && user_info.user.id === auth.user.id"
                                    to="/recipes/new/cover"
                                    class="inline-flex items-center px-6 py-2.5 border border-transparent rounded-full shadow-sm text-white bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 font-medium">
                                    Create Your First Recipe
                                    <i class="pi pi-arrow-right ml-2"></i>
                                </router-link>
                                <router-link to="/recipes"
                                    class="inline-flex items-center px-6 py-2.5 border border-transparent rounded-full shadow-sm text-white bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 font-medium">
                                    Discover recipes
                                    <i class="pi pi-arrow-right ml-2"></i>
                                </router-link>
                            </div>
                        </div>
                    </transition>

                    <!-- Saved Recipes Tab -->
                    <transition enter-active-class="transition-opacity duration-300 ease-out"
                        enter-from-class="opacity-0" enter-to-class="opacity-100"
                        leave-active-class="transition-opacity duration-200 ease-in" leave-from-class="opacity-100"
                        leave-to-class="opacity-0">
                        <div v-show="activeTab === 'saved' && user_info.user.id === auth.user.id"
                            class="py-4 md:px-2 lg:px-5">
                            <MainRecipeCardsParent v-if="activeTab === 'saved' && user_info.user.id"
                                :user_id="user_info.user.id" :saved="true"
                                @recipes_count="update_fetched_user_recipes" />

                            <!-- Empty State for Saved Recipes -->
                            <div v-if="totalSavedRecipes < 1" class="text-center py-12">
                                <div
                                    class="mx-auto w-40 h-40 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden mb-6 relative flex items-center justify-center">
                                    <i class="pi pi-bookmark text-6xl text-gray-400 dark:text-gray-500"></i>
                                    <div
                                        class="absolute inset-0 bg-gradient-to-br from-[var(--theme-color)]/10 to-transparent">
                                    </div>
                                </div>
                                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">
                                    No saved recipes yet
                                </h3>
                                <p class="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">
                                    Save your favorite recipes to find them easily later
                                </p>
                                <router-link to="/recipes"
                                    class="inline-flex items-center px-6 py-2.5 border border-transparent rounded-full shadow-sm text-white bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 font-medium">
                                    Browse Recipes
                                    <i class="pi pi-arrow-right ml-2"></i>
                                </router-link>
                            </div>
                        </div>
                    </transition>
                    <transition enter-active-class="transition-opacity duration-300 ease-out"
                        enter-from-class="opacity-0" enter-to-class="opacity-100"
                        leave-active-class="transition-opacity duration-200 ease-in" leave-from-class="opacity-100"
                        leave-to-class="opacity-0">
                        <div v-show="activeTab === 'cooking-tips'" class="py-4 md:px-2 lg:px-5">


                            <!-- Empty State for Saved Recipes -->
                            <div class="text-center py-12">
                                <div
                                    class="mx-auto w-40 h-40 bg-gray-100 dark:bg-gray-700 rounded-full overflow-hidden mb-6 relative flex items-center justify-center">
                                    <i class="pi pi-bookmark text-6xl text-gray-400 dark:text-gray-500"></i>
                                    <div
                                        class="absolute inset-0 bg-gradient-to-br from-[var(--theme-color)]/10 to-transparent">
                                    </div>
                                </div>
                                <h3 class="text-xl font-bold text-gray-900 dark:text-white mb-3">
                                    No cooking tipss yet
                                </h3>
                                <p class="text-gray-500 dark:text-gray-400 mb-6 max-w-md mx-auto">
                                </p>
                                <router-link to="/cooking-tips"
                                    class="inline-flex items-center px-6 py-2.5 border border-transparent rounded-full shadow-sm text-white bg-[var(--theme-color)] hover:bg-[var(--theme-color)]/90 transition-all transform hover:scale-105 font-medium">
                                    Browse Cooking Tips
                                    <i class="pi pi-arrow-right ml-2"></i>
                                </router-link>
                            </div>
                        </div>
                    </transition>
                </div>



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
import { onMounted, ref, watch, computed, onBeforeUnmount } from 'vue';
import EditProfileCard from '../cards/EditProfile.vue';
import { fetchFollowers, fetchFollowing, folow_unfollow, make_a_post } from '../apis';
import { useAuthStore } from '../store/user';
import { formatDate } from '../reusables/index.js';
import { useToast } from 'primevue/usetoast'
import { useSiteStore } from '../config/siteConfig.js';
import { Cropper } from 'vue-advanced-cropper';
import MainRecipeCardsParent from "../cards/ManyReipesParent.vue"
import { useControl } from "../store/control.js";
import { initializeSession } from './apis/auth.js'

const control = useControl()
import 'vue-advanced-cropper/dist/style.css';
import router from '../router/index.js';
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

const topElementRef = ref(null)
const topHeight = ref(0)

const refreshToken = async () => {
  try {
    const res = await initializeSession(auth.token, auth.user.id)
    if (res?.success && res.data) {
      auth.setUser(res.data.user)
      auth.setToken({
        token: res.data.access_token,
        expires_in: res.data.expires_in
      })
      return true
    }
    return false
  } catch (error) {
    console.error('Token refresh error:', error)
    return false
  }
}

let observer

onMounted( async() => {
    await refreshToken()

    if (topElementRef.value) {
        topHeight.value = topElementRef.value.offsetHeight

        // Watch for changes using ResizeObserver
        observer = new ResizeObserver(entries => {
            for (const entry of entries) {
                topHeight.value = entry.contentRect.height
            }
        })

        observer.observe(topElementRef.value)
    }
    await load_user()
})

onBeforeUnmount(() => {
    if (observer && topElementRef.value) {
        observer.unobserve(topElementRef.value)
    }
})

const changeThemeColor = (color) => {
    user_info.value.user.theme = color.value;
    showColorPicker.value = false;
    // Save to backend in real implementation
};

const editUserProfile = () => {
    editProfile.value = true;
    console.log('Edit profile clicked');
};

const totalPostedRecipes = ref(0);
const totalSavedRecipes = ref(0);

const update_fetched_user_recipes = (count) => {
    if (activeTab.value === 'myRecipes') {
        totalPostedRecipes.value = count;
    } else if (activeTab.value === 'saved') {
        totalSavedRecipes.value = count;
    }
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



const follwrs = ref();
const followers = ref([

]);

const loading_followers = ref(false)
const toggle_followers = (event) => {
    follwrs.value.toggle(event);
    fetch_followers()
}

const followers_limit = ref(10)
const followers_offset = ref(0)
const fetch_followers = async (limit = 10, offset = 0) => {
    loading_followers.value = true
    const res = await fetchFollowers(null, {
        target_id: user_info.value.user.id,
        user_id: auth.user?.id,
        limit: limit,
        offset: offset
    })
    if (res.data) {
        followers.value = res.data.followers
        followers_limit.value = res.data.limit
        followers_offset.value = res.data.offset

    }
    loading_followers.value = false
}


const loading_following = ref(false)
const follwng = ref();
const following = ref([

]);
const toggle_followings = (event) => {
    follwng.value.toggle(event);
    fetch_following()
}

const following_limit = ref(10)
const following_offset = ref(0)
const fetch_following = async (limit = 10, offset = 0) => {
    loading_following.value = true
    const res = await fetchFollowing(null, {
        target_id: user_info.value.user.id,
        user_id: auth.user?.id,
        limit: limit,
        offset: offset
    })
    if (res.data) {
        following.value = res.data.following
        following_limit.value = res.data.limit
        following_offset.value = res.data.offset

    }
    loading_following.value = false
}



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
    router.push('/register/recover-password')
};

const openNotificationSettings = () => {
    router.push("/notifications")
    console.log('Notification settings clicked');
};

const requestChefRole = async (user) => {
    const res = await make_a_post(`/users/chef-request/${user.username}`, auth.token, { chef_id: user.id })
    if (res.success) {
        toast.add({
            severity: 'info',
            summary: 'Chef request sent!!',
            detail: 'You\'ll be notified once your requset has been approved!',
            life: 5000,
            group: 'bc'
        })
    }
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

const toggleFollow = async (follow) => {
    try {
        const res = await folow_unfollow(auth.token, follow.id);

        if (!res?.success) {
            toast.add({
                severity: 'error',
                summary: 'Follow Failed',
                detail: res.message || 'Unable to follow the user. Please try again.',
                group: 'bc',
                life: 4000,
            });
            return;
        }

        // Toggle the local follow state for UI consistency
        const newFollowStatus = !follow.isFollowing;

        // Update in followers list
        const followerItem = followers.value?.find(f => f.id === follow.id);
        if (followerItem) followerItem.isFollowing = newFollowStatus;

        // Update in following list (if needed)
        const followingItem = following.value?.find(f => f.id === follow.id);
        if (followingItem) followingItem.isFollowing = newFollowStatus;

        // Notify the user
        toast.add({
            severity: 'info',
            summary: newFollowStatus ? 'Followed' : 'Unfollowed',
            detail: newFollowStatus
                ? `You're now following ${follow.name}`
                : `You have unfollowed ${follow.name}`,
            group: 'bc',
            life: 3000,
        });

    } catch (err) {
        console.error('Follow/Unfollow error:', err);
        toast.add({
            severity: 'error',
            summary: 'Error',
            detail: 'Something went wrong. Please try again.',
            group: 'bc',
            life: 4000,
        });
    }
};

const NowFollowing = ref(false)
const follow = async (chefId) => {
    NowFollowing.value = true
    const res = await folow_unfollow(auth.token, chefId)

    if (!res?.success) {
        toast.add({
            severity: 'error',
            summary: 'Follow Failed',
            detail: res.message || 'Unable to follow the user. Please try again.',
            group: 'bc',
            life: 4000
        })
        NowFollowing.value = false

        return
    }
    user_info.value.userMetadata.isFollowing = !user_info.value.userMetadata.isFollowing

    toast.add({
        severity: res?.success ? 'info' : 'error',
        summary: res?.success && user_info.value.userMetadata.isFollowing ? 'Followed' : 'Unfollowed',
        detail: res?.success && user_info.value.userMetadata.isFollowing ? `You're now following ${user_info.value.user?.username}` : `You have unfollowed ${user_info.value.user?.username}` || 'Unable to follow the user. Please try again.',
        group: 'bc',
        life: 3000
    })

    NowFollowing.value = false
}





watch(() => props.username, (newVal) => {
    if (newVal) {
        load_user();
        activeTab.value = "myRecipes"
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
.b_content {}

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