import os
import re
import sys
import math
import struct
import getpass
from Crypto.Cipher import AES
from Crypto.Protocol.KDF import PBKDF2
from Crypto.Hash import SHA256
from Crypto.Random import get_random_bytes
from PIL import Image

# --- 1. CRYPTO ---
TAG_BYTES = 12  # 96-bit auth tag

def derive_key(password: str, salt: bytes) -> bytes:
    return PBKDF2(password, salt, 32, count=250000, hmac_hash_module=SHA256)

def encrypt_bytes(plain_bytes: bytes, password: str) -> bytes:
    salt = get_random_bytes(16)
    nonce = get_random_bytes(12)
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=TAG_BYTES)
    ciphertext, tag = cipher.encrypt_and_digest(plain_bytes)
    return salt + nonce + ciphertext + tag

def decrypt_bytes(packed: bytes, password: str) -> bytes:
    if len(packed) < 16 + 12 + TAG_BYTES:
        raise ValueError("Payload too short to be valid.")
    salt = packed[:16]
    nonce = packed[16:28]
    data = packed[28:-TAG_BYTES]
    tag = packed[-TAG_BYTES:]
    
    key = derive_key(password, salt)
    cipher = AES.new(key, AES.MODE_GCM, nonce=nonce, mac_len=TAG_BYTES)
    return cipher.decrypt_and_verify(data, tag)

def pack_image(mime: str, data: bytes) -> bytes:
    mime_bytes = mime.encode('utf-8')
    out = bytearray()
    out.extend(b'IMG1')
    out.append(len(mime_bytes))
    out.extend(mime_bytes)
    out.extend(data)
    return bytes(out)

def unpack_image(packed: bytes):
    if len(packed) < 5 or packed[:4] != b'IMG1':
        return None
    mime_len = packed[4]
    if len(packed) < 5 + mime_len:
        return None
    mime = packed[5:5+mime_len].decode('utf-8')
    data = packed[5+mime_len:]
    return mime, data

# --- 2a. CODEC: CHATTER ---
A_BANTER = ["literally", "honestly", "kinda", "pretty", "super", "really", "probably", "definitely", "totally", "actually", "basically", "seriously", "obviously", "apparently", "clearly", "finally"]
B_BANTER = ["running late", "almost done", "on my way", "still waiting", "good to go", "out of time", "not sure yet", "way too tired", "super busy", "free tonight", "stuck in traffic", "about to leave", "back online", "taking a break", "heading out", "just landed"]

A_OFFICE = ["quickly", "briefly", "roughly", "currently", "technically", "generally", "effectively", "ideally", "ultimately", "specifically", "apparently", "presumably", "eventually", "immediately", "accordingly", "respectively"]
B_OFFICE = ["reviewing the doc", "stuck in a meeting", "waiting on approval", "pushing the update", "closing the ticket", "following up later", "checking the build", "syncing with the team", "finishing the report", "blocked on design", "out until noon", "joining the call", "sharing my screen", "updating the board", "merging the branch", "running a bit behind"]

FLAVORS = {
    "banter": {"A": A_BANTER, "B": B_BANTER, "tag": "B"},
    "office": {"A": A_OFFICE, "B": B_OFFICE, "tag": "O"},
}
TAG_TO_FLAVOR = {"B": "banter", "O": "office"}
GROUP_PATTERN = [3, 4, 2, 5, 3, 4, 2, 5]

def bytes_to_chatter(data: bytes, A: list, B: list) -> str:
    fragments = []
    for i, b in enumerate(data):
        hi = (b >> 4) & 0xf
        lo = b & 0xf
        ai = (i * 3 + hi) % 16
        bi = (i * 7 + lo) % 16
        fragments.append(f"{A[ai]} {B[bi]}")
        
    lines = []
    idx, g = 0, 0
    while idx < len(fragments):
        n = GROUP_PATTERN[g % len(GROUP_PATTERN)]
        chunk = fragments[idx:idx+n]
        joiner = " and " if g % 3 == 2 else ", "
        line = joiner.join(chunk)
        lines.append(line[0].upper() + line[1:])
        idx += n
        g += 1
    return "\n".join(lines)

