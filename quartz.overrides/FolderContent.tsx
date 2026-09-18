// Quartz v4.4.0 quartz/components/pages/FolderContent.tsx 커스텀 버전.
// 배포 시 deploy.yml 이 이 파일로 그 자리를 덮어쓴다.
//
// 이 저장소의 모든 폴더는 tools/build_index.py 가 자동 생성한 "## 문서 목록 (N)"
// 목록을 index.md 본문에 이미 갖고 있다. 원본 FolderContent 는 그 본문 아래에
// Quartz 자체의 <PageList/> 를 한 번 더 붙이기 때문에 문서 목록이 같은 페이지에
// 두 번 나온다 — 그 두 번째 자동 목록만 제거했다. (본문은 그대로 렌더링)
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "../types"
import { Root } from "hast"
import { htmlToJsx } from "../../util/jsx"

const FolderContent: QuartzComponent = (props: QuartzComponentProps) => {
  const { tree, fileData } = props
  const cssClasses: string[] = fileData.frontmatter?.cssclasses ?? []
  const classes = ["popover-hint", ...cssClasses].join(" ")

  const content =
    (tree as Root).children.length === 0 ? fileData.description : htmlToJsx(fileData.filePath!, tree)

  return (
    <div class={classes}>
      <article>{content}</article>
    </div>
  )
}

FolderContent.css = undefined
export default (() => FolderContent) satisfies QuartzComponentConstructor
