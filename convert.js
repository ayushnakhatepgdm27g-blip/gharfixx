const fs = require('fs');
const path = require('path');

const htmlPath = path.join(__dirname, 'index.html');
const appTsxPath = path.join(__dirname, 'src', 'App.tsx');

let html = fs.readFileSync(htmlPath, 'utf8');

const bodyMatch = html.match(/<body[^>]*>([\s\S]*)<\/body>/i);
let bodyContent = bodyMatch ? bodyMatch[1] : html;

// Convert attributes
let jsx = bodyContent.replace(/class="/g, 'className="');
jsx = jsx.replace(/style="font-size: 12px;"/g, 'style={{ fontSize: "12px" }}');
jsx = jsx.replace(/style="font-size: 16px;"/g, 'style={{ fontSize: "16px" }}');
jsx = jsx.replace(/style="font-variation-settings: 'FILL' 1, 'wght' 400, 'GRAD' 0, 'opsz' 24;"/g, 'style={{ fontVariationSettings: "\'FILL\' 1, \'wght\' 400, \'GRAD\' 0, \'opsz\' 24" }}');

// Fix unclosed tags
jsx = jsx.replace(/(<img[^>]*?)(?<!\/)>/g, '$1 />');
jsx = jsx.replace(/(<br[^>]*?)(?<!\/)>/g, '$1 />');
jsx = jsx.replace(/(<hr[^>]*?)(?<!\/)>/g, '$1 />');
jsx = jsx.replace(/(<input[^>]*?)(?<!\/)>/g, '$1 />');

const appTsx = `import React from 'react';

export default function App() {
  return (
    <div className="antialiased min-h-screen flex flex-col font-body-md bg-surface-container-high text-primary-container">
      ${jsx}
    </div>
  );
}
`;

fs.writeFileSync(appTsxPath, appTsx, 'utf8');
console.log('Done!');
