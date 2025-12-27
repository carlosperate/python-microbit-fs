# JavaScript for the original microbit-fs library

## Version

Commit: f63b5f9c21531ee09c84a5903926bc8ba58f57d2
tag: v0.10.0

## How to build the JS file

```bash
git clone https://github.com/microbit-foundation/microbit-fs.git
cd microbit-fs
npm install
npm run build
npx esbuild src/index.ts --bundle --outfile=microbit-fs.js --format=iife --global-name=microbitFs
```
