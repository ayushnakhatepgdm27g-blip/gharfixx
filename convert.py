import re

with open('c:\\Users\\ASUS\\Downloads\\villa-banner-layouts\\index.html', 'r', encoding='utf-8') as f:
    html = f.read()

body_match = re.search(r'<body[^>]*>(.*)</body>', html, re.DOTALL | re.IGNORECASE)
body_content = body_match.group(1) if body_match else html

jsx = body_content.replace('class="', 'className="')
jsx = jsx.replace('style="font-size: 12px;"', 'style={{ fontSize: "12px" }}')
jsx = jsx.replace('style="font-size: 16px;"', 'style={{ fontSize: "16px" }}')
jsx = jsx.replace('style="font-variation-settings: \'FILL\' 1, \'wght\' 400, \'GRAD\' 0, \'opsz\' 24;"', 'style={{ fontVariationSettings: "\'FILL\' 1, \'wght\' 400, \'GRAD\' 0, \'opsz\' 24" }}')

jsx = re.sub(r'(<img[^>]*?)(?<!/)>', r'\1 />', jsx)
jsx = re.sub(r'(<br[^>]*?)(?<!/)>', r'\1 />', jsx)
jsx = re.sub(r'(<hr[^>]*?)(?<!/)>', r'\1 />', jsx)
jsx = re.sub(r'(<input[^>]*?)(?<!/)>', r'\1 />', jsx)

app_tsx = f"""import React from 'react';

export default function App() {{
  return (
    <div className="antialiased min-h-screen flex flex-col font-body-md bg-surface-container-high text-primary-container">
      {jsx}
    </div>
  );
}}
"""

with open('c:\\Users\\ASUS\\Downloads\\villa-banner-layouts\\src\\App.tsx', 'w', encoding='utf-8') as f:
    f.write(app_tsx)
print('Done!')
