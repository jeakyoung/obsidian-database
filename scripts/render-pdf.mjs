// 빌드 시점에 경력 서류(02_Career) 4개 문서를 실제 PDF 파일로 렌더링한다.
// deploy.yml 이 `npx quartz build` 로 만든 quartz-build/public 을 로컬 정적
// 서버로 띄우고, Puppeteer(headless Chrome)로 각 페이지를 print 미디어로
// 렌더링해 quartz-build/public/pdfs/*.pdf 로 저장한다.
// PdfButton 컴포넌트는 이 경로(/pdfs/<파일명>.pdf)를 그대로 링크한다 —
// 두 쪽의 파일명이 어긋나면 다운로드 링크가 깨지므로 세트로 관리할 것.
import http from "node:http"
import fs from "node:fs"
import path from "node:path"
import puppeteer from "puppeteer"

const PUBLIC_DIR = path.resolve("public")
const OUT_DIR = path.join(PUBLIC_DIR, "pdfs")
const PORT = 8123

const PAGES = [
  "02_Career/01_Resume.html",
  "02_Career/02_CareerDescription.html",
  "02_Career/03_CoverLetter.html",
  "02_Career/04_Portfolio.html",
]

const MIME = {
  ".html": "text/html; charset=utf-8",
  ".css": "text/css; charset=utf-8",
  ".js": "application/javascript",
  ".json": "application/json",
  ".png": "image/png",
  ".jpg": "image/jpeg",
  ".jpeg": "image/jpeg",
  ".svg": "image/svg+xml",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".ico": "image/x-icon",
  ".xml": "application/xml",
  ".txt": "text/plain; charset=utf-8",
}

function startServer() {
  const server = http.createServer((req, res) => {
    const reqPath = decodeURIComponent(req.url.split("?")[0])
    let filePath = path.join(PUBLIC_DIR, reqPath)
    if (reqPath.endsWith("/")) filePath = path.join(filePath, "index.html")
    if (!fs.existsSync(filePath) && fs.existsSync(filePath + ".html")) filePath += ".html"
    if (!fs.existsSync(filePath)) {
      res.writeHead(404)
      res.end("Not found: " + reqPath)
      return
    }
    const ext = path.extname(filePath)
    res.writeHead(200, { "Content-Type": MIME[ext] ?? "application/octet-stream" })
    fs.createReadStream(filePath).pipe(res)
  })
  return new Promise((resolve) => server.listen(PORT, () => resolve(server)))
}

async function main() {
  fs.mkdirSync(OUT_DIR, { recursive: true })
  const server = await startServer()
  const browser = await puppeteer.launch({ headless: "new" })

  try {
    for (const rel of PAGES) {
      const page = await browser.newPage()
      await page.goto(`http://localhost:${PORT}/${rel}`, { waitUntil: "networkidle0" })
      await page.emulateMediaType("print")
      const outName = path.basename(rel, ".html") + ".pdf"
      const outPath = path.join(OUT_DIR, outName)
      await page.pdf({
        path: outPath,
        format: "A4",
        printBackground: true,
        margin: { top: "18mm", bottom: "18mm", left: "16mm", right: "16mm" },
      })
      console.log(`rendered ${rel} -> pdfs/${outName}`)
      await page.close()
    }
  } finally {
    await browser.close()
    server.close()
  }
}

main().catch((err) => {
  console.error(err)
  process.exit(1)
})
