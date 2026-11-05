import sys
import time
import math
import urllib.request

# Allow Python to convert large multi-digit integers to strings
sys.set_int_max_str_digits(0)

def generate_golden_ratio_bin(filename="digits_golden_ratio_10_to_6.bin", total_digits=1_000_000):
    print(f"Generating {total_digits:,} digits of Golden Ratio (including leading '1')...")
    t0 = time.time()
    
    # We want 1 leading digit ('1') + (total_digits - 1) decimal fractional digits
    frac_digits = total_digits - 1
    
    # Golden Ratio = (1 + sqrt(5)) / 2
    # Compute integer sqrt of 5 * 10^(2 * frac_digits)
    scale = 10 ** (2 * frac_digits)
    target = 5 * scale
    
    # Fast integer square root
    x = math.isqrt(target)
    phi_int = (10 ** frac_digits + x) // 2
    
    # phi_int starts with '1', followed by the fractional digits
    phi_str = str(phi_int)[:total_digits]
    raw_bytes = bytes([ord(c) - 48 for c in phi_str])
    
    with open(filename, "wb") as f:
        f.write(raw_bytes)
        
    print(f"-> Saved {filename} ({len(raw_bytes):,} bytes) in {time.time()-t0:.2f} seconds")

def generate_pi_bin(filename="digits_pi_10_to_6.bin", total_digits=1_000_000):
    print(f"Fetching {total_digits:,} digits of Pi (including leading '3')...")
    t0 = time.time()
    
    # Fetch digits from standard public repository
    url = "https://stuff.mit.edu/afs/sipb/contrib/pi/pi-billion.txt"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    
    # Read extra buffer to account for possible formatting/decimal points
    with urllib.request.urlopen(req) as response:
        data = response.read(total_digits + 50)
        
    # Extract numeric digits (including the leading '3')
    pi_digits = [b - 48 for b in data if 48 <= b <= 57][:total_digits]
    raw_bytes = bytes(pi_digits)
    
    with open(filename, "wb") as f:
        f.write(raw_bytes)
        
    print(f"-> Saved {filename} ({len(raw_bytes):,} bytes) in {time.time()-t0:.2f} seconds")

if __name__ == "__main__":
    generate_golden_ratio_bin()
    generate_pi_bin()
    print("\nFiles are ready!")