import MediumEditor from 'medium-editor'
import rangy from 'rangy/lib/rangy-classapplier' // http://stackoverflow.com/questions/29530195/rangy-classapplier-and-browserify

// https://github.com/yabwe/medium-editor/blob/ea7b00b7ddbf5fe9c9655a4e65e9495c46f958a4/src/js/extensions/WALKTHROUGH-BUTTON.md#walkthrough---building-a-button
const MediumButtonFactory = ({ name, tag, contentDefault, contentFA, aria, action, className }) => MediumEditor.extensions.button.extend({
  name, // identifier of the button
  tagNames: [tag], // nodeName which indicates the button should be 'active' when isAlreadyApplied() is called
  contentDefault, // default innerHTML of the button
  contentFA, // innerHTML of button when 'fontawesome' is being used
  aria, // used as both aria-label and title attributes
  action, // used as the data-action attribute of the button

  init: function (args) { // eslint-disable-line
    MediumEditor.extensions.button.prototype.init.call(this);
  },

  handleClick: function (event) {
    const classApplier = rangy.createClassApplier(className, {
      elementTagName: tag,
      normalize: true,
    })
    classApplier.toggleSelection()
    // Ensure the editor knows about an html change so watchers are notified
    // ie: <textarea> elements depend on the editableInput event to stay synchronized
    this.base.checkContentChanged()
  },
})

export default MediumButtonFactory
