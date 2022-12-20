import { Component } from '@angular/core';
import { NodeCollection } from 'cytoscape';
import { CytoscapeService } from '../../services/cytoscape/cytoscape.service';

@Component({
  selector: 'app-controls',
  templateUrl: './controls.component.html',
  styleUrls: ['./controls.component.scss']
})
export class ControlsComponent {

  constructor(
    private cytoscapeService: CytoscapeService
  ) { }

  nodeList(): string[] {
    return this.cytoscapeService?.cytoscapeObj?.nodes().map(node => node.id())
  }

  downloadNetwork(): void {
    console.log(this.cytoscapeService.getNetworkJson())
  }

  resetView() {
    this.cytoscapeService.resetView();
  }
}
