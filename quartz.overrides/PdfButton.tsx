// 경력 서류(02_Career, frontmatter type: 경력문서) 페이지에만 노출되는
// "PDF로 저장" 버튼. 빌드 시점에 scripts/render-pdf.mjs(Puppeteer)가 이
// 페이지들을 /pdfs/<파일명>.pdf 로 미리 렌더링해 두고, 이 버튼은 그 정적
// 파일을 바로 다운로드하는 링크일 뿐이다 — 클릭 시 대화상자 없이 바로
// 저장된다. 파일명은 render-pdf.mjs 의 출력 파일명과 반드시 맞아야 한다
// (slug 마지막 세그먼트 + ".pdf").
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import { pathToRoot, joinSegments } from "../util/path"
import { classNames } from "../util/lang"

const PdfButton: QuartzComponent = ({ fileData, displayClass }: QuartzComponentProps) => {
  if (fileData.frontmatter?.type !== "경력문서") return null
  const slug = fileData.slug!
  const fileName = slug.split("/").pop()
  const href = joinSegments(pathToRoot(slug), "pdfs", `${fileName}.pdf`)
  return (
    <a
      class={classNames(displayClass, "pdf-export-button")}
      href={href}
      download
      aria-label="PDF로 저장"
    >
      📄 PDF로 저장
    </a>
  )
}

export default (() => PdfButton) satisfies QuartzComponentConstructor