def chatter_to_bytes(text: str, A: list, B: list) -> bytes:
    raw_fragments = []
    for line in text.strip().split('\n'):
        parts = re.split(r'\s*,\s*|\s+and\s+', line.lower())
        raw_fragments.extend([p.strip() for p in parts if p.strip()])
        
    if not raw_fragments: return None
    out = bytearray()
    for i, frag in enumerate(raw_fragments):
        tokens = frag.split()
        if len(tokens) < 2: return None
        a_word = tokens[0]
        b_word = " ".join(tokens[1:])
        if a_word not in A or b_word not in B: return None
        ai = A.index(a_word)
        bi = B.index(b_word)
        hi = ((ai - i * 3) % 16 + 16) % 16
        lo = ((bi - i * 7) % 16 + 16) % 16
        out.append((hi << 4) | lo)
    return bytes(out)

def packed_to_chatter(packed: bytes, flavor: str) -> str:
    flav = FLAVORS[flavor]
    return f"[{flav['tag']}] " + bytes_to_chatter(packed, flav["A"], flav["B"])

def chatter_to_packed(raw: str) -> bytes:
    m = re.match(r'^\[([BO])\]\s*([\s\S]*)$', raw.strip())
    if not m: return None
    flav = FLAVORS[TAG_TO_FLAVOR[m.group(1)]]
    return chatter_to_bytes(m.group(2), flav["A"], flav["B"])

# --- 2b. CODEC: STEGANOGRAPHY ---
STEGO_MAGIC = b'STEG'
STEGO_HEADER_BYTES = 9
STEGO_FLATTEN_BG = (247, 248, 243)
MAX_STEGO_DIM = 3000

def flatten_image_data_to_opaque(img: Image.Image) -> Image.Image:
    if img.mode != 'RGBA':
        img = img.convert('RGBA')
    pixels = img.load()
    for y in range(img.height):
        for x in range(img.width):
            r, g, b, a = pixels[x, y]
            if a == 255: continue
            inv = 255 - a
            nr = round((r * a + STEGO_FLATTEN_BG[0] * inv) / 255)
            ng = round((g * a + STEGO_FLATTEN_BG[1] * inv) / 255)
            nb = round((b * a + STEGO_FLATTEN_BG[2] * inv) / 255)
            pixels[x, y] = (nr, ng, nb, 255)
    return img

def upscale_cover_to_fit(img: Image.Image, needed_bytes: int) -> Image.Image:
    pixels_needed = math.ceil((needed_bytes * 8) / 3 * 1.1)
    scale = math.sqrt(pixels_needed / (img.width * img.height))
    new_w = min(math.ceil(img.width * scale), MAX_STEGO_DIM)
    new_h = min(math.ceil(img.height * scale), MAX_STEGO_DIM)
    scaled = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
    return flatten_image_data_to_opaque(scaled)

def write_bits_into_image(img: Image.Image, payload: bytes) -> Image.Image:
    if img.mode != 'RGBA': img = img.convert('RGBA')
    raw = bytearray(img.tobytes())
    total_bits = len(payload) * 8
    bit_idx = 0
    
    for i in range(len(raw)):
        if bit_idx >= total_bits: break
        if (i % 4) == 3: continue  # Skip alpha
        byte_val = payload[bit_idx >> 3]
        bit = (byte_val >> (7 - (bit_idx & 7))) & 1
        raw[i] = (raw[i] & 0xfe) | bit
        bit_idx += 1
        
    if bit_idx < total_bits:
        raise ValueError("Payload is larger than image capacity")
    return Image.frombytes("RGBA", img.size, bytes(raw))

def read_bits_from_image(raw_bytes: bytes, byte_count: int, is_legacy: bool = False) -> bytes:
    total_bits = byte_count * 8
    out = bytearray(byte_count)
    bit_idx = 0
    
    for i in range(len(raw_bytes)):
        if bit_idx >= total_bits: break
        if not is_legacy and (i % 4) == 3: continue
        bit = raw_bytes[i] & 1
        out[bit_idx >> 3] |= bit << (7 - (bit_idx & 7))
        bit_idx += 1
        
    return bytes(out)

# --- 3. TUI (Text User Interface) ---
class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    DIM = '\033[2m'

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_banner():
    banner = f"""{Colors.GREEN}{Colors.BOLD}
      ,-----.       ____   ____     .__.__ 
     /       \\      \\   \\ /   /____ |__|  |
     |       |       \\   Y   // __ \\|  |  |
      \\     /         \\     /\\  ___/|  |  |__
       \\   /           \\___/  \\___  >__|____/
        \\ /                       \\/       
         V                                 
{Colors.ENDC}{Colors.DIM}
Local Privacy Workspace (AIO Interactive CLI)
Encryption: AES-256-GCM
{Colors.ENDC}"""
    print(banner)

