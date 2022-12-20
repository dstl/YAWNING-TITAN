import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';
import { ImportService } from '../services/export-import/import.service';

@Component({
  selector: 'app-network-view',
  templateUrl: './network-view.component.html',
  styleUrls: ['./network-view.component.scss']
})
export class NetworkViewComponent implements AfterViewInit {
  @ViewChild('main', { static: true }) main!: ElementRef;

  constructor(
    private cytoscapeService: CytoscapeService,
    private importService: ImportService
  ) {

  }

  ngAfterViewInit() {
    // set the element to render to
    this.cytoscapeService.init(this.main?.nativeElement);
  }

  loadFile($event: any) {
    this.importService.loadFile($event);
  }
}
