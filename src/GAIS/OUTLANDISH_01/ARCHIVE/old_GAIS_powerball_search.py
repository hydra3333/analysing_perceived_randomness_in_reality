import os
import time
import itertools
from collections import defaultdict
import ahocorasick

# -------------------------------------------------------------
# Configuration & Sample Data
# -------------------------------------------------------------
# Each draw is: (draw_number, [main_1, ..., main_7], powerball)
# The order of main numbers reflects extraction order.
SAMPLE_POWERBALL_DRAWS = [
    (1440, [10, 24, 18, 4, 31, 14, 2], 12),
    (1441, [32, 11, 29, 6, 21, 15, 8], 5),
    (1442, [3, 27, 19, 14, 35, 8, 22], 17),
    (1443, [12, 17, 1, 33, 9, 25, 4], 9),
    (1444, [16, 22, 34, 7, 28, 11, 3], 14),
    (1445, [29, 2, 15, 31, 8, 20, 13], 1),
    (1446, [5, 18, 24, 33, 12, 27, 7], 19),
    (1447, [21, 14, 3, 30, 9, 26, 16], 8),
    (1448, [35, 11, 4, 17, 23, 2, 19], 10),
    (1449, [8, 25, 13, 32, 6, 28, 1], 15),
    (1450, [18, 7, 29, 12, 34, 22, 5], 3),
]


def ball_to_digits_str(num: int) -> str:
    """Converts a ball number (e.g. 7 or 24) to a 2-character string ('07' or '24')."""
    return f"{num:02d}"


def balls_to_str(balls) -> str:
    """Converts a sequence of balls to contiguous 2-digit characters."""
    return "".join(ball_to_digits_str(b) for b in balls)


# -------------------------------------------------------------
# 4.1 Preparation: Pattern Generation & Automaton Building
# -------------------------------------------------------------
def build_winning_patterns(draws, any_order_div3=True):
    """
    Builds the consolidated P_win_set into a pyahocorasick Automaton.
    Handles p1 (Div 1), p2 (Div 2), and p3 (Div 3).
    """
    print(f"Generating winning patterns for {len(draws)} draws...")
    t0 = time.time()

    # Store in dict to handle pattern collisions between different draws:
    # pattern_str -> list of (draw_index, div_id)
    pattern_map = defaultdict(list)
    total_patterns_created = 0

    for draw_idx, (draw_num, main_balls, pb) in enumerate(draws):
        pb_str = ball_to_digits_str(pb)

        # (p1) Div 1: 7 winning numbers drawn in order + Powerball (16 chars)
        p1 = balls_to_str(main_balls) + pb_str
        pattern_map[p1].append((draw_idx, 1))
        total_patterns_created += 1

        # (p2) Div 2: 7 winning numbers drawn in order (14 chars)
        p2 = balls_to_str(main_balls)
        pattern_map[p2].append((draw_idx, 2))
        total_patterns_created += 1

        # (p3) Div 3: Any 6 main numbers + Powerball
        if any_order_div3:
            # 7 combinations * 6! permutations = 5,040 patterns per draw
            for combo in itertools.combinations(main_balls, 6):
                for perm in itertools.permutations(combo):
                    p3 = balls_to_str(perm) + pb_str
                    pattern_map[p3].append((draw_idx, 3))
                    total_patterns_created += 1
        else:
            for combo in itertools.combinations(main_balls, 6):
                p3 = balls_to_str(combo) + pb_str
                pattern_map[p3].append((draw_idx, 3))
                total_patterns_created += 1

    gen_time = time.time() - t0
    print(f"Generated {total_patterns_created:,} total patterns ({len(pattern_map):,} unique keys) in {gen_time:.3f}s")

    # Compile pyahocorasick trie
    t_compile = time.time()
    print("Compiling Aho-Corasick Automaton into memory...")
    automaton = ahocorasick.Automaton()
    for pat_str, draw_div_list in pattern_map.items():
        automaton.add_word(pat_str, draw_div_list)

    automaton.make_automaton()
    compile_time = time.time() - t_compile
    print(f"Automaton compiled in {compile_time:.3f}s\n")

    return automaton, gen_time + compile_time


