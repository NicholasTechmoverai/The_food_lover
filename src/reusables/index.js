import router from '../router';


export const goHome = () => {
  router.push('/')
}

export const copyToClipboard = async (msg) => {
  try {
    await navigator.clipboard.writeText(msg)
    return true
  } catch (err) {
    console.error('Failed to copy OTP: ', err)
    return false
  }
}

export const applyTheme = (theme) => {
  const root = document.documentElement;
  root.classList.remove('dark', 'my-app-dark'); // Clear all first

  if (theme === 'dark') {
    root.classList.add('dark', 'my-app-dark'); // Both for Tailwind + PrimeVue
  } else if (theme === 'light') {
    // Nothing to add
  } else if (theme === 'system') {
    if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
      root.classList.add('dark', 'my-app-dark');
    }
  }
};
