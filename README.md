# Astro Starter Kit: Blog

```
npm create astro@latest -- --template blog
```

[![Open in StackBlitz](https://developer.stackblitz.com/img/open_in_stackblitz.svg)](https://stackblitz.com/github/withastro/astro/tree/latest/examples/blog)
[![Open with CodeSandbox](https://assets.codesandbox.io/github/button-edit-lime.svg)](https://codesandbox.io/p/sandbox/github/withastro/astro/tree/latest/examples/blog)
[![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/withastro/astro?devcontainer_path=.devcontainer/blog/devcontainer.json)

> 🧑‍🚀 **Seasoned astronaut?** Delete this file. Have fun!

![blog](https://github.com/withastro/astro/assets/2244813/ff10799f-a816-4703-b967-c78997e8323d)

Features:

- ✅ Minimal styling (make it your own!)
- ✅ 100/100 Lighthouse performance
- ✅ SEO-friendly with canonical URLs and OpenGraph data
- ✅ Sitemap support
- ✅ RSS Feed support
- ✅ Markdown & MDX support

## 🚀 Project Structure

Inside of your Astro project, you'll see the following folders and files:

```
├── public/
├── src/
│   ├── components/
│   ├── content/
│   ├── layouts/
│   └── pages/
├── astro.config.mjs
├── README.md
├── package.json
└── tsconfig.json
```

Astro looks for `.astro` or `.md` files in the `src/pages/` directory. Each page is exposed as a route based on its file name.

There's nothing special about `src/components/`, but that's where we like to put any Astro/React/Vue/Svelte/Preact components.

The `src/content/` directory contains "collections" of related Markdown and MDX documents. Use `getCollection()` to retrieve posts from `src/content/blog/`, and type-check your frontmatter using an optional schema. See [Astro's Content Collections docs](https://docs.astro.build/en/guides/content-collections/) to learn more.

Any static assets, like images, can be placed in the `public/` directory.

## 🧞 Commands

All commands are run from the root of the project, from a terminal:

| Command                   | Action                                           |
| :------------------------ | :----------------------------------------------- |
| `npm install`             | Installs dependencies                            |
| `npm run dev`             | Starts local dev server at `localhost:3000`      |
| `npm run build`           | Build your production site to `./dist/`          |
| `npm run preview`         | Preview your build locally, before deploying     |
| `npm run astro ...`       | Run CLI commands like `astro add`, `astro check` |
| `npm run astro -- --help` | Get help using the Astro CLI                     |

## 👀 Want to learn more?

Check out [our documentation](https://docs.astro.build) or jump into our [Discord server](https://astro.build/chat).

## Credit

This theme is based off of the lovely [Bear Blog](https://github.com/HermanMartinus/bearblog/).

## npm create astro@latest -- --template blog log / choices

    $npm create astro@latest -- --template blog log / choices
    Need to install the following packages:
      create-astro@3.1.11
    Ok to proceed? (y)

    astro   v2.10.1 Launch sequence initiated.

      dir   Where should we create your new project?
            ./
     tmpl   tmpl Using blog as project template
        ✔  Template copied

     deps   Install dependencies?
            Yes
        ✔  Dependencies installed

       ts   Do you plan to write TypeScript?
            Yes

      use   How strict should TypeScript be?
            Strict
        ✔  TypeScript customized

      git   Initialize a new git repository?
            Yes
        ✔  Git initialized

     next   Liftoff confirmed. Explore your project!
            Run npm run dev to start the dev server. CTRL+C to stop.
            Add frameworks like react or tailwind using astro add.

            Stuck? Join us at https://astro.build/chat

## npm run astro -- --help 

    $ npm run astro -- --help

    > astro
    > astro --help


       astro  v2.10.1 Build faster websites.

      astro [command] [...flags]

       Commands
                    add  Add an integration.
                  build  Build your project and write it to disk.
                  check  Check your project for errors.
                    dev  Start the development server.
                   docs  Open documentation in your web browser.
                   info  List info about your current Astro setup.
                preview  Preview your build locally.
                   sync  Generate content collection types.
              telemetry  Configure telemetry settings.

       Global Flags
        --config <path>  Specify your config file.
          --root <path>  Specify your project root folder.
           --site <url>  Specify your project site.
      --base <pathname>  Specify your project base.
              --verbose  Enable verbose logging.
               --silent  Disable all logging.
              --version  Show the version number and exit.
                 --help  Show this help message.

## Deploy your Astro Site to GitHub Pages

 https://docs.astro.build/en/guides/deploy/github/

 extend astro.config.mjs with

     site: 'https://roebi.github.io',
     base: '/roebi-halter-in-blog'

add file .github/workflows/deploy.yml
with content from docu
