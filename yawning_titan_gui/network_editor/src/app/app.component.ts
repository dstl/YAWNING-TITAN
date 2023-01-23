import { AfterViewInit, Component, ElementRef, HostListener, OnInit, ViewChild } from '@angular/core';
import { CytoscapeService } from './services/cytoscape/cytoscape.service';
import { ElementType } from './services/cytoscape/graph-objects';
import { NodePropertiesSidenavComponent } from './node-properties/node-properties-sidenav/node-properties-sidenav.component';
import { InteractionService } from './services/interaction/interaction.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
  host: {
    '(document:keydown)': 'handleKeyboardEvent($event)'
  }
})
export class AppComponent implements OnInit {
  @ViewChild('nodePropertiesSideNav', { static: true }) sidenav: NodePropertiesSidenavComponent;

  constructor(
    private cytoscapeService: CytoscapeService,
    private interactionService: InteractionService
  ) { }

  ngOnInit() {
    // listen to element selection
    this.cytoscapeService.selectedElementEvent.subscribe(el => this.toggleNodePropertiesSidenav(el))
  }

  /**
   * Listen to key press
  */
  handleKeyboardEvent(event: KeyboardEvent) {
    this.interactionService.keyInput(event);
  }

  /**
   * Toggles the node properties sidenav
   * Opens the sidenav when a node is selected, closes it otherwise
   * @param element
   * @returns
   */
  private toggleNodePropertiesSidenav(element: { id: string, type: ElementType }): void {
    // if not a node, close sidenav
    if(element?.type !== ElementType.NODE) {
      this.sidenav.close();
      return;
    }

    this.sidenav.open(element.id);
  }
}
