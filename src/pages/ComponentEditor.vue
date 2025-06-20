<template>
  <div class="space-y-4">
    <!-- Icon Display -->
    <div v-if="isIcon" class="flex flex-col gap-2">
      <label class="font-medium text-gray-700">{{ displayKeyName }}</label>
      <div class="flex items-center gap-4">
        <i :class="localValue" class="text-2xl text-purple-600" />
        <InputText v-model="localValue" placeholder="fas fa-star" class="w-full" />
      </div>
    </div>

        <!-- SIMPLE FILE PREVIEW (image or video) -->
    <div v-else-if="inputType === 'file'" class="space-y-1">
      <label class="block text-sm font-medium text-gray-700">{{ displayKeyName }}</label>
      <div v-if="isImage(localValue)" class="preview-box">
        <img :src="localValue" class="preview-img" />
      </div>
      <div v-else-if="isVideo(localValue)" class="preview-box">
        <video :src="localValue" class="preview-img" controls />
      </div>
      <input type="file" @change="handleFileChange" :accept="fileAccept" class="input" />
    </div>
    <!-- OBJECT WITH IMAGE/VIDEO KEYS -->
    <div v-else-if="inputType === 'object'" class="nested space-y-2">
      <h4 class="font-bold  text-gray-500 decoration-1 underline flex items-center gap-2">
        <i v-if="fieldIcon" :class="fieldIcon" class="text-gray-500"></i>
        {{ displayKeyName }}
      </h4>
      <div class="pl-2">
        <ConfigEditor
          v-for="(v, k) in localValue"
          :key="k"
          :keyName="k"
          :value="v"
          @update:modelValue="nv => updateNestedValue(k, nv)"
        />
      </div>
    </div>

      <div v-else-if="inputType === 'object' && isImageObject(localValue)" class="nested space-y-2">
    <h4 class="font-bold text-gray-500 decoration-1 underline flex items-center gap-2">
      <i v-if="fieldIcon" :class="fieldIcon" class="text-gray-500"></i>
      {{ displayKeyName }}
    </h4>
    <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">Desktop Image</label>
        <InputText v-model="localValue.desktop" class="w-full" />
        <div v-if="isImage(localValue.desktop)" class="preview-box mt-2">
          <img :src="localValue.desktop" class="preview-img" />
        </div>
      </div>
      <div class="space-y-2">
        <label class="block text-sm font-medium text-gray-700">Mobile Image</label>
        <InputText v-model="localValue.mobile" class="w-full" />
        <div v-if="isImage(localValue.mobile)" class="preview-box mt-2">
          <img :src="localValue.mobile" class="preview-img" />
        </div>
      </div>
    </div>
  </div>

    <!-- Simple Inputs -->
    <div v-else-if="inputType !== 'object' && inputType !== 'array' && inputType !== 'null'">
      <label class="font-medium text-gray-700 flex items-center gap-2">
        <i v-if="fieldIcon" :class="fieldIcon" class="text-gray-500" />
        {{ displayKeyName }}
      </label>

      <InputText v-if="inputType === 'text'" v-model="localValue" class="w-full" />
      <input v-else-if="inputType === 'color'" type="color" v-model="localValue" class="input-color" />
      <InputNumber v-else-if="inputType === 'number'" v-model="localValue" class="w-full" />
      <div v-else-if="inputType === 'boolean'" class="flex items-center gap-2">
        <Checkbox v-model="localValue" :binary="true" />
        {{ localValue ? 'Enabled' : 'Disabled' }}
      </div>
      <Textarea v-else-if="inputType === 'textarea'" v-model="localValue" class="w-full" rows="3" />
    </div>

    <!-- File Inputs (Image or Video) -->
    <div v-else-if="inputType === 'file'" class="space-y-2">
      <label class="font-medium text-gray-700 flex items-center gap-2">
        <i v-if="fieldIcon" :class="fieldIcon" class="text-gray-500" />
        {{ displayKeyName }}
      </label>
      <input type="file" @change="handleFileChange" :accept="fileAccept" class="input" />

      <div v-if="localValue" class="preview-area mt-2">
        <Image v-if="isImage(localValue)" :src="localValue" alt="Preview" imageClass="w-48 border rounded-md" preview />
        <div v-else-if="isVideo(localValue)">
          <video :src="localValue" class="rounded-md border max-w-full" controls />
        </div>
        <Button icon="pi pi-times" severity="danger" text size="small" @click="clearFile" label="Remove" class="mt-2" />
      </div>
    </div>

    <!-- Array Inputs -->
    <div v-else-if="inputType === 'array'" class="space-y-2">
      <h4 class="font-bold flex text-gray-500 decoration-1 underline items-center gap-2">
        <i v-if="fieldIcon" :class="fieldIcon" class="text-gray-500" />
        {{ displayKeyName }}
      </h4>
      <div v-for="(item, index) in localValue" :key="index" class="nested">
        <ConfigEditor v-for="(v, k) in item" :key="k" :keyName="k" :value="v" @update:modelValue="nv => updateArrayItem(index, k, nv)" />
      </div>
      <Button icon="pi pi-plus" label="Add Item" text @click="addArrayItem" />
    </div>

    <!-- Object Inputs -->
    <div v-else-if="inputType === 'object'">
      <h4 class="font-bold  text-gray-500 decoration-1 underline flex items-center gap-2">
        <i v-if="fieldIcon" :class="fieldIcon" class="text-gray-500" />
        {{ displayKeyName }}
      </h4>
      <div class="nested">
        <ConfigEditor v-for="(v, k) in localValue" :key="k" :keyName="k" :value="v" @update:modelValue="nv => updateNestedValue(k, nv)" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from 'vue'