# -------------------------------------------------------------
# 4.2 & 4.3: Single-Pass Scan of Digit File
# -------------------------------------------------------------
def scan_digit_stream(bin_file_path, automaton, max_bytes=1_000_000):
    if not os.path.exists(bin_file_path):
        print(f"Error: Could not find '{bin_file_path}'")
        return None, 0.0

    print(f"Loading '{bin_file_path}' ({max_bytes:,} bytes) into memory...")
    with open(bin_file_path, "rb") as f:
        stream_bytes = f.read(max_bytes)

    # Fast 1:1 translation from bytes 0x00..0x09 to ASCII chars '0'..'9'
    table = bytes.maketrans(bytes(range(10)), b"0123456789")
    stream_str = stream_bytes.translate(table).decode("ascii")

    print(f"Scanning stream in one single sequential pass...")
    t0 = time.time()

    # occurrences[draw_idx][div_id] = list of match byte positions
    occurrences = defaultdict(lambda: defaultdict(list))
    match_count = 0

    # Single pass search
    for end_idx, draw_div_list in automaton.iter(stream_str):
        for draw_idx, div_id in draw_div_list:
            occurrences[draw_idx][div_id].append(end_idx)
            match_count += 1

    scan_time = time.time() - t0
    print(f"Scan complete in {scan_time:.4f}s ({len(stream_bytes) / scan_time / 1e6:.1f} MB/s throughput)")
    print(f"Total matches found: {match_count:,}")
    return occurrences, scan_time


# -------------------------------------------------------------
# 4.4 Correlation: Draw W vs Draw W+1 Analysis
# -------------------------------------------------------------
def analyze_draw_correlations(draws, occurrences):
    print("\n" + "=" * 60)
    print("            DRAW CORRELATION ANALYSIS (W -> W+1)")
    print("=" * 60)

    total_w_with_div1 = 0
    total_w_with_any_win = 0
    transition_successes = 0

    for w in range(len(draws) - 1):
        draw_w_num = draws[w][0]
        draw_next_num = draws[w + 1][0]

        w_div1 = occurrences[w][1]
        w_div2 = occurrences[w][2]
        w_div3 = occurrences[w][3]
        w_has_any = (len(w_div1) + len(w_div2) + len(w_div3)) > 0

        if w_has_any:
            total_w_with_any_win += 1

        next_div1 = occurrences[w + 1][1]
        next_div2 = occurrences[w + 1][2]
        next_div3 = occurrences[w + 1][3]
        next_total = len(next_div1) + len(next_div2) + len(next_div3)

        # Check for Div 1 specifically as requested in 4.4
        if len(w_div1) > 0:
            total_w_with_div1 += 1
            print(f"\n[!] Draw W={draw_w_num} matched Div1 at positions: {w_div1}")
            print(f"    -> Checking Draw W+1={draw_next_num} wins:")
            print(f"       Div 1: {len(next_div1)} hits {next_div1}")
            print(f"       Div 2: {len(next_div2)} hits {next_div2}")
            print(f"       Div 3: {len(next_div3)} hits {next_div3}")
            if next_total > 0:
                transition_successes += 1
        else:
            if w_has_any and next_total > 0:
                print(f"Draw {draw_w_num} (has wins) -> Draw {draw_next_num} also has wins (Div3: {len(next_div3)})")

    print("\n--- Summary Statistics ---")
    print(f"Total draws evaluated: {len(draws)}")
    print(f"Draws with at least one win found in stream: {total_w_with_any_win}")
    print(f"Draws with Div 1 match: {total_w_with_div1}")
    print(f"Draw W (Div1) followed by any Draw W+1 win: {transition_successes}")
    print("=" * 60 + "\n")


# -------------------------------------------------------------
# Main Execution
# -------------------------------------------------------------
if __name__ == "__main__":
    # 1. Build patterns
    automaton, prep_time = build_winning_patterns(SAMPLE_POWERBALL_DRAWS, any_order_div3=True)

    # 2. Test against Pi
    print(">>> EXPERIMENT 1: Scanning digits_pi_10_to_6.bin <<<")
    occ_pi, time_pi = scan_digit_stream("digits_pi_10_to_6.bin", automaton, max_bytes=1_000_000)
    if occ_pi is not None:
        analyze_draw_correlations(SAMPLE_POWERBALL_DRAWS, occ_pi)

    # 3. Test against Golden Ratio
    print(">>> EXPERIMENT 2: Scanning digits_golden_ratio_10_to_6.bin <<<")
    occ_phi, time_phi = scan_digit_stream("digits_golden_ratio_10_to_6.bin", automaton, max_bytes=1_000_000)
    if occ_phi is not None:
        analyze_draw_correlations(SAMPLE_POWERBALL_DRAWS, occ_phi)

    # 4. Linear Projection Benchmark Report
    print("--- 3900X TIMING & PROJECTION BENCHMARK ---")
    print(f"Preparation / Automaton Build Time: {prep_time:.2f}s (fixed one-off)")
    print(f"Scan Time for T = 1,000,000 digits: {time_pi:.4f}s")
    print(
        f"Linear Projected Scan Time for M = 10^9 digits: {time_pi * 1000:.2f}s (~{(time_pi * 1000) / 60:.1f} minutes)"
    )
