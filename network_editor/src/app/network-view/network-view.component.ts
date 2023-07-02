import { AfterViewInit, Component, ElementRef, HostListener, Inject, OnChanges, SimpleChanges, ViewChild } from '@angular/core';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';
import { ImportService } from '../services/export-import/import.service';
import { InteractionService } from '../services/interaction/interaction.service';

@Component({
  selector: 'app-network-view',
  templateUrl: './network-view.component.html',
  styleUrls: ['./network-view.component.scss']
})
export class NetworkViewComponent implements AfterViewInit {
  @ViewChild('cytoscapeCanvas', { static: true }) cytoscapeCanvas!: ElementRef;

  private curNetworkJsonString = "";

  constructor(
    private cytoscapeService: CytoscapeService,
    private importService: ImportService,
    private interactionService: InteractionService
  ) { }

  ngAfterViewInit() {
    // set the element to render to
    this.cytoscapeService.init(this.cytoscapeCanvas?.nativeElement);

    // check if window.NETWORK has been set
    if (globalThis.NETWORK) {
      this.curNetworkJsonString = globalThis.NETWORK;
      this.importService.loadNetworkFromWindow(globalThis.NETWORK);
    }
  }

  /**
   * listen to the networkUpdate event
   * @param event
   * @returns
   */
  @HostListener('document:networkUpdate', ['$event'])
  private listenToNetworkChange(event: any) {
    // make sure that the network is not the same as previous
    if (!event || event?.detail == this.curNetworkJsonString) {
      return;
    }

    this.curNetworkJsonString = event?.detail;
    this.importService.loadNetworkFromWindow(event?.detail);
  }


  /**
   * listen to the networkUpdate event
   * @param event
   * @returns
   */
  @HostListener('document:networkSettingsUpdate', ['$event'])
  private listenToNetworkSettingsChange(event: any) {
    let val = {};
    for (const formData of event?.detail) {
      val[`${formData[0]}`] = formData[1];
    }

    if (val['_operation'] == 'UPDATE_NETWORK_DETAILS') {
      this.interactionService.processNetworkSettingsChanges(val);
      return;
    } else if (val['_operation'] == 'UPDATE_NETWORK_METADATA') {
      this.interactionService.processNetworkMetadataChanges(val);
      return;
    }
  }

  @HostListener('document:nodeSelected', ['$event'])
  private listenToSelectedNodeListItem(event: any) {
    this.interactionService.processNodeSelected(event?.detail);
  }

  @HostListener('document:deleteNode', ['$event'])
  private listenToNodeListItemDelete(event: any) {
    this.interactionService.processNodeDelete(event?.detail);
  }

  /**
   * Listen to window resize event and resize the cytoscape canvas
   * @param event
   */
  @HostListener('window:resize', ['$event'])
  onResize(event) {
    const element: Element = this.cytoscapeCanvas.nativeElement;

    // get the height of the top nav if it exists
    const topOffset = document.getElementById('top-nav') ? document.getElementById('top-nav').offsetHeight : 0;

    // get the width of toolbar
    const toolbarWidth = document.getElementById('toolbar') ? document.getElementById('toolbar').offsetWidth : 0;
    const sidenavWidth = document.getElementById('network-sidenav')? document.getElementById('network-sidenav').offsetWidth : 0;

    // set element width and height
    element['style'].width = `${event.target.innerWidth - (toolbarWidth + sidenavWidth)}px`
    element['style'].height = `${event.target.innerHeight - topOffset}px`

    this.cytoscapeService.resetView();
  }

  /**
   * Load the dropped file
   * @param $event
   */
  public loadFile($event: any) {
    this.importService.loadFile($event);
  }
}
