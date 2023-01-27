import { AfterViewInit, Component, ElementRef, HostListener, Inject, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';
import { ImportService } from '../services/export-import/import.service';

@Component({
  selector: 'app-network-view',
  templateUrl: './network-view.component.html',
  styleUrls: ['./network-view.component.scss']
})
export class NetworkViewComponent implements AfterViewInit {
  @ViewChild('main', { static: true }) main!: ElementRef;

  private curNetworkJsonString = "";

  constructor(
    private cytoscapeService: CytoscapeService,
    private importService: ImportService
  ) { }

  ngAfterViewInit() {
    // set the element to render to
    this.cytoscapeService.init(this.main?.nativeElement);

    // check if window.NETWORK has been set
    if (window && (<any>window).NETWORK) {
      this.curNetworkJsonString = (<any>window).NETWORK;
      this.importService.loadNetworkFromWindow((<any>window).NETWORK);
    }
  }

  /**
   * listen to the networkUpdate event
   * @param event
   * @returns
   */
  @HostListener('document:networkUpdate', ['$event'])
  listenToNetworkChange(event: any) {
    // make sure that the network is not the same as previous
    if(!event || event?.detail == this.curNetworkJsonString) {
      return;
    }

    this.curNetworkJsonString = event?.detail;
    this.importService.loadNetworkFromWindow(event?.detail);
  }

  /**
   * Load the dropped file
   * @param $event
   */
  loadFile($event: any) {
    this.importService.loadFile($event);
  }
}
