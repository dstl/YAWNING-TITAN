import { Component, ElementRef, Input, OnInit } from '@angular/core';
import * as cytoscape from 'cytoscape';

@Component({
  selector: 'app-node-colour-key-item',
  templateUrl: './node-colour-key-item.component.html',
  styleUrls: ['./node-colour-key-item.component.scss']
})
export class NodeColourKeyItemComponent implements OnInit {
  @Input() public label;
  @Input() public style: cytoscape.Css.Node | cytoscape.Css.Edge | cytoscape.Css.Core;

  constructor(
    private el: ElementRef
  ) { }

  ngOnInit() {
    this.setNodeStyle(this.el.nativeElement.querySelector('.node-key-item'), this.style)
  }

  private setNodeStyle(el: HTMLElement, nodeStyle: cytoscape.Css.Node | cytoscape.Css.Edge | cytoscape.Css.Core) {
    if (!el) {
      return;
    }

    // apply stroke color if exists
    if (nodeStyle['border-color']) {
      el.style.borderColor = nodeStyle['border-color']
    }

    // apply background color if exists
    if (nodeStyle['background-color']) {
      el.style.backgroundColor = nodeStyle['background-color'];
    }

    console.log(nodeStyle)
  }
}
