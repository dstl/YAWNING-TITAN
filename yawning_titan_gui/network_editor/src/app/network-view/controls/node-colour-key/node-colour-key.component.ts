import { Component, Inject } from '@angular/core';
import { NODE_KEY_CONFIG } from 'src/app/app.tokens';

@Component({
  selector: 'app-node-colour-key',
  templateUrl: './node-colour-key.component.html',
  styleUrls: ['./node-colour-key.component.scss']
})
export class NodeColourKeyComponent {
  constructor(@Inject(NODE_KEY_CONFIG) private nodeKey) { }

  colourKeyList(): any[] {
    // only display ones that are configured to be shown on the key
    return this.nodeKey && Array.isArray(this.nodeKey) ?
      this.nodeKey.filter(key => !key.noKeyDisplay) : [];
  }
}
