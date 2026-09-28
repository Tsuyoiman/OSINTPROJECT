# Classroom OSINT Investigation Tool

This project is the Kali Linux investigation client for the authorized,
fictional Facebook-style classroom laboratory.

The client communicates only with the instructor's fictional web application
through public HTTP endpoints. It does not log in, bypass authentication,
access MongoDB, extract private messages, or target real people.

The lab demonstrates this investigation chain:

```text
Public clue
  -> identify username
  -> collect public profile information
  -> correlate friends, organizations, posts, and clues
  -> analyze authorized public images
  -> perform authorized network reconnaissance
  -> document the findings in an OSINT report
```

## 1. Lab architecture

There are two separate projects:

1. **Facebook-and-Osint-Lab** — the fictional website and Express API running
   on the instructor's Windows computer.
2. **OSINTPROJECT** — this Python client running on the student's Kali VM.

The default classroom target is:

```text
http://192.168.100.7:8000
```

The Express backend intentionally has no route at `/`. Therefore this is
normal:

```text
GET /       -> 404 Cannot GET /
```

An HTTP 404 response from `/` still proves that a web server answered. This
client tests `/searchUsers?q=a` instead.

## 2. Requirements before using Kali

The instructor must first start the fictional website on Windows. The
backend must listen on all network interfaces, not only localhost:

```text
0.0.0.0:8000
```

The Kali VM must be able to reach the Windows host. In VMware, use a network
mode appropriate for the classroom:

- **Bridged** — Kali and Windows receive addresses on the same LAN.
- **Host-only** — useful for an isolated host-to-VM classroom network.
- **NAT** — requires VMware port forwarding from Kali to the Windows host.

Windows Firewall must allow inbound TCP port `8000` for the authorized
classroom network. Do not expose the fictional lab to the public Internet.

## 3. Find the target address

The default address is `192.168.100.7`, but the instructor's address may
change. On Windows, find the IPv4 address with:

```powershell
ipconfig
```

Look for the adapter used by the VMware network. On Kali, verify basic
reachability:

```bash
ping -c 3 192.168.100.7
```

If ping is disabled, test the API directly instead:

```bash
curl -i "http://192.168.100.7:8000/searchUsers?q=Megan"
```

An HTTP response means Kali can reach the server. A timeout or connection
refusal indicates a server, firewall, VMware networking, IP, or port problem.

## 4. Clone the project on Kali

Open a terminal in Kali and run:

```bash
cd ~
git clone https://github.com/Tsuyoiman/OSINTPROJECT.git
cd OSINTPROJECT
```

If the project is already cloned, update it instead:

```bash
cd ~/OSINTPROJECT
git pull
```

Confirm that the required files exist:

```bash
ls -la
```

You should see files including:

```text
config.py
main.py
connection.py
username.py
install.sh
osint-lab
requirements.txt
```

## 5. Configure the target

Open the configuration file:

```bash
nano config.py
```

Set these values to the instructor's Windows server:

```python
LAB_IP = "192.168.100.7"
LAB_PORT = 8000
FRONTEND_PORT = 3000
```

Save in nano with `Ctrl+O`, press `Enter`, then exit with `Ctrl+X`.

The backend API normally runs on port `8000`. The React frontend normally
runs on port `3000` and serves profile images.

## 6. Install the Kali dependencies

Make the scripts executable:

```bash
cd ~/OSINTPROJECT
chmod +x install.sh osint-lab
```

Run the installer:

```bash
./install.sh
```

The installer performs these steps:

1. Attempts to install optional `nmap` and ExifTool packages.
2. Attempts to create an isolated Python virtual environment.
3. Installs the Python dependencies from `requirements.txt`.
4. Falls back automatically when Kali does not have `ensurepip`.
5. Makes the `osint-lab` launcher executable.

### If the virtual environment fails

Kali may display an error saying that `ensurepip` or
`python3.11-venv` is unavailable. This does not necessarily prevent the
client from running. Use the system-Python fallback:

