import { beforeEach, describe, expect, it, vi } from 'vitest'
import axios from 'axios'
import {
  Login,
  Signup,
  initializeSession,
  isTokenExpired,
  is_user_exists,
  resetPassword,
  send_verify,
  verifyCodeAPI,
} from './auth'

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    delete: vi.fn(),
  },
}))

const encodeToken = (payload) => {
  const encoded = btoa(JSON.stringify(payload)).replaceAll('=', '')
  return `header.${encoded}.signature`
}

describe('auth API helpers', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('detects valid, expired, and malformed JWT expiry values', () => {
    const consoleError = vi.spyOn(console, 'error').mockImplementation(() => {})

    expect(isTokenExpired(encodeToken({ exp: Math.floor(Date.now() / 1000) + 60 }))).toBe(false)
    expect(isTokenExpired(encodeToken({ exp: Math.floor(Date.now() / 1000) - 60 }))).toBe(true)
    expect(isTokenExpired('not-a-token')).toBe(true)
    expect(consoleError).toHaveBeenCalled()

    consoleError.mockRestore()
  })

  it('returns existing session token without refreshing when it is still valid', async () => {
    const token = { token: 'access', expires_in: encodeToken({ exp: Math.floor(Date.now() / 1000) + 60 }) }

    await expect(initializeSession(token, 'user-1')).resolves.toBe(token)
    expect(axios.post).not.toHaveBeenCalled()
  })

  it('refreshes expired tokens and sends bearer authorization', async () => {
    axios.post.mockResolvedValueOnce({ status: 200, data: { access_token: 'fresh' } })

    const result = await initializeSession(
      { token: 'old', expires_in: encodeToken({ exp: Math.floor(Date.now() / 1000) - 60 }) },
      'user-1',
    )

    expect(result).toEqual({ success: true, data: { access_token: 'fresh' } })
    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/auth/refresh'),
      { user_id: 'user-1' },
      expect.objectContaining({ headers: expect.objectContaining({ Authorization: 'Bearer old' }) }),
    )
  })

  it('wraps login and signup success and validation failures', async () => {
    axios.post
      .mockResolvedValueOnce({ status: 200, data: { access_token: 'token' } })
      .mockResolvedValueOnce({ status: 201, data: { id: 'verification' } })

    await expect(Login({ email: 'chef@example.com', password: 'secret' })).resolves.toEqual({
      success: true,
      data: { access_token: 'token' },
    })
    await expect(Signup({ email: 'new@example.com', password: 'secret' })).resolves.toEqual({
      success: true,
      data: { id: 'verification' },
    })
    await expect(Login(null)).resolves.toEqual({ success: false, message: 'Invalid login data provided.' })
    await expect(Signup(null)).resolves.toEqual({ success: false, message: 'Invalid signup data provided.' })
  })

  it('passes verification and reset-password query parameters', async () => {
    axios.post
      .mockResolvedValueOnce({ status: 200, data: { verified: true } })
      .mockResolvedValueOnce({ status: 200, data: { sent: true } })
      .mockResolvedValueOnce({ status: 200, data: true })
      .mockResolvedValueOnce({ status: 200, data: { reset: true } })

    await expect(verifyCodeAPI('code-1', '123456', 'email')).resolves.toMatchObject({ success: true })
    await expect(send_verify('code-1', 'link', 'email', 'user-1', 'new@example.com')).resolves.toMatchObject({ success: true })
    await expect(is_user_exists('chef@example.com')).resolves.toMatchObject({ success: true })
    await expect(resetPassword({ verifier: 'chef@example.com', password: 'secret1', confirmPassword: 'secret1' })).resolves.toMatchObject({ success: true })

    expect(axios.post).toHaveBeenNthCalledWith(1, expect.stringContaining('/auth/verify'), null, {
      params: { code_id: 'code-1', code: '123456', type: 'email' },
    })
    expect(axios.post).toHaveBeenNthCalledWith(4, expect.stringContaining('/auth/reset-password'), null, {
      params: { verifier: 'chef@example.com', password: 'secret1', confirmPassword: 'secret1' },
    })
  })

  it('returns failure when token refresh fails', async () => {
    axios.post.mockRejectedValueOnce(new Error('Network error'))

    const result = await initializeSession(
      { token: 'old', expires_in: encodeToken({ exp: Math.floor(Date.now() / 1000) - 60 }) },
      'user-1',
    )

    expect(result).toEqual({ success: false })
  })

  it('returns null when session inputs are missing', async () => {
    await expect(initializeSession(null, 'user-1')).resolves.toBeNull()
    await expect(initializeSession({ token: 'abc' }, null)).resolves.toBeNull()
  })

  it('normalizes backend error details', async () => {
    axios.post.mockRejectedValueOnce({ response: { data: { detail: 'Bad credentials' } } })

    await expect(Login({ email: 'chef@example.com', password: 'wrong' })).resolves.toEqual({
      success: false,
      message: 'Bad credentials',
      data: { detail: 'Bad credentials' },
    })
  })
})
