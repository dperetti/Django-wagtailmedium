import MediumEditor from 'medium-editor'

const rangy = require('rangy/lib/rangy-classapplier.js') // http://stackoverflow.com/questions/29530195/rangy-classapplier-and-browserify

function createLinkAttributes(pageData) {
  let obj = {
    href: pageData.url,
  }
  if (pageData.id) {
    obj = { ...obj,
      'data-title': pageData.title,
      'data-id': pageData.id,
      'data-parent-id': pageData.parentId,
      'data-linktype': 'page',
    }
  }
  return obj
}

// https://github.com/yabwe/medium-editor/blob/ea7b00b7ddbf5fe9c9655a4e65e9495c46f958a4/src/js/extensions/WALKTHROUGH-BUTTON.md#walkthrough---building-a-button
const LinkButton = MediumEditor.extensions.button.extend({
  name: 'link',
  contentDefault: '<b>Link</b>', // default innerHTML of the button
  contentFA: '<span class="fa fa-link"></span>', // innerHTML of button when 'fontawesome' is being used
  aria: 'Link', // used as both aria-label and title attributes
  action: 'Link', // used as the data-action attribute of the button

  init: function () {
    MediumEditor.extensions.button.prototype.init.call(this)
  },

  isAlreadyApplied: function (node) {
    return node.nodeName.toLowerCase() === 'a' && node.getAttribute('data-linktype') !== 'document'
  },

  showModalWorkflow: function (parentPageId = null, href = null) {
    const urlParams = {
      allow_external_link: true,
      allow_email_link: true,
    };
    let url
    if (parentPageId) {
      url = window.chooserUrls.pageChooser + (parentPageId ? parentPageId.toString() + '/' : '')
    } else if (href) {
      if (href.startsWith('mailto:')) {
        url = window.chooserUrls.emailLinkChooser
        href = href.replace('mailto:', '')
      } else {
        url = window.chooserUrls.externalLinkChooser
      }
      urlParams['link_url'] = href
    } else {
      url = window.chooserUrls.pageChooser
    }

    const base = this.base;
    base.saveSelection()
    // https://github.com/torchbox/wagtail/blob/c6666c6de5e83bf94d18324858c121e6584ba47d/wagtail/wagtailadmin/static_src/wagtailadmin/js/modal-workflow.js#L6
    ModalWorkflow({ // #7FsEf#
      url,
      urlParams,
      responses: {
        pageChosen: function (pageData) {
          const classApplier = rangy.createClassApplier('wagtail-page', {
            elementTagName: 'a',
            normalize: true,
            elementAttributes: createLinkAttributes(pageData),
          });
          base.restoreSelection()
          classApplier.toggleSelection()
          // Ensure the editor knows about an html change so watchers are notified
          // ie: <textarea> elements depend on the editableInput event to stay synchronized
          base.checkContentChanged()
        },
      },
    })
  },

  // https://github.com/yabwe/medium-editor/blob/b1b0e87eb5b97698d53c48612f8c948153fb0b17/src/js/extensions/anchor.js#L56
  handleClick: function (event, ed) { // #3EcPh#
    event.preventDefault()
    event.stopPropagation()

    const range = MediumEditor.selection.getSelectionRange(this.document);

    if (range.startContainer.nodeName.toLowerCase() === 'a' ||
        range.endContainer.nodeName.toLowerCase() === 'a' ||
        MediumEditor.util.getClosestTag(MediumEditor.selection.getSelectedParentElement(range), 'a')
    ) {
      return this.execAction('unlink')
    }
    const elem = MediumEditor.selection.getSelectedParentElement(range)
    // const pageId = elem.getAttribute('data-id')
    const parentPageId = elem.getAttribute('data-parent-id')
    this.showModalWorkflow(parentPageId)
  },
})

export default LinkButton
