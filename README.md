# TDDProject

This template should help get you started developing with Vue 3 in Vite.

## Recommended IDE Setup

[VSCode](https://code.visualstudio.com/) + [Volar](https://marketplace.visualstudio.com/items?itemName=Vue.volar) (and disable Vetur).

## Customize configuration

See [Vite Configuration Reference](https://vite.dev/config/).

## Project Setup

```sh
npm install
```

### Compile and Hot-Reload for Development

```sh
npm run dev
```

### Compile and Minify for Production

```sh
npm run build
```

### Run Unit Tests with [Vitest](https://vitest.dev/)

```sh
npm run test:unit
```


Objectif : créer un projet Amplify avec une Labda qui enregistre un utilisateur dans DynamoBD, et écrire des tests unitaires mockés avec Moto pour valider la logique.

On part sur un projet backend pur sans API REST exposée, juste :
- Un code métier : add_user(), get_user()
- Une table DynamoBD créée via Amplify
- Un fonction Lambda qui s'en sert
- Des test locaux simulés avec Moto
- Optionnellement : tu les intègres dans CI/CD Amplify