import { Component } from '@angular/core';
import { CytoscapeService } from 'src/app/services/cytoscape/cytoscape.service';

@Component({
  selector: 'app-canvas-control',
  templateUrl: './canvas-control.component.html',
  styleUrls: ['./canvas-control.component.scss']
})
export class CanvasControlComponent {

  constructor(private cytoscapeService: CytoscapeService) { }

  resetView() {
    this.cytoscapeService.resetView();
  }
}
