import { beforeEach, describe, expect, it } from 'vitest'
import { createTestPinia } from '../test/helpers/pinia'
import { useOngoingStore } from './ongoing'

describe('useOngoingStore', () => {
  beforeEach(() => {
    createTestPinia()
  })

  it('starts with no in-progress recipe data', () => {
    const store = useOngoingStore()

    expect(store.coverRecipe).toBeNull()
    expect(store.recipeSteps).toBeNull()
  })

  it('stores and clears cover recipe draft', () => {
    const store = useOngoingStore()
    const cover = { recipeName: 'Pilau', tags: ['rice'] }

    store.setCoverRecipe(cover)
    expect(store.coverRecipe).toEqual(cover)

    store.clearCoverRecipe()
    expect(store.coverRecipe).toBeNull()
  })

  it('stores and clears recipe steps draft', () => {
    const store = useOngoingStore()
    const steps = { name: 'Pilau', steps: [{ no: 1, instructions: 'Boil' }] }

    store.setRecipeSteps(steps)
    expect(store.recipeSteps).toEqual(steps)

    store.clearRecipeSteps()
    expect(store.recipeSteps).toBeNull()
  })
})
