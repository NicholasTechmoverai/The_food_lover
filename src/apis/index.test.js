import { beforeEach, describe, expect, it, vi } from 'vitest'
import axios from 'axios'
import {
  fetchComments,
  fetchFollowers,
  fetchFollowing,
  fetchLikes,
  fetch_cooking_tips,
  folow_unfollow,
  like_unlike,
  make_a_delete,
  make_a_post,
  save_unsave_favourites,
} from './index'

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    delete: vi.fn(),
  },
}))

describe('generic API helpers', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches metadata collections with auth headers and query params', async () => {
    axios.get.mockResolvedValueOnce({ status: 200, data: { followers: [] } })

    const result = await fetchFollowers({ token: 'abc' }, { target_id: 'chef-1' })

    expect(result).toEqual({ success: true, data: { followers: [] } })
    expect(axios.get).toHaveBeenCalledWith(
      expect.stringContaining('/users/followers'),
      { headers: { Authorization: 'Bearer abc' }, params: { target_id: 'chef-1' } },
    )
  })

  it('fetches following, comments, likes, and cooking tips', async () => {
    axios.get
      .mockResolvedValueOnce({ status: 200, data: { following: [] } })
      .mockResolvedValueOnce({ status: 200, data: { comments: [] } })
      .mockResolvedValueOnce({ status: 200, data: { likes: [] } })
      .mockResolvedValueOnce({ status: 200, data: [{ id: 'tip-1' }] })

    await expect(fetchFollowing({ token: 'abc' }, { target_id: 'chef-1' })).resolves.toMatchObject({ success: true })
    await expect(fetchComments({ token: 'abc' }, 'r1', { limit: 5 })).resolves.toMatchObject({ success: true })
    await expect(fetchLikes({ token: 'abc' }, 'r1')).resolves.toMatchObject({ success: true })
    await expect(fetch_cooking_tips(null, { limit: 10 })).resolves.toMatchObject({ success: true })

    expect(axios.get).toHaveBeenCalledTimes(4)
  })

  it('returns fallback data when fetch fails', async () => {
    axios.get.mockRejectedValueOnce({ response: { data: { detail: 'Not found' } } })

    const result = await fetchComments({ token: 'abc' }, 'r1')

    expect(result.success).toBe(false)
    expect(result.message).toBe('Not found')
    expect(result.data).toEqual([])
  })

  it('guards token-dependent mutations before making requests', async () => {
    await expect(like_unlike(null, 'r1')).resolves.toMatchObject({ success: false, message: 'Missing token or recipe ID' })
    await expect(save_unsave_favourites({ token: 'abc' }, null)).resolves.toMatchObject({ success: false, message: 'Missing token or recipe ID' })
    await expect(folow_unfollow(null, 'chef-1')).resolves.toMatchObject({ success: false, message: 'Missing token or Chef !' })
    expect(axios.post).not.toHaveBeenCalled()
  })

  it('posts like, favourite, and follow mutations with bearer tokens', async () => {
    axios.post
      .mockResolvedValueOnce({ status: 200, data: { success: true } })
      .mockResolvedValueOnce({ status: 200, data: { success: true } })
      .mockResolvedValueOnce({ status: 200, data: { success: true } })

    await expect(like_unlike({ token: 'abc' }, 'r1')).resolves.toMatchObject({ success: true })
    await expect(save_unsave_favourites({ token: 'abc' }, 'r1')).resolves.toMatchObject({ success: true })
    await expect(folow_unfollow({ token: 'abc' }, 'chef-1')).resolves.toEqual({ success: true })
    expect(axios.post).toHaveBeenCalledTimes(3)
  })

  it('requires login for generic post and delete helpers', async () => {
    await expect(make_a_post('/recipes/meta', null, {}, [])).resolves.toMatchObject({
      success: false,
      message: 'Kindly login to make the request!',
    })
    await expect(make_a_delete('/recipes/r1', null)).resolves.toMatchObject({
      success: false,
      message: 'Kindly login to make the request!',
    })
  })

  it('wraps generic post and delete helpers with fallback data', async () => {
    axios.post.mockResolvedValueOnce({ status: 200, data: { ok: true } })
    axios.delete.mockRejectedValueOnce({ response: { data: { message: 'Cannot delete' } } })

    await expect(make_a_post('/recipes/meta', { token: 'abc' }, { recipe_ids: ['r1'] }, [])).resolves.toEqual({
      success: true,
      data: { ok: true },
    })
    await expect(make_a_delete('/recipes/r1/comments/1', { token: 'abc' }, {}, ['fallback'])).resolves.toEqual({
      success: false,
      message: 'Cannot delete',
      data: ['fallback'],
    })
  })
})
