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
  title = 'network_editor';

  @ViewChild('appSideNav', { static: true }) sidenav: NodePropertiesSidenavComponent;

  constructor(
    private cytoscapeService: CytoscapeService,
    private interactionService: InteractionService
  ) { }

  ngOnInit() {
    // listen to element selection
    this.cytoscapeService.selectedElementSubject.subscribe(el => this.toggleSidenav(el))
  }

  /**
   * Listen to key press
  */
  handleKeyboardEvent(event: KeyboardEvent) {
    switch (event?.key) {
      case 'Backspace':
      case 'Delete':
        this.cytoscapeService.deleteItem()

      default:
        break;
    }
  }

  private toggleSidenav(element: { id: string, type: ElementType }): void {
    // if not a node, close sidenav
    if(element?.type !== ElementType.NODE) {
      this.sidenav.close();
      return;
    }

    this.sidenav.open(element.id);
  }
}
