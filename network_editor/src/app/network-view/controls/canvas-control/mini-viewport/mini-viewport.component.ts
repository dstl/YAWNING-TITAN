import { AfterViewInit, Component, ElementRef, ViewChild } from '@angular/core';
import { MiniViewportService } from './service/mini-viewport.service';
import { CytoscapeService } from 'src/app/services/cytoscape/cytoscape.service';

@Component({
  selector: 'app-mini-viewport',
  templateUrl: './mini-viewport.component.html',
  styleUrls: ['./mini-viewport.component.scss']
})
export class MiniViewportComponent implements AfterViewInit {
  @ViewChild('miniViewport', { static: true }) viewport: ElementRef;

  constructor(
    private cytoscapeService: CytoscapeService,
    private viewportService: MiniViewportService
  ) { }

  ngAfterViewInit(): void {
    // initialise service
    this.cytoscapeService.cytoscapeInstance.subscribe(() => {
      this.viewportService.init(this.viewport.nativeElement);
    })
  }
}
