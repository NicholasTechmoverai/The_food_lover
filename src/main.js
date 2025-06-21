import { createApp } from 'vue';
import App from './App.vue';
import router from './router'

import PrimeVue from 'primevue/config';
import ToastService from 'primevue/toastservice';
import Aura from '@primeuix/themes/aura';
import Splitter from 'primevue/splitter';
import SplitterPanel from 'primevue/splitterpanel';
import Button from 'primevue/button'
import Panel from 'primevue/panel'
import MegaMenu from 'primevue/megamenu'
import Avatar from 'primevue/avatar';
import TieredMenu from 'primevue/tieredmenu';
import InputText from 'primevue/inputtext'
import Textarea from 'primevue/textarea'
import InputNumber from 'primevue/inputnumber'
import Checkbox from 'primevue/checkbox'
import Image from 'primevue/image'
import Stepper from 'primevue/stepper';
import StepList from 'primevue/steplist';
import StepPanels from 'primevue/steppanels';
import StepItem from 'primevue/stepitem';
import Step from 'primevue/step';
import StepPanel from 'primevue/steppanel';
import Popover from 'primevue/popover';
import Skeleton from 'primevue/skeleton';
import Toast from 'primevue/toast';
import AnimateOnScroll from 'primevue/animateonscroll';

import '@fortawesome/fontawesome-free/css/all.min.css';
import 'primeicons/primeicons.css';

import '@fontsource/inter/400.css'; // Regular
import '@fontsource/inter/700.css'; // Bold
import '@fontsource/inter/900.css'; // Black

import './style.css';

const app = createApp(App);
app.component('Button', Button)
app.component('Panel', Panel)
app.component('Splitter', Splitter);
app.component('SplitterPanel', SplitterPanel);
app.component('MegaMenu', MegaMenu)
app.component('Avatar', Avatar)
app.component('TieredMenu', TieredMenu);
app.component('Stepper', Stepper);
app.component('StepList', StepList);
app.component('StepPanels', StepPanels);
app.component('StepItem', StepItem);
app.component('Step', Step);
app.component('StepPanel', StepPanel);
app.component('InputNumber',InputNumber)
app.component('Image',Image)
app.component('Textarea',Textarea)
app.component('Checkbox',Checkbox)
app.component('InputText',InputText)
app.component('Popover',Popover)
app.component('Skeleton',Skeleton)
app.component('Toast',Toast)
app.component('AnimateOnScroll',AnimateOnScroll)
app.directive('animateonscroll', AnimateOnScroll);


app.use(router)
app.use(ToastService);
app.use(PrimeVue, {
    // unstyled: true,
    // Default theme configuration
    theme: {
        preset: Aura,
        options: {
            prefix: 'p',
            darkModeSelector: 'system',
            cssLayer: false
        }
    }
 });
app.mount('#app');
