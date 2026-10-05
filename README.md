# Veil

Veil encrypts messages and images, then carries the encrypted data as ordinary-looking chatter or inside a PNG image. It is an experimental privacy tool, not an audited secure-messaging product.

## Use Veil

- **Web app:** [annex-studio.github.io/VEIL/Veil.html](https://annex-studio.github.io/VEIL/Veil.html)
- **Python CLI:** install the dependencies and run `python CLI/veil.py`:

	```bash
	python -m pip install -r CLI/requirements.txt
	python CLI/veil.py
	```

- **Self-host:** follow the [build and deployment guide](docs/documentation/docs/self-hosting.mdx).

## Browser workflows

- **Write / Decode:** encrypt text into casual or work-style chatter and recover it with the same password.
- **Image → text:** encrypt an image into chatter text; the recipient decodes it back to an image.
- **Image in image:** encrypt text or an image inside a PNG cover, then reveal it with the password.

The chatter is camouflage, not encryption. Use a strong unique password and send it separately. Do not resize, recompress, or edit a generated carrier image. Veil does not guarantee protection against steganalysis, compromised devices, or weak passwords.

## Documentation

The [Veil documentation](https://annex-studio.github.io/VEIL/manual/intro.html) covers browser workflows, CLI use, security limitations, and deployment. Source files are in `docs/documentation/`; the canonical browser app is `docs/Veil.html`.
