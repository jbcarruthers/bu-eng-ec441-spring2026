import marimo

__generated_with = "0.10.3"
app = marimo.App(width="medium")


@app.cell
def __():
    import marimo as mo
    import numpy as np
    import matplotlib.pyplot as plt
    return mo, np, plt


@app.cell
def __(mo):
    mo.md(
        r"""
        # Lecture 2: Information - Interactive Exploration

        **EC 441 - Introduction to Computer Networking**

        This notebook contains interactive demonstrations and experiments to explore the concepts from Lecture 2.
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ## Part 1: Shannon Entropy

        Entropy $H(p)$ for a Bernoulli random variable (binary outcome with probability $p$):

        $$H(p) = -p \log_2(p) - (1-p) \log_2(1-p)$$

        This represents the minimum number of bits needed to represent the outcome on average.
        """
    )
    return


@app.cell
def __(mo):
    # Interactive slider for probability
    p_slider = mo.ui.slider(
        start=0.0,
        stop=1.0,
        step=0.01,
        value=0.5,
        label="Probability p:",
        show_value=True
    )
    p_slider
    return (p_slider,)


@app.cell
def __(np, p_slider, plt):
    def entropy(p):
        """Calculate entropy H(p) for Bernoulli random variable."""
        result = np.zeros_like(p)
        mask = (p > 0) & (p < 1)
        p_valid = p[mask]
        result[mask] = -(p_valid * np.log2(p_valid) +
                         (1 - p_valid) * np.log2(1 - p_valid))
        return result

    # Full entropy curve
    p_range = np.linspace(0, 1, 1000)
    H_p = entropy(p_range)

    # Current point from slider
    p_current = p_slider.value
    H_current = entropy(np.array([p_current]))[0] if 0 < p_current < 1 else 0.0

    # Create plot
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(p_range, H_p, 'b-', linewidth=2, label='H(p)')
    ax.plot(p_current, H_current, 'ro', markersize=10,
            label=f'p={p_current:.2f}, H(p)={H_current:.4f} bits')
    ax.grid(True, alpha=0.3)
    ax.set_xlabel('p (probability)', fontsize=12)
    ax.set_ylabel('H(p) (bits)', fontsize=12)
    ax.set_title('Entropy of Bernoulli Random Variable', fontsize=13)
    ax.set_xlim(-0.05, 1.05)
    ax.set_ylim(-0.05, 1.1)
    ax.legend(loc='upper right', fontsize=10)
    plt.tight_layout()

    fig
    return H_current, H_p, ax, entropy, fig, p_current, p_range


@app.cell
def __(H_current, mo, p_current):
    mo.md(
        f"""
        **Current entropy:** $H({p_current:.2f}) = {H_current:.4f}$ bits

        **Interpretation:**
        - At $p = 0.5$: Maximum entropy (1 bit) - completely uncertain
        - At $p = {p_current:.2f}$: {H_current:.4f} bits needed on average
        - At $p = 0$ or $p = 1$: Zero entropy - completely certain
        """
    )
    return


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Part 2: Text Encoding Experiments

        ### UTF-8 Encoding Analysis
        """
    )
    return


@app.cell
def __(mo):
    # Text input for encoding analysis
    text_input = mo.ui.text_area(
        value="Hello, World! 你好世界",
        label="Enter text to analyze:",
        rows=3
    )
    text_input
    return (text_input,)


@app.cell
def __(mo, text_input):
    text = text_input.value

    # Analyze UTF-8 encoding
    utf8_bytes = text.encode('utf-8')
    utf16_bytes = text.encode('utf-16')
    ascii_ok = all(ord(c) < 128 for c in text)

    # Character breakdown
    char_info = []
    for _char in text:
        utf8_len = len(_char.encode('utf-8'))
        codepoint = ord(_char)
        char_info.append({
            'char': _char,
            'codepoint': f'U+{codepoint:04X}',
            'utf8_bytes': utf8_len,
            'hex': _char.encode('utf-8').hex().upper()
        })

    # Create results table
    table_data = {
        'Character': [c['char'] for c in char_info],
        'Code Point': [c['codepoint'] for c in char_info],
        'UTF-8 Bytes': [c['utf8_bytes'] for c in char_info],
        'UTF-8 Hex': [c['hex'] for c in char_info]
    }

    results = mo.md(
        f"""
        ### Encoding Analysis Results

        **Input text:** `{text}`

        **Sizes:**
        - UTF-8: {len(utf8_bytes)} bytes
        - UTF-16: {len(utf16_bytes)} bytes
        - ASCII compatible: {'Yes' if ascii_ok else 'No'}

        **Character breakdown:**
        """
    )

    table = mo.ui.table(table_data)

    mo.vstack([results, table])
    return (
        ascii_ok,
        char_info,
        codepoint,
        results,
        table,
        table_data,
        text,
        utf16_bytes,
        utf8_bytes,
        utf8_len,
    )


@app.cell
def __(mo, text):
    # Base64 encoding demonstration
    import base64

    base64_encoded = base64.b64encode(text.encode('utf-8')).decode('ascii')
    base64_size = len(base64_encoded)
    original_size = len(text.encode('utf-8'))
    overhead = (base64_size / original_size - 1) * 100 if original_size > 0 else 0

    mo.md(
        f"""
        ### Base64 Encoding

        **Original (UTF-8):** {original_size} bytes
        **Base64 encoded:** {base64_size} bytes
        **Overhead:** {overhead:.1f}%

        ```
        {base64_encoded}
        ```

        Base64 encodes 3 bytes into 4 characters (6 bits each), resulting in ~33% overhead.
        """
    )
    return base64, base64_encoded, base64_size, original_size, overhead


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Part 3: Multimedia Data Rate Calculator

        ### Audio Data Rates
        """
    )
    return


