import MediumEditor from 'medium-editor'
import React from 'react'
import ReactTooltip from 'react-tooltip'
import ReactDOM from 'react-dom'
import TooltipContent from './TooltipContent'

const LinkPreview = MediumEditor.extensions.anchorPreview.extend({
  name: 'link-preview',
  handleEditableMouseover: function (event) {
    const target = MediumEditor.util.getClosestTag(event.target, 'a');

    if (target === false) {
      return null
    }
    // Detect empty href attributes
    // The browser will make href="" or href="#top"
    // into absolute urls when accessed as event.target.href, so check the html
    if (!this.showOnEmptyLinks && (!/href=["']\S+["']/.test(target.outerHTML) || /href=["']#\S+["']/.test(target.outerHTML))) {
      return true
    }
    // only show when toolbar is not present
    const toolbar = this.base.getExtensionByName('toolbar');
    if (!this.showWhenToolbarIsVisible && toolbar && toolbar.isDisplayed && toolbar.isDisplayed()) {
      return true
    }
    // detach handler for other anchor in case we hovered multiple anchors quickly
    if (this.activeAnchor && this.activeAnchor !== target) {
      this.detachPreviewHandlers();
    }
    this.anchorToPreview = target;
    // Using setTimeout + delay because:
    // - We're going to show the anchor preview according to the configured delay
    //   if the mouse has not left the anchor tag in that time
    this.base.delay(() => {
      if (this.anchorToPreview) {
        this.showPreview(this.anchorToPreview);
      }
    })
    return null
  },

  showPreview: function (anchorEl) { // taken from https://github.com/yabwe/medium-editor/blob/b1b0e87eb5b97698d53c48612f8c948153fb0b17/src/js/extensions/anchor-preview.js#L78
    if (this.anchorPreview.classList.contains('medium-editor-anchor-preview-active') || anchorEl.getAttribute('data-disable-preview')) {
      return true;
    }
    // this.base.selectElement(anchorEl)
    // we changed this :
    if (this.previewValueSelector) {
      ReactDOM.render(<TooltipContent
        linkType={anchorEl.getAttribute('data-linktype') || 'href'}
        pageId={anchorEl.getAttribute('data-id')}
        title={anchorEl.getAttribute('data-title')}
        href={anchorEl.getAttribute('href')}
        fragment={anchorEl.getAttribute('data-fragment')}
        onClick={event => this.handleClickToEditLink(event, anchorEl)}
        onChangeFragment={fragment => this.handleChangeFragment(fragment, anchorEl)}
      />, this.anchorPreview)
    }

    this.anchorPreview.classList.add('medium-toolbar-arrow-over');
    this.anchorPreview.classList.remove('medium-toolbar-arrow-under');

    if (!this.anchorPreview.classList.contains('medium-editor-anchor-preview-active')) {
      this.anchorPreview.classList.add('medium-editor-anchor-preview-active');
    }

    this.activeAnchor = anchorEl // required for positionPreview()
    this.positionPreview()
    this.attachPreviewHandlers()

    return this
  },

  handleChangeFragment: function (fragment, anchorEl) {
    if (fragment === null) {
      anchorEl.removeAttribute('data-fragment')
    } else {
      anchorEl.setAttribute('data-fragment', fragment)
    }

    this.showPreview(anchorEl)
    this.base.selectElement(anchorEl)
    this.base.checkContentChanged()
  },

  handleClickToEditLink: function (event, anchorEl) { // taken from https://github.com/yabwe/medium-editor/blob/b1b0e87eb5b97698d53c48612f8c948153fb0b17/src/js/extensions/anchor-preview.js#L174
    if (anchorEl) {
      const anchorExtension = this.base.getExtensionByName(anchorEl.getAttribute('data-linktype') === 'document' ? 'linkdoc' : 'link')
      if (anchorExtension) {
        event.preventDefault()
        this.base.selectElement(anchorEl)
        // Using setTimeout + delay because:
        // We may actually be displaying the anchor form, which should be controlled by delay
        this.base.delay(() => {
          anchorExtension.showModalWorkflow(anchorEl.getAttribute('data-parent-id'), anchorEl.getAttribute('href'))
        })
      }
    }
    this.hidePreview()
  },
})

MediumEditor.extensions.linkPreview = LinkPreview

export default LinkPreview
