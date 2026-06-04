import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createTestPinia } from '../test/helpers/pinia'

vi.mock('../assets/logo.png', () => ({ default: 'logo.png' }))
vi.mock('../assets/logo.ico', () => ({ default: 'logo.ico' }))
vi.mock('../assets/blob-scene-landscape.svg', () => ({ default: 'desktop.svg' }))
vi.mock('../assets/blob-scene-potrait.svg', () => ({ default: 'mobile.svg' }))
vi.mock('../assets/3196344-uhd_3840_2160_25fps-compress.mp4', () => ({ default: 'welcome.mp4' }))
vi.mock('../assets/kitchen1.jpg', () => ({ default: 'kitchen.jpg' }))
vi.mock('../assets/3255109-uhd_3840_2160_25fps-compress.mp4', () => ({ default: 'design.mp4' }))
vi.mock('../assets/chips1.jpg', () => ({ default: 'chips.jpg' }))

import { useSiteStore } from './siteConfig'

describe('useSiteStore', () => {
  beforeEach(() => {
    createTestPinia()
  })

  it('provides default site configuration', () => {
    const store = useSiteStore()

    expect(store.siteConfig.meta.siteName).toBe('The Food Lovers')
    expect(store.siteConfig.colors.primary).toBe('#800000')
    expect(store.siteConfig.contactInfo.email).toContain('@')
  })

  it('returns desktop values from responsive config', () => {
    const store = useSiteStore()
    const config = { amplitude: { desktop: 10, mobile: 30, ratio: 0.6 } }

    expect(store.getResponsiveValue(config, 'amplitude', false)).toBe(10)
  })

  it('returns explicit mobile values when defined', () => {
    const store = useSiteStore()
    const config = { amplitude: { desktop: 10, mobile: 30, ratio: 0.6 } }

    expect(store.getResponsiveValue(config, 'amplitude', true)).toBe(30)
  })

  it('returns ratio-adjusted values when mobile value is absent', () => {
    const store = useSiteStore()
    const config = { amplitude: { desktop: 10, ratio: 0.6 } }

    expect(store.getResponsiveValue(config, 'amplitude', true)).toBe(6)
  })

  it('updates theme colors with hash prefix normalization', () => {
    const store = useSiteStore()
    const consoleLog = vi.spyOn(console, 'log').mockImplementation(() => {})

    store.adjustThemesColor({
      primary: 'FF0000',
      secondary: '#00FF00',
      text: { primary: '#111111' },
      gradients: { primary: 'linear-gradient(red, blue)' },
    })

    expect(store.siteConfig.colors.primary).toBe('#FF0000')
    expect(store.siteConfig.colors.secondary).toBe('#00FF00')
    expect(store.siteConfig.colors.text.primary).toBe('#111111')
    expect(store.siteConfig.colors.gradients.primary).toBe('linear-gradient(red, blue)')

    consoleLog.mockRestore()
  })
})
