import { PageLayout, SharedLayout } from "./quartz/cfg"
import * as Component from "./quartz/components"
import { QuartzComponent, QuartzComponentConstructor, QuartzComponentProps } from "./quartz/components/types"

// Quartz v4.4.0 기본 quartz.layout.ts 를 기반으로 커스터마이징.
// 이 저장소엔 원래 quartz.layout.ts 가 없어서(=기본값 그대로) Explorer/TOC/Graph/
// Backlinks 가 전부 기본 동작이었다. 홈페이지(index)는 포트폴리오 랜딩 느낌을
// 위해 Graph/Backlinks/TableOfContents 를 숨기고, 나머지 문서 페이지는 그대로 둔다.

// 특정 컴포넌트를 홈(index) 페이지에서만 숨기는 래퍼.
// Quartz 의 ContentPage 이미터는 모든 콘텐츠 페이지에 같은 레이아웃을 쓰기 때문에,
// 페이지별로 다르게 보이게 하려면 컴포넌트 레벨에서 slug 를 보고 분기해야 한다.
function hideOnIndex(Wrapped: QuartzComponent): QuartzComponent {
  const HiddenOnIndex: QuartzComponent = (props: QuartzComponentProps) => {
    if (props.fileData.slug === "index") return null
    return Wrapped(props)
  }
  HiddenOnIndex.css = Wrapped.css
  HiddenOnIndex.afterDOMLoaded = Wrapped.afterDOMLoaded
  return HiddenOnIndex
}

// components shared across all pages
export const sharedPageComponents: SharedLayout = {
  head: Component.Head(),
  header: [],
  afterBody: [],
  footer: Component.Footer({
    links: {
      GitHub: "https://github.com/jeakyoung",
    },
  }),
}

// components for pages that display a single page (e.g. a single note)
export const defaultContentPageLayout: PageLayout = {
  beforeBody: [
    Component.Breadcrumbs(),
    Component.ArticleTitle(),
    Component.ContentMeta(),
    Component.TagList(),
  ],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Darkmode(),
    Component.DesktopOnly(Component.Explorer()),
  ],
  right: [
    hideOnIndex(Component.Graph()),
    Component.DesktopOnly(hideOnIndex(Component.TableOfContents())),
    hideOnIndex(Component.Backlinks()),
  ],
}

// components for pages that display lists of pages  (e.g. tags or folders)
export const defaultListPageLayout: PageLayout = {
  beforeBody: [Component.Breadcrumbs(), Component.ArticleTitle(), Component.ContentMeta()],
  left: [
    Component.PageTitle(),
    Component.MobileOnly(Component.Spacer()),
    Component.Search(),
    Component.Darkmode(),
    Component.DesktopOnly(Component.Explorer()),
  ],
  right: [],
}