import ConfigEditor from './ComponentEditor.vue'

// PrimeVue components
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'
import Image from 'primevue/image'
import Button from 'primevue/button'

const props = defineProps({ keyName: [String, Number], value: [String, Number, Boolean, Array, Object] })
const emit = defineEmits(['update:modelValue'])
const localValue = ref(props.value)

const displayKeyName = computed(() => {
  const raw = String(props.keyName ?? '')
  return raw.replace(/([A-Z])/g, ' $1').replace(/^./, str => str.toUpperCase())
})


const isImageObject = (obj) => {
  return obj && typeof obj === 'object' && 
         'desktop' in obj && 'mobile' in obj &&
         typeof obj.desktop === 'string' && 
         typeof obj.mobile === 'string';
};

const fieldIcon = computed(() => {
  const key = String(props.keyName ?? '').toLowerCase()
  if (key.includes('icon')) return 'fas fa-icons'
  if (key.includes('image')) return 'fas fa-image'
  if (key.includes('video')) return 'fas fa-video'
  if (key.includes('logo')) return 'fas fa-apple-alt'
  if (key.includes('note')) return 'fas fa-sticky-note'
  if (key.includes('title')) return 'fas fa-heading'
  if (key.includes('description')) return 'fas fa-align-left'
  return null
})

const isIcon = computed(() => {
  const key = String(props.keyName ?? '').toLowerCase()
  const val = localValue.value
  return key.includes('icon') && typeof val === 'string' && val.startsWith('fa')
})

const inputType = computed(() => {
  if (isIcon.value) return 'icon'
  if (typeof props.value === 'boolean') return 'boolean'
  if (typeof props.value === 'number') return 'number'

  if (typeof props.value === 'string') {
    const val = props.value.trim().toLowerCase()

    // Check for color
    const isHex = val.startsWith('#') && /^#[0-9a-f]{3,8}$/i.test(val)
    const isRgb = val.startsWith('rgb') && /^rgb(a)?\((\s*\d+\s*,){2,3}\s*\d+\s*\)$/i.test(val)

    if (isHex || isRgb) return 'color'

    // Handle Data URIs (image or video)
    if (/^data:(image|video)\//.test(val)) return 'file'

    // Image extensions
    if (/\.(jpg|jpeg|png|svg|gif|webp)$/i.test(val)) return 'file'

    // Video extensions
    if (/\.(mp4|webm|ogg)$/i.test(val)) return 'file'

    // Long text
    if (val.length > 80) return 'textarea'

    // Default fallback
    return 'text'
  }

  if (Array.isArray(props.value)) return 'array'
  if (props.value && typeof props.value === 'object') return 'object'
  return 'null'
})


const fileAccept = computed(() => /video/i.test(props.keyName) ? 'video/*' : 'image/*')
const isImage = val => typeof val === 'string' && /\.(jpg|jpeg|png|svg|gif|webp)$/i.test(val)
const isVideo = val => typeof val === 'string' && /\.(mp4|webm|ogg)$/i.test(val)

const updateNestedValue = (key, newVal) => {
  localValue.value[key] = newVal
  emit('update:modelValue', localValue.value)
}
const updateArrayItem = (index, key, newVal) => {
  localValue.value[index][key] = newVal
  emit('update:modelValue', localValue.value)
}
const addArrayItem = () => localValue.value.push({})

const handleFileChange = (e) => {
  const file = e.target.files[0]
  if (file) {
    const reader = new FileReader()
    reader.onload = () => {
      localValue.value = reader.result
      emit('update:modelValue', reader.result)
    }
    reader.readAsDataURL(file)
  }
}
const clearFile = () => {
  localValue.value = ''
  emit('update:modelValue', '')
}

watch(() => props.value, nv => { localValue.value = nv }, { deep: true })
watch(localValue, nv => emit('update:modelValue', nv), { deep: true })
</script>

<style scoped>
.input-color {
  width: 3rem;
  height: 2rem;
  padding: 0.25rem;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  cursor: pointer;
}
.nested {
  padding-left: 1rem;
  border-left: 2px solid #ccc;
  margin-bottom: 1rem;
}
</style>


<style scoped>
.input {
  width: 100%;
  padding: 0.5rem;
  color: #746d6d !important;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  background-color: white;
}
.input:focus {
  outline: none;
  border-color: #6366f1;
  box-shadow: 0 0 0 1px #6366f1;
}
.input-color {
  width: 3rem;
  height: 2rem;
  padding: 0.25rem;
  border: 1px solid #ccc;
  border-radius: 0.375rem;
  cursor: pointer;
}
.preview-img {
  max-width: 200px;
  max-height: 150px;
  margin-top: 0.5rem;
  border-radius: 0.25rem;
  border: 1px solid #eee;
}
.nested {
  padding-left: 1rem;
  border-left: 2px solid #ccc;
  margin-bottom: 1rem;
}
button {
  transition: all 0.2s ease;
}
button:hover {
  transform: translateY(-1px);
}
</style>
