// Quartz v4.4.0 quartz/components/Backlinks.tsx 커스텀 버전.
// 배포 시 deploy.yml 이 이 파일로 그 자리를 덮어쓴다.
//
// 원본은 역링크가 하나도 없어도 "Backlinks / 이 페이지를 가리키는 문서가 없습니다"
// 를 항상 보여준다. 이 저장소는 문서 대부분이 [[...]] 로 서로 링크돼 있지만
// 일부(오래된 작업/회의록 등)는 역링크가 없어서, 그 페이지들에 빈 블록만 남는
// 게 어색하다는 지적이 있었다 — 역링크가 없으면 컴포넌트 자체를 렌더링하지 않는다.
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./types"
import style from "./styles/backlinks.scss"
import { resolveRelative, simplifySlug } from "../util/path"
import { i18n } from "../i18n"
import { classNames } from "../util/lang"

const Backlinks: QuartzComponent = ({
  fileData,
  allFiles,
  displayClass,
  cfg,
}: QuartzComponentProps) => {
  const slug = simplifySlug(fileData.slug!)
  const backlinkFiles = allFiles.filter((file) => file.links?.includes(slug))

  if (backlinkFiles.length === 0) return null

  return (
    <div class={classNames(displayClass, "backlinks")}>
      <h3>{i18n(cfg.locale).components.backlinks.title}</h3>
      <ul class="overflow">
        {backlinkFiles.map((f) => (
          <li>
            <a href={resolveRelative(fileData.slug!, f.slug!)} class="internal">
              {f.frontmatter?.title}
            </a>
          </li>
        ))}
      </ul>
    </div>
  )
}

Backlinks.css = style
export default (() => Backlinks) satisfies QuartzComponentConstructor
