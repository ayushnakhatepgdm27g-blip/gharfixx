import os

stitch_path = r'c:\Users\ASUS\Downloads\villa-banner-layouts\stitch_website.html'
ezgif_path = r'c:\Users\ASUS\Downloads\ezgif-21e22e8581b8c639-jpg\index.html'
out_path = r'c:\Users\ASUS\Downloads\ezgif-21e22e8581b8c639-jpg\combined_website.html'

with open(stitch_path, 'r', encoding='utf-8') as f:
    stitch = f.read()

with open(ezgif_path, 'r', encoding='utf-8') as f:
    ezgif = f.read()

# Extract parts from stitch
import re
tailwind_config = re.search(r'(<script id="tailwind-config">.*?</script>)', stitch, re.DOTALL).group(1)
fonts = re.findall(r'<link href="https://fonts.googleapis.com[^>]+>', stitch)

# Extract body contents from stitch (excluding scripts at the end if any)
body_match = re.search(r'<body[^>]*>(.*?)</body>', stitch, re.DOTALL | re.IGNORECASE)
stitch_body = body_match.group(1)

# Extract head from ezgif
ezgif_head = re.search(r'<head>(.*?)</head>', ezgif, re.DOTALL | re.IGNORECASE).group(1)
# Add tailwind config and fonts to ezgif head
new_head = ezgif_head.replace('</title>', '</title>\n' + '\n'.join(fonts) + '\n' + tailwind_config)
# Remove the ezgif tailwind cdn script so we don't have duplicates, tailwind config is already bringing one maybe? Wait, stitch has:
# <script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>
# ezgif has: <script src="https://cdn.tailwindcss.com"></script>
# We should use the stitch one.
new_head = re.sub(r'<script src="https://cdn.tailwindcss.com"></script>', '', new_head)
stitch_cdn = '<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>'
new_head = new_head.replace(tailwind_config, stitch_cdn + '\n' + tailwind_config)

# Now, we need to inject the stitch_body into ezgif body.
# We will wrap stitch_body in a div with the classes from stitch body.
# stitch body class: "antialiased min-h-screen flex flex-col font-body-md bg-surface-container-high text-primary-container"
stitch_wrapper = f"""
<!-- STITCH CONTENT START -->
<div class="antialiased flex flex-col font-body-md bg-surface-container-high text-primary-container relative z-20 w-full bg-opacity-100">
{stitch_body}
</div>
<!-- STITCH CONTENT END -->
"""

# Find where to insert in ezgif: right before the <script> tag for the canvas.
# Or right after <div class="h-[50vh]"></div> </div>
ezgif_body = re.search(r'<body[^>]*>(.*?)</body>', ezgif, re.DOTALL | re.IGNORECASE).group(1)

insert_pos = ezgif_body.rfind('<script>')
if insert_pos != -1:
    new_ezgif_body = ezgif_body[:insert_pos] + stitch_wrapper + ezgif_body[insert_pos:]
else:
    new_ezgif_body = ezgif_body + stitch_wrapper

new_html = f"""<!DOCTYPE html>
<html class="scroll-smooth" lang="en">
<head>
{new_head}
</head>
<body>
{new_ezgif_body}
</body>
</html>
"""

with open(out_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Combined successfully!")
