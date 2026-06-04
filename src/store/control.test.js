import { beforeEach, describe, expect, it, vi } from 'vitest'
import { createTestPinia } from '../test/helpers/pinia'

const { mockPush, mockRoute } = vi.hoisted(() => ({
  mockPush: vi.fn(),
  mockRoute: { value: { query: {} } },
}))

vi.mock('../router', () => ({
  default: {
    push: mockPush,
    currentRoute: mockRoute,
  },
}))

import { useControl } from './control'

describe('useControl store', () => {
  beforeEach(() => {
    createTestPinia()
    mockPush.mockClear()
    mockRoute.value = { query: {} }
  })

  it('toggles search visibility and syncs query param', () => {
    const store = useControl()

    store.setShowSearch(true)

    expect(store.showSearch).toBe(true)
    expect(mockPush).toHaveBeenCalledWith({ query: { search: 'true' } })

    store.setShowSearch(false)

    expect(store.showSearch).toBe(false)
    expect(mockPush).toHaveBeenLastCalledWith({ query: {} })
  })

  it('toggles nav visibility and syncs query param', () => {
    const store = useControl()

    store.setShowNav(true)

    expect(store.showNav).toBe(true)
    expect(mockPush).toHaveBeenCalledWith({ query: { search: 'true' } })
  })
})
