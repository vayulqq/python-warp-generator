# WARP Config Generator

Python script to generate Cloudflare WARP WireGuard configuration files using the Cloudflare WARP API.

## Features
- Generates WireGuard config files (`WARPYMDHHMM.conf`) with MSK time.
- Automatically installs dependencies (`requests`, `cryptography`, `pytz`).
- Uses randomized User-Agents and serial numbers for better API compatibility.
- Includes retry logic for API requests and file overwrite prevention.

## Requirements
- Python 3.6+
- Internet connection for API calls and dependency installation

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/vayulqq/python-warp-generator.git
   ```

2. Ensure Python is installed:
   ```bash
   python --version
   ```

## Usage
1. Run the script:
   ```bash
   python generate_warp_config.py
   ```
2. The script will:
   - Install required dependencies.
   - Generate a configuration file (e.g., `WARP202506091127.conf`) in the current directory.

## Notes
- File names use MSK time (e.g., `WARP202506091127.conf` for June 9, 2025, 11:27 MSK).
- Cloudflare WARP API may limit registrations from the same IP. Try a different IP if blocked.
- Ensure write permissions in the script's directory. Run as Administrator if needed.
- Manually install dependencies if `pip` fails:
   ```bash
   python -m pip install requests cryptography>=42.0.0 pytz
   ```

## License
MIT