def get_multiline_input(prompt):
    print(prompt)
    print(f"{Colors.DIM}(Press Enter twice to finish){Colors.ENDC}")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    return "\n".join(lines)

def pause():
    input(f"\n{Colors.DIM}Press Enter to return to menu...{Colors.ENDC}")

def tui_write():
    secret = get_multiline_input(f"\n{Colors.CYAN}[Write] Enter your secret message:{Colors.ENDC}")
    if not secret.strip():
        print(f"{Colors.FAIL}Message cannot be empty.{Colors.ENDC}")
        return pause()
        
    flavor_choice = input(f"Disguise as (1: Casual Banter, 2: Office Chatter) [1]: ")
    flavor = "office" if flavor_choice.strip() == "2" else "banter"
    
    password = getpass.getpass(f"Password: ")
    if not password:
        print(f"{Colors.FAIL}Password required.{Colors.ENDC}")
        return pause()
        
    print(f"{Colors.DIM}Encrypting...{Colors.ENDC}")
    packed = encrypt_bytes(secret.encode('utf-8'), password)
    chatter = packed_to_chatter(packed, flavor)
    
    print(f"\n{Colors.GREEN}{Colors.BOLD}--- Disguised Message ---{Colors.ENDC}")
    print(chatter)
    print(f"{Colors.GREEN}{Colors.BOLD}-------------------------{Colors.ENDC}")
    pause()

def tui_decode():
    raw = get_multiline_input(f"\n{Colors.CYAN}[Decode] Paste the disguised chatter:{Colors.ENDC}")
    if not raw.strip(): return pause()
    
    password = getpass.getpass(f"Password: ")
    packed = chatter_to_packed(raw)
    
    if not packed:
        print(f"{Colors.FAIL}That doesn't look like a valid disguised message.{Colors.ENDC}")
        return pause()
        
    print(f"{Colors.DIM}Decrypting...{Colors.ENDC}")
    try:
        pt = decrypt_bytes(packed, password)
        img = unpack_image(pt)
        if img:
            out_name = input("Image detected! Enter filename to save (e.g., secret.png): ").strip()
            if not out_name: out_name = "decoded_image.png"
            with open(out_name, "wb") as f: f.write(img[1])
            print(f"{Colors.GREEN}[+] Decoded an image ({img[0]}). Saved to {out_name}{Colors.ENDC}")
        else:
            print(f"\n{Colors.GREEN}{Colors.BOLD}--- Revealed Secret ---{Colors.ENDC}")
            print(pt.decode('utf-8'))
            print(f"{Colors.GREEN}{Colors.BOLD}-----------------------{Colors.ENDC}")
    except ValueError:
        print(f"{Colors.FAIL}Wrong password or corrupted text.{Colors.ENDC}")
    pause()

def tui_stego_hide():
    cover_path = input(f"\n{Colors.CYAN}[Stego Hide] Enter path to cover image (PNG/JPG): {Colors.ENDC}").strip()
    if not os.path.exists(cover_path):
        print(f"{Colors.FAIL}File not found.{Colors.ENDC}")
        return pause()
        
    try:
        img = Image.open(cover_path).convert("RGBA")
    except Exception as e:
        print(f"{Colors.FAIL}Error loading cover image: {e}{Colors.ENDC}")
        return pause()
        
    img = flatten_image_data_to_opaque(img)
    
    payload_type = input("Hide Text (1) or Image (2)? [1]: ").strip()
    if payload_type == "2":
        secret_img_path = input("Enter path to secret image: ").strip()
        if not os.path.exists(secret_img_path):
            print(f"{Colors.FAIL}File not found.{Colors.ENDC}")
            return pause()
        with open(secret_img_path, 'rb') as f:
            data = f.read()
        ext = secret_img_path.split('.')[-1].lower()
        mime = f"image/{'jpeg' if ext in ['jpg', 'jpeg'] else 'png'}"
        payload = pack_image(mime, data)
        kind = 1
    else:
        secret = get_multiline_input("Enter secret text to hide:")
        payload = secret.encode('utf-8')
        kind = 0
        
    password = getpass.getpass(f"Password: ")
    out_path = input("Save disguised image as [hidden.png]: ").strip()
    if not out_path: out_path = "hidden.png"
    
    print(f"{Colors.DIM}Encrypting and Embedding...{Colors.ENDC}")
    packed = encrypt_bytes(payload, password)
    header = bytearray(STEGO_MAGIC)
    header.append(kind)
    header.extend(struct.pack('>I', len(packed)))
    full_payload = bytes(header) + packed
    
    capacity = (img.width * img.height * 3) // 8
    if len(full_payload) > capacity:
        print(f"{Colors.WARNING}[!] Payload too large, upscaling cover image to fit...{Colors.ENDC}")
        img = upscale_cover_to_fit(img, len(full_payload))
        capacity = (img.width * img.height * 3) // 8
        if len(full_payload) > capacity:
            print(f"{Colors.FAIL}Error: Payload too large even after maximum upscaling.{Colors.ENDC}")
            return pause()
            
    try:
        final_img = write_bits_into_image(img, full_payload)
        final_img.save(out_path, format="PNG")
        print(f"{Colors.GREEN}[+] Payload hidden successfully! Saved to {out_path}{Colors.ENDC}")
    except Exception as e:
        print(f"{Colors.FAIL}Error during embed: {e}{Colors.ENDC}")
    pause()

