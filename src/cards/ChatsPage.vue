<template>
    <div>
        <Card class="mb-4">
            <template #title>
                <div class="flex items-center gap-3">
                    <Avatar image="https://cdn.pixabay.com/photo/2015/10/05/22/37/blank-profile-picture-973460_1280.png"
                        shape="circle" />
                    <div>
                        <p class="text-sm font-semibold">Jane Doe</p>
                        <p class="text-xs text-gray-400">2 hours ago</p>
                    </div>
                </div>
            </template>

            <template #content>
                <p>This is a great recipe! I tried it with coconut milk and it was amazing. 😍</p>
            </template>

            <template #footer>
                <div class="flex gap-4 text-sm text-gray-500">
                    <span class="cursor-pointer hover:text-amber-600"><i class="pi pi-thumbs-up" />
                        Like</span>
                    <span class="cursor-pointer hover:text-amber-600"><i class="pi pi-reply" />
                        Reply</span>
                </div>
            </template>
        </Card>
    </div>
</template>