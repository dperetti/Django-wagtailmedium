// #8VVkT#
import 'medium-editor/dist/css/medium-editor.css'
import MediumEditor from 'medium-editor'
import LinkButton from './LinkButton'
import LinkDocButton from './LinkDocButton'
import LinkPreview from './LinkPreview'
import MediumButtonFactory from './MediumButtonFactory'
import './wagtailmedium.less'
import 'font-awesome-webpack'

// Make MediumEditor and related globally available
window.MediumEditor = {
  MediumEditor,
  LinkButton,
  LinkDocButton,
  LinkPreview,
  MediumButtonFactory,
}
