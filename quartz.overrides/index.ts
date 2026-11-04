// Quartz v4.4.0 quartz/components/index.ts 커스텀 버전.
// 배포 시 deploy.yml 이 이 파일로 그 자리를 덮어쓴다.
// 원본에 PdfButton 컴포넌트(경력 서류 페이지의 "PDF로 저장" 버튼) export 만 추가했다.
import Content from "./pages/Content"
import TagContent from "./pages/TagContent"
import FolderContent from "./pages/FolderContent"
import NotFound from "./pages/404"
import ArticleTitle from "./ArticleTitle"
import Darkmode from "./Darkmode"
import Head from "./Head"
import PageTitle from "./PageTitle"
import ContentMeta from "./ContentMeta"
import Spacer from "./Spacer"
import TableOfContents from "./TableOfContents"
import Explorer from "./Explorer"
import TagList from "./TagList"
import Graph from "./Graph"
import Backlinks from "./Backlinks"
import Search from "./Search"
import Footer from "./Footer"
import DesktopOnly from "./DesktopOnly"
import MobileOnly from "./MobileOnly"
import RecentNotes from "./RecentNotes"
import Breadcrumbs from "./Breadcrumbs"
import Comments from "./Comments"
import PdfButton from "./PdfButton"

export {
  ArticleTitle,
  Content,
  TagContent,
  FolderContent,
  Darkmode,
  Head,
  PageTitle,
  ContentMeta,
  Spacer,
  TableOfContents,
  Explorer,
  TagList,
  Graph,
  Backlinks,
  Search,
  Footer,
  DesktopOnly,
  MobileOnly,
  RecentNotes,
  NotFound,
  Breadcrumbs,
  Comments,
  PdfButton,
}