def tui_stego_reveal():
    img_path = input(f"\n{Colors.CYAN}[Stego Reveal] Enter path to image: {Colors.ENDC}").strip()
    if not os.path.exists(img_path):
        print(f"{Colors.FAIL}File not found.{Colors.ENDC}")
        return pause()
        
    try:
        img = Image.open(img_path).convert("RGBA")
    except Exception as e:
        print(f"{Colors.FAIL}Error loading image: {e}{Colors.ENDC}")
        return pause()
        
    password = getpass.getpass(f"Password: ")
    print(f"{Colors.DIM}Scanning and Decrypting...{Colors.ENDC}")
    
    raw = img.tobytes()
    capacity_rgb = (img.width * img.height * 3) // 8
    capacity_legacy = (img.width * img.height * 4) // 8
    
    is_legacy = False
    header = read_bits_from_image(raw, STEGO_HEADER_BYTES, False) if capacity_rgb >= STEGO_HEADER_BYTES else b''
    if header[:4] != STEGO_MAGIC:
        is_legacy = True
        header = read_bits_from_image(raw, STEGO_HEADER_BYTES, True) if capacity_legacy >= STEGO_HEADER_BYTES else b''
        if header[:4] != STEGO_MAGIC:
            print(f"{Colors.FAIL}Error: No hidden payload found in this image.{Colors.ENDC}")
            return pause()
            
    kind = header[4]
    length = struct.unpack('>I', header[5:9])[0]
    
    try:
        total_data = read_bits_from_image(raw, STEGO_HEADER_BYTES + length, is_legacy)
        packed = total_data[STEGO_HEADER_BYTES:]
        pt = decrypt_bytes(packed, password)
        
        if kind == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}--- Revealed Secret Text ---{Colors.ENDC}")
            print(pt.decode('utf-8'))
            print(f"{Colors.GREEN}{Colors.BOLD}----------------------------{Colors.ENDC}")
        else:
            img_data = unpack_image(pt)
            if not img_data:
                print(f"{Colors.FAIL}Error: Decoded bytes aren't a valid image.{Colors.ENDC}")
                return pause()
            out_name = input("Image revealed! Enter filename to save (e.g., secret.png): ").strip()
            if not out_name: out_name = "revealed_image.png"
            with open(out_name, "wb") as f: f.write(img_data[1])
            print(f"{Colors.GREEN}[+] Revealed an image ({img_data[0]}). Saved to {out_name}{Colors.ENDC}")
            
    except ValueError:
        print(f"{Colors.FAIL}Wrong password or corrupted payload.{Colors.ENDC}")
    pause()

def main_menu():
    while True:
        clear_screen()
        print_banner()
        print(f"1. {Colors.BOLD}Write{Colors.ENDC} (Text → Disguised Chatter)")
        print(f"2. {Colors.BOLD}Decode{Colors.ENDC} (Disguised Chatter → Text/Image)")
        print(f"3. {Colors.BOLD}Hide Stego{Colors.ENDC} (Text/Image → Inside Cover Image)")
        print(f"4. {Colors.BOLD}Reveal Stego{Colors.ENDC} (Cover Image → Secret Text/Image)")
        print(f"5. {Colors.FAIL}Exit{Colors.ENDC}")
        
        choice = input(f"\n{Colors.CYAN}Select an option [1-5]: {Colors.ENDC}").strip()
        if choice == '1': tui_write()
        elif choice == '2': tui_decode()
        elif choice == '3': tui_stego_hide()
        elif choice == '4': tui_stego_reveal()
        elif choice == '5': break
        else: print("Invalid choice.")

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}Exiting Veil...{Colors.ENDC}")
        sys.exit(0)