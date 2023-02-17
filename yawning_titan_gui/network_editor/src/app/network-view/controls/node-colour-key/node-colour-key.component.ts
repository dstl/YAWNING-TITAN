import { Component, Inject } from '@angular/core';
import * as cytoscape from 'cytoscape';
import { CYTOSCAPE_STYLE } from 'src/app/app.tokens';

@Component({
  selector: 'app-node-colour-key',
  templateUrl: './node-colour-key.component.html',
  styleUrls: ['./node-colour-key.component.scss']
})
export class NodeColourKeyComponent {
  constructor(@Inject(CYTOSCAPE_STYLE) private styles) {}

  colourKeyList(): any[] {
    return this.styles;
  }
}
