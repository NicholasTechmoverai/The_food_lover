import { beforeEach, describe, expect, it, vi } from 'vitest'
import axios from 'axios'
import {
  fetchLiveRecipes,
  fetchRecipeMeta,
  fetchRecipeSteps,
  fetchRecipeTypes,
  fetchRecipes,
  saveRecipe,
} from './recipes'

vi.mock('axios', () => ({
  default: {
    post: vi.fn(),
    get: vi.fn(),
    delete: vi.fn(),
  },
}))

describe('recipe API helpers', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('fetches recipe lists with filters and authorization headers', async () => {
    axios.post.mockResolvedValueOnce({ status: 200, data: [{ id: 'r1' }] })

    const result = await fetchRecipes({ token: 'abc' }, { recipe_name: 'pilau' })

    expect(result).toEqual({ success: true, data: [{ id: 'r1' }] })
    expect(axios.post).toHaveBeenCalledWith(
      expect.stringContaining('/recipes/get'),
      { recipe_name: 'pilau' },
      { headers: { Authorization: 'Bearer abc' } },
    )
  })

  it('falls back to runtime recipes when list fetching fails', async () => {
    axios.post.mockRejectedValueOnce(new Error('Network down'))

    const result = await fetchRecipes(null, null)

    expect(result.success).toBe(false)
    expect(result.message).toBe('Network down')
    expect(result.data.length).toBeGreaterThan(0)
  })

  it('fetches recipe steps and falls back to bundled recipe steps on errors', async () => {
    axios.get
      .mockResolvedValueOnce({ status: 200, data: { cover: { name: 'Pilau' }, steps: [{ no: 1 }] } })
      .mockRejectedValueOnce({ response: { data: { detail: 'Missing' } } })

    await expect(fetchRecipeSteps({ token: 'abc' }, 'pilau', 'recipe-id')).resolves.toEqual({
      success: true,
      data: { cover: { name: 'Pilau' }, steps: [{ no: 1 }] },
    })

    const fallback = await fetchRecipeSteps(null, 'runtime', 1)
    expect(fallback.success).toBe(false)
    expect(fallback.message).toBe('Missing')
    expect(fallback.data.cover.recipeName).toContain('Beef')
    expect(fallback.data.steps.steps.length).toBeGreaterThan(0)
  })

  it('validates saveRecipe inputs and posts authenticated recipes', async () => {
    axios.post.mockResolvedValueOnce({ status: 201, data: { recipeId: 'r1' } })

    await expect(saveRecipe(null, {})).resolves.toMatchObject({ success: false })
    await expect(saveRecipe({ token: 'abc' }, null)).resolves.toEqual({ success: false, message: 'Invalid recipe data' })
    await expect(saveRecipe({ token: 'abc' }, { recipeCover: { recipeName: 'Pilau' } })).resolves.toEqual({
      success: true,
      data: { recipeId: 'r1' },
    })
  })

  it('fetches metadata and recipe types with fallback data', async () => {
    axios.get
      .mockResolvedValueOnce({ status: 200, data: { liked: true } })
      .mockRejectedValueOnce(new Error('No recipe types'))

    await expect(fetchRecipeMeta('/recipe/meta', { token: 'abc' }, { recipe_id: 'r1' }, [])).resolves.toEqual({
      success: true,
      data: { liked: true },
    })

    const types = await fetchRecipeTypes()
    expect(types.success).toBe(false)
    expect(types.data.length).toBeGreaterThan(0)
  })

  it('returns bundled live recipes', async () => {
    const recipes = await fetchLiveRecipes()

    expect(recipes.some((recipe) => recipe.live)).toBe(true)
  })
})
