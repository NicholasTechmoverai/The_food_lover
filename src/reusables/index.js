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