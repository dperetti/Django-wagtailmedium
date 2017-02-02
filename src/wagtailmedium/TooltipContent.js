import React, { PropTypes } from 'react'

const linkIcons = {
  href: 'external-link',
  document: 'book',
  page: 'file',
}

export default class TootipContent extends React.Component {
  static propTypes = {
    linkType: PropTypes.oneOf(['page', 'document', 'href']),
    title: PropTypes.string,
    fragment: PropTypes.string,
    onClick: PropTypes.func,
    onChangeFragment: PropTypes.func,
  }

  constructor() {
    super()
    this.state = {
      fragment: '',
    }
  }

  editFragmentHandler = () => {
    const newFragment = window.prompt('Fragment', this.props.fragment || '') // eslint-disable-line
    this.props.onChangeFragment(newFragment.length === 0 ? null : newFragment)
  }

  render() {
    const tooltipClass = `wagtailmedium-tooltip ${this.props.linkType}`

    const icon = <span className={`fa fa-${linkIcons[this.props.linkType]}`}></span>
    let fragmentEditor
    let label
    if (this.props.linkType === 'page' || this.props.linkType === 'document') {
      label = <div><div>{icon}{this.props.title}</div><div className="href">{this.props.href}</div></div>
    } else {
      label = <div>{icon}{this.props.href}</div>
    }
    if (this.props.linkType === 'page') {
      if (this.props.fragment === null) {
        fragmentEditor = <div onClick={this.editFragmentHandler} className="fragment empty-fragment">Click to add fragment</div>
      } else {
        fragmentEditor = <div onClick={this.editFragmentHandler} className="fragment">#{this.props.fragment}</div>
      }
    }
    return (<div className={tooltipClass}>
        <div onClick={this.props.onClick}>
          {label}
        </div>
        {fragmentEditor}
    </div>)
  }
}
