# Veil

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

**Veil** encrypts messages and images, then carries the encrypted data as ordinary-looking chatter or inside a PNG image. It is an experimental privacy tool designed for journalists, whistleblowers, dissidents, and anyone who values confidential communication.

> **Warning:** Veil is an experimental privacy tool, **not** an audited secure-messaging product. Do not rely on it as the sole protection for high-risk or life-critical communication.

## Features

- **Password-based encryption:** AES-256-GCM with PBKDF2 key derivation (250,000 iterations)
- **Text steganography:** Encode encrypted data as casual banter or office chatter
- **Image steganography:** Hide encrypted data inside PNG images using LSB (Least Significant Bit) encoding
- **Cross-platform:** Browser-based web app and Python CLI
- **No server required:** All processing happens locally on your device

## Quick Start

### Web App (Recommended)

Use the hosted version at: **[https://annex-studio.github.io/VEIL/Veil.html](https://annex-studio.github.io/VEIL/Veil.html)**

Or open `docs/Veil.html` in your browser for local use.

### Python CLI

```bash
# Install dependencies
python -m pip install -r CLI/requirements.txt

# Run the interactive CLI
python CLI/veil.py
```

On Windows:
```powershell
py -3 -m pip install -r CLI\requirements.txt
py -3 CLI\veil.py
```

## Workflows

### 1. Write / Decode (Text to Chatter)

Encrypt a text message and disguise it as everyday conversation:

```
Write mode:
- Enter your secret message
- Choose flavor: Casual Banter or Office Chatter
- Set a strong password
- Copy the generated chatter text

Decode mode:
- Paste the full chatter text (including [B] or [O] prefix)
- Enter the same password
- Recover the original message
```

### 2. Image → Text

Encrypt an image file and convert it to chatter text:

```
- Select or drop an image file
- Choose chatter flavor and set password
- Encrypt to chatter
- Share the text

Recipient uses Decode mode with the password to recover the image.
```

### 3. Image in Image (Steganography)

Hide encrypted data inside a cover image:

```
Hide mode:
- Load a cover image (PNG/JPG)
- Choose to hide text or an image
- Enter your secret and password
- Download the carrier PNG

Reveal mode:
- Load the carrier PNG
- Enter the password
- Recover the hidden content
```

> **Important:** Do NOT resize, recompress, or edit the carrier image. Any modification can corrupt the hidden data.

## Security Model

### What Veil Protects Against

- ✅ Disclosure of plaintext when someone has only the carrier (not the password)
- ✅ Undetected modification of encrypted content (AES-GCM authentication)

### What Veil Does NOT Protect Against

- ❌ Steganalysis or determined inspection of the carrier
- ❌ Weak, reused, or compromised passwords
- ❌ Malware, keyloggers, or compromised devices
- ❌ Metadata in cover images or sharing patterns
- ❌ Loss from editing carrier images
- ❌ Implementation vulnerabilities (unaudited code)

### Encryption Details

- **Algorithm:** AES-256-GCM
- **Key Derivation:** PBKDF2-HMAC-SHA-256
- **Iterations:** 250,000
- **Authentication Tag:** 96-bit
- **Salt:** 16 bytes (random per encryption)
- **Nonce:** 12 bytes (random per encryption)

## Documentation

Full documentation is available at:
**[https://annex-studio.github.io/VEIL/manual/intro.html](https://annex-studio.github.io/VEIL/manual/intro.html)**

- [Browser User Guide](https://annex-studio.github.io/VEIL/manual/user-guide) - Complete guide to all browser workflows
- [Python CLI Guide](https://annex-studio.github.io/VEIL/manual/cli) - CLI installation and usage
- [Build and Self-Host](https://annex-studio.github.io/VEIL/manual/self-hosting) - Host your own instance
- [Security Model and Limitations](https://annex-studio.github.io/VEIL/manual/security-model) - Understanding the security properties

## Self-Hosting

Veil is a static web application. You can self-host it:

```bash
# Build the documentation site (includes Veil.html)
cd docs/documentation
npm install
npm run build

# The built site will be in docs/manual/
# Serve docs/manual/ with any static web server
```

See the [self-hosting guide](https://annex-studio.github.io/VEIL/manual/self-hosting) for detailed instructions.

## Project Structure

```
VEIL/
├── CLI/
│   ├── veil.py           # Main CLI application
│   ├── requirements.txt  # Python dependencies
│   └── veil.spec         # PyInstaller spec for building standalone executable
├── docs/
│   ├── Veil.html         # Canonical browser application
│   ├── manual/           # Built documentation (generated)
│   └── documentation/    # Documentation source (Docusaurus)
├── README.md             # This file
└── LICENSE               # MIT License
```

## Building Standalone Executable

```bash
# Install PyInstaller
python -m pip install pyinstaller

# Build from CLI directory
cd CLI
pyinstaller veil.spec

# Executable will be in CLI/dist/
```

Note: Build on each target platform separately (Windows, macOS, Linux).

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Disclaimer

**Veil is experimental software.** It has not been audited by security professionals. Use at your own risk. The authors are not responsible for any data loss, privacy breaches, or other issues that may arise from using this software.

For high-security use cases, use established, audited secure communication tools instead.