@app.cell
def __(mo):
    # Audio parameters
    audio_sample_rate = mo.ui.slider(8000, 192000, value=44100, step=100,
                                      label="Sample rate (Hz):", show_value=True)
    audio_bit_depth = mo.ui.dropdown(["8", "16", "24", "32"], value="16",
                                      label="Bit depth:")
    audio_channels = mo.ui.dropdown(["1 (mono)", "2 (stereo)"], value="2 (stereo)",
                                     label="Channels:")

    mo.vstack([
        audio_sample_rate,
        audio_bit_depth,
        audio_channels
    ])
    return audio_bit_depth, audio_channels, audio_sample_rate


@app.cell
def __(audio_bit_depth, audio_channels, audio_sample_rate, mo):
    # Calculate audio data rate
    sample_rate = audio_sample_rate.value
    bit_depth = int(audio_bit_depth.value)
    channels = 1 if "mono" in audio_channels.value else 2

    bits_per_second = sample_rate * bit_depth * channels
    bytes_per_second = bits_per_second / 8
    mb_per_second = bits_per_second / 1_000_000
    mb_per_minute = bytes_per_second * 60 / 1_000_000

    # Compare to standards
    is_cd_quality = (sample_rate == 44100 and bit_depth == 16 and channels == 2)
    is_telephone = (sample_rate == 8000 and bit_depth == 8 and channels == 1)

    standard_text = ""
    if is_cd_quality:
        standard_text = "**This is CD quality audio!**"
    elif is_telephone:
        standard_text = "**This is telephone quality audio.**"

    mo.md(
        f"""
        ### Audio Data Rate Results

        **Configuration:**
        - Sample rate: {sample_rate:,} Hz
        - Bit depth: {bit_depth} bits
        - Channels: {channels}

        **Uncompressed data rate:**
        - {bits_per_second:,} bits/sec = **{mb_per_second:.2f} Mb/s**
        - {mb_per_minute:.1f} MB per minute

        {standard_text}

        **With compression:**
        - MP3 (128 kb/s): {128 / mb_per_second:.1f}× compression
        - MP3 (320 kb/s): {320 / mb_per_second:.1f}× compression
        """
    )
    return (
        bit_depth,
        bits_per_second,
        bytes_per_second,
        channels,
        is_cd_quality,
        is_telephone,
        mb_per_minute,
        mb_per_second,
        sample_rate,
        standard_text,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ### Video Data Rates
        """
    )
    return


@app.cell
def __(mo):
    # Video parameters
    video_resolution = mo.ui.dropdown(
        ["854×480 (480p)", "1280×720 (720p)", "1920×1080 (1080p)",
         "2560×1440 (1440p)", "3840×2160 (4K)"],
        value="1920×1080 (1080p)",
        label="Resolution:"
    )
    video_fps = mo.ui.slider(24, 120, value=30, step=1,
                              label="Frame rate (fps):", show_value=True)
    video_bpp = mo.ui.dropdown(["3 (RGB)", "4 (RGBA)"], value="3 (RGB)",
                                label="Bytes per pixel:")

    mo.vstack([
        video_resolution,
        video_fps,
        video_bpp
    ])
    return video_bpp, video_fps, video_resolution


@app.cell
def __(mo, video_bpp, video_fps, video_resolution):
    # Parse resolution
    resolution_map = {
        "854×480 (480p)": (854, 480),
        "1280×720 (720p)": (1280, 720),
        "1920×1080 (1080p)": (1920, 1080),
        "2560×1440 (1440p)": (2560, 1440),
        "3840×2160 (4K)": (3840, 2160)
    }

    width, height = resolution_map[video_resolution.value]
    fps = video_fps.value
    bytes_per_pixel = int(video_bpp.value.split()[0])

    # Calculate uncompressed data rate
    pixels_per_frame = width * height
    bytes_per_frame = pixels_per_frame * bytes_per_pixel
    mb_per_frame = bytes_per_frame / 1_000_000

    bytes_per_sec_video = bytes_per_frame * fps
    mb_per_sec_video = bytes_per_sec_video / 1_000_000
    gb_per_sec = mb_per_sec_video / 1000
    bits_per_sec_video = bytes_per_sec_video * 8
    gb_per_sec_bits = bits_per_sec_video / 1_000_000_000

    # Compressed estimates
    h264_bitrate_low = 3  # Mb/s for 1080p
    h264_bitrate_high = 10  # Mb/s for 1080p
    compression_ratio_low = bits_per_sec_video / (h264_bitrate_low * 1_000_000)
    compression_ratio_high = bits_per_sec_video / (h264_bitrate_high * 1_000_000)

    mo.md(
        f"""
        ### Video Data Rate Results

        **Configuration:**
        - Resolution: {width}×{height} ({pixels_per_frame:,} pixels)
        - Frame rate: {fps} fps
        - Bytes per pixel: {bytes_per_pixel}

        **Uncompressed data rate:**
        - {mb_per_frame:.2f} MB per frame
        - {mb_per_sec_video:.1f} MB/s = **{gb_per_sec_bits:.2f} Gb/s**
        - This is **completely impractical** for transmission or storage!

        **With H.264 compression (estimated):**
        - Low quality (3 Mb/s): {compression_ratio_low:.0f}× compression
        - High quality (10 Mb/s): {compression_ratio_high:.0f}× compression

        **Typical compressed rates for this resolution:**
        - YouTube: 3-5 Mb/s (for 1080p)
        - Netflix: 5-8 Mb/s (for 1080p HD)
        - Blu-ray: 20-40 Mb/s (for 1080p)
        """
    )
    return (
        bits_per_sec_video,
        bytes_per_frame,
        bytes_per_pixel,
        bytes_per_sec_video,
        compression_ratio_high,
        compression_ratio_low,
        fps,
        gb_per_sec,
        gb_per_sec_bits,
        h264_bitrate_high,
        h264_bitrate_low,
        height,
        mb_per_frame,
        mb_per_sec_video,
        pixels_per_frame,
        resolution_map,
        width,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Part 4: File Format Exploration

        ### Hex Dump Viewer

        This demonstrates how to view the raw bytes of a file, including magic numbers.
        """
    )
    return


