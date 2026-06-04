import { describe, expect, it } from 'vitest'
import router from './index'

describe('router configuration', () => {
  it('registers core public, auth, recipe, and utility route names', () => {
    const names = router.options.routes.flatMap((route) => {
      const childNames = route.children?.flatMap((child) => [
        child.name,
        ...(child.children?.flatMap((nested) => [
          nested.name,
          ...(nested.children?.map((deep) => deep.name) ?? []),
        ]) ?? []),
      ]) ?? []
      return [route.name, ...childNames]
    })

    for (const name of [
      'LandingPage',
      'RecipesPage',
      'RecipeId',
      'LoginPage',
      'SignupPage',
      'SettingsPage',
      'NotFound',
    ]) {
      expect(names).toContain(name)
    }
  })

  it('resolves landing page at root path', () => {
    const resolved = router.resolve('/')

    expect(resolved.name).toBe('LandingPage')
  })

  it('resolves login and signup auth routes', () => {
    expect(router.resolve('/register/login').name).toBe('LoginPage')
    expect(router.resolve('/register/signup').name).toBe('SignupPage')
  })

  it('keeps nested recipe creation routes reachable', () => {
    expect(router.resolve('/recipes/new/cover').name).toBe('CoverInfo')
    expect(router.resolve('/recipes/new/e/step-1').name).toBe('NewRecipeUploadsWithId')
    expect(router.resolve('/recipes/new/e/step-1').params.id).toBe('step-1')
  })

  it('resolves recipe detail route with name and id params', () => {
    const resolved = router.resolve('/recipes/pilau/abc-123')

    expect(resolved.name).toBe('RecipeId')
    expect(resolved.params.recipe_name).toBe('pilau')
    expect(resolved.params.recipe_id).toBe('abc-123')
  })

  it('resolves profile route for usernames', () => {
    const resolved = router.resolve('/chef_nia')

    expect(resolved.name).toBe('ProfilePage')
    expect(resolved.params.username).toBe('chef_nia')
  })
})
