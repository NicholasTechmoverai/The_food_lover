import { beforeEach, describe, expect, it, vi } from 'vitest'
import {
  applyTheme,
  copyToClipboard,
  formatCookTime,
  formatDate,
  formattedFromUrl,
  generateUUID,
  polishUrlName,
} from './index'

describe('reusable helpers', () => {
  beforeEach(() => {
    document.documentElement.className = ''
    vi.clearAllMocks()
  })

  describe('copyToClipboard', () => {
    it('returns true on successful copy', async () => {
      navigator.clipboard.writeText.mockResolvedValueOnce(undefined)

      await expect(copyToClipboard('hello')).resolves.toBe(true)
      expect(navigator.clipboard.writeText).toHaveBeenCalledWith('hello')
    })

    it('returns false when clipboard write fails', async () => {
      const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {})
      navigator.clipboard.writeText.mockRejectedValueOnce(new Error('denied'))

      await expect(copyToClipboard('hello')).resolves.toBe(false)
      consoleError.mockRestore()
    })
  })

  describe('applyTheme', () => {
    it('applies dark theme classes', () => {
      applyTheme('dark')

      expect(document.documentElement.classList.contains('dark')).toBe(true)
      expect(document.documentElement.classList.contains('my-app-dark')).toBe(true)
    })

    it('removes dark classes for light theme', () => {
      document.documentElement.classList.add('dark', 'my-app-dark')

      applyTheme('light')

      expect(document.documentElement.classList.contains('dark')).toBe(false)
    })

    it('follows system preference for system theme', () => {
      window.matchMedia.mockReturnValueOnce({
        matches: true,
        addListener: vi.fn(),
        removeListener: vi.fn(),
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
        dispatchEvent: vi.fn(),
      })

      applyTheme('system')

      expect(document.documentElement.classList.contains('dark')).toBe(true)
    })
  })

  describe('generateUUID', () => {
    it('returns a valid v4 UUID format', () => {
      const uuid = generateUUID()

      expect(uuid).toMatch(
        /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/,
      )
    })
  })

  describe('polishUrlName', () => {
    it('slugifies names without id', () => {
      expect(polishUrlName('Beef Stew')).toBe('beef-stew')
    })

    it('appends id when provided', () => {
      expect(polishUrlName('Beef Stew', 'abc-123')).toBe('beef-stew/abc-123')
    })
  })

  describe('formattedFromUrl', () => {
    it('replaces hyphens with spaces', () => {
      expect(formattedFromUrl('beef-stew')).toBe('beef stew')
    })

    it('returns untitled for empty input', () => {
      expect(formattedFromUrl(null)).toBe('Untitled ')
    })
  })

  describe('formatCookTime', () => {
    it('formats hours and minutes', () => {
      expect(formatCookTime({ hr: 1, min: 30 })).toBe('1h 30m')
    })

    it('returns 0m for empty input', () => {
      expect(formatCookTime(null)).toBe('0m')
      expect(formatCookTime({ hr: 0, min: 0 })).toBe('0m')
    })
  })

  describe('formatDate', () => {
    it('formats ISO date strings', () => {
      const formatted = formatDate('2024-06-15')

      expect(formatted).toContain('2024')
      expect(formatted).toContain('June')
    })

    it('returns unknown date for falsy input', () => {
      expect(formatDate(null)).toBe('Unknown date')
    })
  })
})
