# LOTWebHooks

<p align="center">
  <a href="https://lotwebhooks.github.io/">
    <img src="./assets/logo.png" alt="LOTWebHooks — Living Off The WebHooks" width="180">
  </a>
</p>

LOTWebHooks is a community-maintained reference catalog of webhook services and endpoints that may be abused for data exfiltration or command-and-control (C2). It is intended to support security research and defensive detection.

## Project links

- **Live site:** <https://lotwebhooks.github.io/>
- **Source repository:** <https://github.com/LOTWebHooks/LOTWebhooks.github.io>
- **Contributors:** <https://lotwebhooks.github.io/contributors.html>
- **About the project:** <https://lotwebhooks.github.io/about.html>
- **Issues and corrections:** <https://github.com/LOTWebHooks/LOTWebhooks.github.io/issues>
- **MITRE ATT&CK — Exfiltration Over Web Service (T1567.004):** <https://attack.mitre.org/techniques/T1567/004/>

## Contributing

1. Fork and clone the [repository](https://github.com/LOTWebHooks/LOTWebhooks.github.io).
2. Add or update a row in the `#hooks` table in [`index.html`](./index.html). Include the service name, endpoint pattern, type, and a useful reference URL or explanation.
3. Regenerate the CSV and entry-count badge:

   ```sh
   python3 scripts/generate_csv.py
   ```

   The script uses only the Python standard library and writes [`data/webhooks.csv`](./data/webhooks.csv) and [`data/badge.json`](./data/badge.json).
4. Open `index.html` locally and check that the new row, search, and type filter work as expected.
5. Commit the page and generated-data updates, then open a pull request against the `main` branch.

Please use reliable references, keep endpoint patterns accurate, and avoid including credentials or live tokens.

## Project files

- [`index.html`](./index.html) — searchable webhook catalog.
- [`about.html`](./about.html) — project maintainer information.
- [`contributors.html`](./contributors.html) — project leads and live GitHub contributor list.
- [`scripts/generate_csv.py`](./scripts/generate_csv.py) — exports the HTML catalog and updates the entry-count badge.
- [`data/webhooks.csv`](./data/webhooks.csv) — generated CSV version of the catalog.
- [`data/badge.json`](./data/badge.json) — generated catalog count used by the contributors page.

## Contact

- Kamran Saifullah: <https://www.linkedin.com/in/kamransaifullah/>