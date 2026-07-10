# LLMs for Social Scientists

**A book being written in the open.** Read the working draft at **[yemretapan.com/llms4socialscientists](https://yemretapan.com/llms4socialscientists)**.

From using language models to steering, reading, and changing them — hands-on methods for social science research, grown out of the [BLISS](https://bliss.boston) workshops, the AIDE summer bootcamp, and SICSS-Istanbul.

## How this repo works

- Built with [Quarto](https://quarto.org). `_quarto.yml` lists **published** chapters; `_quarto-full.yml` is the full manuscript including drafts.
- Preview everything locally: `quarto preview --profile full`
- Publish a chapter: move its line from `_quarto-full.yml` into `_quarto.yml` and push — CI renders the published profile only.
- Regenerate the book map after adding chapters or links: `python3 scripts/build-book-map.py`
- Comments run on [Giscus](https://giscus.app) (GitHub Discussions); content issues via the [issue template](.github/ISSUE_TEMPLATE/content-issue.md).

## Deployment

On every push to `main`, CI renders the published profile and pushes it to the `gh-pages` branch. The book is served at **yemretapan.com/llms4socialscientists**, where the [yemretapan.com](https://github.com/tapanyemre/yemretapan.com) site build grafts this repo's `gh-pages` output into `/llms4socialscientists`.

To make the public site refresh **automatically** after each book deploy, set one secret:

1. Create a [fine-grained personal access token](https://github.com/settings/tokens?type=beta) — Resource owner **tapanyemre**, Repository access **Only tapanyemre/yemretapan.com**, Permissions → Repository → **Contents: Read and write**.
2. Add it here: `gh secret set SITE_DISPATCH_TOKEN -R tapanyemre/LLMs4SocialScientists` (paste the token when prompted).

The deploy workflow then fires a `repository_dispatch` at yemretapan.com after each build. Until the secret is set, that step is a harmless no-op and the domain copy updates on the next site deploy (or `gh workflow run deploy.yml -R tapanyemre/yemretapan.com --ref v4`).

## License

Text: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · Code: MIT

© 2026 Yunus Emre Tapan
