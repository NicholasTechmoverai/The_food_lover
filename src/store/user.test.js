import { beforeEach, describe, expect, it } from 'vitest'
import { createTestPinia } from '../test/helpers/pinia'
import { useAuthStore, useNotificationStore } from './user'

describe('useAuthStore', () => {
  beforeEach(() => {
    createTestPinia()
  })

  it('starts unauthenticated with null user and token', () => {
    const store = useAuthStore()

    expect(store.isAuthenticated).toBe(false)
    expect(store.user).toBeNull()
    expect(store.token).toBeNull()
  })

  it('sets token and derives authenticated state', () => {
    const store = useAuthStore()

    store.setToken('abc-token')

    expect(store.token).toBe('abc-token')
    expect(store.isAuthenticated).toBe(true)
  })

  it('assigns default profile picture when user has none', () => {
    const store = useAuthStore()

    store.setUser({ id: '1', username: 'chef', email: 'chef@example.com' })

    expect(store.user.profilePic).toContain('flaticon.com')
  })

  it('preserves existing profile picture', () => {
    const store = useAuthStore()
    const pic = 'https://example.com/avatar.png'

    store.setUser({ id: '1', username: 'chef', profilePic: pic })

    expect(store.user.profilePic).toBe(pic)
  })

  it('clears all auth state on logout', () => {
    const store = useAuthStore()
    store.setToken('abc')
    store.setUser({ id: '1' })
    store.setAuthData({ role: 'chef' })

    store.logout()

    expect(store.token).toBeNull()
    expect(store.user).toBeNull()
    expect(store.authData).toBeNull()
    expect(store.isAuthenticated).toBe(false)
  })
})

describe('useNotificationStore', () => {
  beforeEach(() => {
    createTestPinia()
  })

  it('initializes with zero notification counts', () => {
    const store = useNotificationStore()

    expect(store.notificationsCount.all).toBe(0)
    expect(store.liveNotifications).toBeNull()
  })

  it('sets live notifications as a new array', () => {
    const store = useNotificationStore()
    const notifications = [{ id: 'n1' }, { id: 'n2' }]

    store.setLiveNotifications(notifications)

    expect(store.liveNotifications).toEqual(notifications)
    expect(store.liveNotifications).not.toBe(notifications)
  })

  it('ignores null when setting live notifications', () => {
    const store = useNotificationStore()
    store.setLiveNotifications([{ id: 'n1' }])

    store.setLiveNotifications(null)

    expect(store.liveNotifications).toEqual([{ id: 'n1' }])
  })

  it('updates notification counts and clears live notifications', () => {
    const store = useNotificationStore()
    store.setLiveNotifications([{ id: 'n1' }])
    store.setNotificationsCount({ likes: 3, comment: 1, mentions: 0, follows: 2, system: 0, all: 6 })

    expect(store.notificationsCount.all).toBe(6)
    store.clearLiveNotifications()
    expect(store.liveNotifications).toBeNull()
  })
})
