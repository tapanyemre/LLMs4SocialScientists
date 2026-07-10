# LLMs for Social Scientists

**A book being written in the open.** Read the working draft at **[yemretapan.com/llms4socialscientists](https://yemretapan.com/llms4socialscientists)**.

From using language models to steering, reading, and changing them — hands-on methods for social science research, grown out of the [BLISS](https://bliss.boston) workshops, the AIDE summer bootcamp, and SICSS-Istanbul.

## How this repo works

- Built with [Quarto](https://quarto.org). `_quarto.yml` lists **published** chapters; `_quarto-full.yml` is the full manuscript including drafts.
- Preview everything locally: `quarto preview --profile full`
- Publish a chapter: move its line from `_quarto-full.yml` into `_quarto.yml` and push — CI renders the published profile only.
- Regenerate the book map after adding chapters or links: `python3 scripts/build-book-map.py`
- Comments run on [Giscus](https://giscus.app) (GitHub Discussions); content issues via the [issue template](.github/ISSUE_TEMPLATE/content-issue.md).

## License

Text: [CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) · Code: MIT

© 2026 Yunus Emre Tapan