```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

If pip is not installed:

```bash
sudo apt install -y python3-pip python3-requests
```

Then retry:

```bash
python3 -m pip install --break-system-packages -r requirements.txt
```

If Kali's package index is stale, refresh it first:

```bash
sudo apt update
```

Third-party repository errors, such as an expired WineHQ signing key, are
unrelated to this project. The Python fallback may still be usable even when
an optional package installation fails.

## 7. Start the investigation client

Preferred launch command:

```bash
cd ~/OSINTPROJECT
./osint-lab
```

Direct launch also works:

```bash
python3 main.py
```

If a virtual environment was successfully created, the launcher uses it
automatically. Otherwise it uses Kali's `python3`.

## 8. Test the connection

At the menu, select:

```text
[1] Test Target Connection
```

A successful result looks similar to:

```text
[+] Target is reachable (HTTP 200)
[+] Classroom website detected
```

You can test the same endpoint manually:

```bash
curl -i "http://192.168.100.7:8000/searchUsers?q=Megan"
```

You can test a known fictional profile:

```bash
curl -i "http://192.168.100.7:8000/publicProfile/megan_fox"
```

## 9. Use the investigation workflow

### Option 1 — Test Target Connection

Confirms that Kali can reach the public API.

### Option 2 — Search Public Users

Search by a display name, partial name, or username:

```text
Megan Fox
```

The search returns public usernames. Use the returned handle in option 3.

### Option 3 — Investigate Username / View Full Profile

Enter the exact fictional username:

```text
megan_fox
```

The tool displays publicly exposed information such as:

- name
- username
- biography
- job
- workplace
- college
- current city
- hometown
- organizations
- fictional clue references
- public posts
- public friends

The tool also records the result in the current evidence log.

### Option 4 — Correlate Friends and Organizations

Investigate a profile first, then select option 4. The tool pivots through
the profile's public friends and retrieves their public profiles. It reports
related usernames, workplaces, and shared organizations.

This demonstrates the central OSINT lesson: several individually harmless
public facts can become more informative when correlated.

### Option 5 — Download Profile Images

Investigate a profile first, then select option 5. Publicly served profile
and cover images are saved under:

```text
output/images/<username>/
```

If ExifTool is installed, the tool automatically displays image metadata.
Install it manually if necessary:

```bash
sudo apt install -y libimage-exiftool-perl
```

### Option 6 — Authorized Network Reconnaissance

Use this option only against the authorized classroom target or another
address inside the authorized network:

```text
192.168.100.0/24
```

The tool refuses targets outside that range. The default target is
`192.168.100.7`.

Install Nmap if necessary:

```bash
sudo apt install -y nmap
```

The tool runs a basic version/service scan:

```text
nmap -sV -Pn <authorized-ip>
```

Do not use this feature against arbitrary Internet systems.

### Option 7 — Generate OSINT Investigation Report

After collecting evidence, select option 7. The report is saved under:

```text
output/report_<username>_<timestamp>.txt
```

The report contains these 17 sections:

1. Investigation objective
2. Target identification
3. Scope
4. Public information discovered
5. Username/profile findings
6. Public posts
7. Related users
8. Organizations/projects
9. Events and clue references
10. Image/metadata findings
11. Network reconnaissance findings
12. Evidence
13. Relationship/correlation analysis
14. Security observations
15. Limitations
16. Ethical considerations
17. Conclusion

## 10. Example complete session

```text
cd ~/OSINTPROJECT
git pull
chmod +x install.sh osint-lab
./install.sh
./osint-lab
```

Inside the program:

```text
1
2 -> Megan Fox
3 -> megan_fox
4
5
6 -> 192.168.100.7
7
8
```

The generated evidence and reports remain local to the Kali project folder.

## 11. Troubleshooting

### `requirements.txt` cannot be opened

You are not in the project directory:

```bash
cd ~/OSINTPROJECT
ls -la requirements.txt
```

### `source .venv/bin/activate` does not exist

Do not activate the environment manually. Run:

```bash
./install.sh
./osint-lab
```

The launcher automatically uses `.venv` only when it exists and is valid.

### `ensurepip is not available`

Use the system-Python fallback:

```bash
python3 -m pip install --break-system-packages -r requirements.txt
./osint-lab
```

### Browser cannot connect, but curl works

Check the exact URL and port:

```text
http://192.168.100.7:8000/publicProfile/megan_fox
```

Do not rely on the root URL `/`, because the API intentionally returns 404
there. Also confirm that the browser is not using a proxy that bypasses the
VM's classroom route.

### Curl returns `Connection refused` or times out

Check all of the following:

1. The Windows Facebook clone server is running.
2. The backend is listening on port `8000`.
3. The backend listens on `0.0.0.0`, not only `127.0.0.1`.
4. The Windows firewall allows TCP `8000`.
5. Kali and Windows are on reachable VMware networks.
6. `LAB_IP` in `config.py` is current.

### Profile lookup returns no data

Use a seeded fictional handle, not an email address:

```text
megan_fox
zendaya
margot_robbie
ana_de_armas
jenna_ortega
scarlett_johansson
```

You can also search by display name with option 2 first.

### Nmap or ExifTool is unavailable

Install the optional tools:

```bash
sudo apt install -y nmap libimage-exiftool-perl
```

The profile search and report features do not require these optional tools.

## 12. Ethical and authorization rules

This laboratory is limited to fictional classroom data and the
instructor-authorized network. Students must not:

- target real Facebook, real people, or real organizations
- attempt password theft or account takeover
- bypass authentication or access private messages
- access MongoDB directly
- scan arbitrary Internet addresses
- download private or restricted content
- use the tool for stalking or harassment

The purpose is to learn responsible public-information collection,
correlation, authorized reconnaissance, evidence handling, and security
reporting.