@app.cell
def __(mo):
    # File content input
    hex_input = mo.ui.text_area(
        value="89 50 4E 47 0D 0A 1A 0A",
        label="Enter hex bytes (space-separated):",
        rows=2
    )
    hex_input
    return (hex_input,)


@app.cell
def __(hex_input, mo):
    # Parse hex input
    try:
        hex_str = hex_input.value.replace(" ", "")
        if len(hex_str) % 2 != 0:
            hex_str = "0" + hex_str

        byte_values = [int(hex_str[i:i+2], 16) for i in range(0, len(hex_str), 2)]

        # Common magic numbers
        magic_numbers = {
            "89504E470D0A1A0A": "PNG image",
            "FFD8FF": "JPEG image",
            "47494638": "GIF image",
            "25504446": "PDF document",
            "504B0304": "ZIP archive",
            "7F454C46": "ELF executable"
        }

        # Check for matches
        hex_prefix = hex_str[:16].upper()
        detected_format = "Unknown"
        for magic, format_name in magic_numbers.items():
            if hex_prefix.startswith(magic):
                detected_format = format_name
                break

        # Create ASCII representation
        ascii_repr = ""
        for byte in byte_values:
            if 32 <= byte < 127:
                ascii_repr += chr(byte)
            else:
                ascii_repr += "."

        result = mo.md(
            f"""
            ### Hex Dump Analysis

            **Bytes:** `{' '.join(f'{b:02X}' for b in byte_values)}`

            **ASCII representation:** `{ascii_repr}`

            **Detected format:** **{detected_format}**

            **Common file signatures:**
            - PNG: `89 50 4E 47 0D 0A 1A 0A` (.PNG....)
            - JPEG: `FF D8 FF` (ÿØÿ)
            - GIF: `47 49 46 38` (GIF8)
            - PDF: `25 50 44 46` (%PDF)
            - ZIP: `50 4B 03 04` (PK..)
            - ELF: `7F 45 4C 46` (.ELF)
            """
        )
    except Exception as e:
        result = mo.md(f"**Error parsing hex input:** {str(e)}")

    result
    return (
        ascii_repr,
        byte_values,
        detected_format,
        hex_prefix,
        hex_str,
        magic_numbers,
        result,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Part 5: Data vs. Information

        ### Compression Ratio Explorer

        This demonstrates the relationship between data size and information content.
        """
    )
    return


@app.cell
def __(mo):
    # Text for compression analysis
    compression_text = mo.ui.text_area(
        value="the the the the the",
        label="Enter text to analyze compression potential:",
        rows=3
    )
    compression_text
    return (compression_text,)


@app.cell
def __(compression_text, mo):
    import zlib
    from collections import Counter

    text_to_compress = compression_text.value

    # Original size
    original_bytes = len(text_to_compress.encode('utf-8'))

    # Compressed size
    compressed = zlib.compress(text_to_compress.encode('utf-8'))
    compressed_size = len(compressed)

    # Calculate character frequency (for entropy estimation)
    char_counts = Counter(text_to_compress)
    total_chars = len(text_to_compress)

    # Estimate entropy
    estimated_entropy = 0
    for _char, _count in char_counts.items():
        p = _count / total_chars
        if p > 0:
            estimated_entropy -= p * (np.log2(p) if p > 0 else 0)

    # Theoretical minimum
    theoretical_min_bits = estimated_entropy * total_chars
    theoretical_min_bytes = theoretical_min_bits / 8

    compression_ratio = original_bytes / compressed_size if compressed_size > 0 else 0
    efficiency = (theoretical_min_bytes / original_bytes * 100) if original_bytes > 0 else 0

    mo.md(
        f"""
        ### Compression Analysis

        **Original text:** {len(text_to_compress)} characters

        **Sizes:**
        - Original (UTF-8): {original_bytes} bytes
        - Compressed (zlib): {compressed_size} bytes
        - Compression ratio: {compression_ratio:.2f}×

        **Information theory:**
        - Estimated entropy: {estimated_entropy:.3f} bits/character
        - Theoretical minimum: {theoretical_min_bytes:.1f} bytes ({theoretical_min_bits:.1f} bits)
        - Encoding efficiency: {efficiency:.1f}%

        **Character frequencies:**
        {dict(char_counts.most_common(10))}

        **Observations:**
        - Repetitive text compresses better (lower entropy)
        - Random text compresses poorly (higher entropy)
        - ASCII encoding uses 8 bits/char, but English text has ~1.5 bits/char of entropy
        """
    )
    return (
        Counter,
        char_counts,
        compressed,
        compressed_size,
        compression_ratio,
        efficiency,
        estimated_entropy,
        original_bytes,
        p,
        text_to_compress,
        theoretical_min_bits,
        theoretical_min_bytes,
        total_chars,
        zlib,
    )


@app.cell
def __(mo):
    mo.md(
        r"""
        ---

        ## Summary

        This notebook demonstrated:

        1. **Entropy visualization** - Interactive exploration of $H(p)$
        2. **Text encoding** - UTF-8, UTF-16, Base64 analysis
        3. **Multimedia data rates** - Audio and video calculations
        4. **File formats** - Magic number detection
        5. **Compression** - Relationship between data size and information content

        **Key Insight:** Information content (entropy) sets the theoretical minimum for data representation,
        but practical encodings trade efficiency for other properties (readability, error tolerance, etc.).
        """
    )
    return


if __name__ == "__main__":
    app.run()
