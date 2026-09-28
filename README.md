# Classroom OSINT Investigation Tool

This is a Kali Linux command-line client for the authorized fictional
Facebook-style classroom lab. It uses only public HTTP endpoints exposed by
the lab website; it does not log in, access MongoDB, bypass controls, or
target real people.

## Quick start on Kali

From the cloned project directory:

```bash
cd ~/OSINTPROJECT
git pull
chmod +x install.sh osint-lab
./install.sh
./osint-lab
```

The installer first tries to create `.venv`. If Kali cannot provide
`ensurepip`, it automatically falls back to installing the small Python
dependency set with Kali's `--break-system-packages` option. Nmap and ExifTool
are installed on a best-effort basis; the core client still works if those
optional packages are unavailable.

## Configure the target

Edit `config.py` if the instructor assigns a different server:

```python
LAB_IP = "192.168.100.7"
LAB_PORT = 8000
```

The client expects the backend's public routes:

- `GET /searchUsers?q=<query>`
- `GET /publicProfile/<username>`

The backend intentionally has no `/` route, so an HTTP 404 at
`http://192.168.100.7:8000/` does not mean the server is unreachable. Option
1 probes `/searchUsers?q=a` instead.

## Investigation workflow

1. **Test Target Connection** — verifies the HTTP API is reachable.
2. **Search Public Users** — search a name or clue and identify usernames.
3. **Investigate Username / View Full Profile** — collect public fields,
   posts, organizations, clues, and public friends.
4. **Correlate Friends & Organizations** — pivot to related public profiles
   and identify shared organizations.
5. **Download Profile Images** — save publicly served images and run ExifTool
   when installed.
6. **Authorized Network Reconnaissance** — run an Nmap service scan only for
   addresses inside `192.168.100.0/24`.
7. **Generate OSINT Investigation Report** — write a 17-section report to
   `output/`.

Seeded example usernames include `megan_fox`, `zendaya`, `margot_robbie`,
`ana_de_armas`, `jenna_ortega`, and `scarlett_johansson`. Display names also
work through the public search fallback, for example `Megan Fox`.

## Troubleshooting

Check the API directly from Kali:

```bash
curl -i "http://192.168.100.7:8000/searchUsers?q=Megan"
curl -i "http://192.168.100.7:8000/publicProfile/megan_fox"
```

An HTTP response proves that Kali can reach the server. A timeout or
connection refusal indicates a VMware network mode, Windows firewall, server
status, IP address, or port issue. The website server must be running on the
Windows host and listening on `0.0.0.0:8000`, not only `127.0.0.1:8000`.

All reconnaissance must remain inside the instructor-authorized classroom
network. Do not use this tool against Internet targets or real individuals.