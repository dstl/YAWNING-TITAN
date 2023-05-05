import { Component, Inject, OnInit, ViewChild } from '@angular/core';
import { ElementType, SelectedGraphRef as SelectedGraphItemRef } from './services/cytoscape/graph-objects';
import { NodePropertiesSidenavComponent } from './node-properties/node-properties-sidenav/node-properties-sidenav.component';
import { InteractionService } from './services/interaction/interaction.service';
import { NetworkService } from './network-class/network.service';
import { Network } from './network-class/network';
import { Node } from './network-class/network-interfaces';
import { HttpClient } from '@angular/common/http';
import { DJANGO_SAVE_URL } from './app.tokens';
import { debounceTime, tap } from 'rxjs';

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
    @Inject(DJANGO_SAVE_URL) private saveUrl,
    private http: HttpClient,
    private networkService: NetworkService,
    private interactionService: InteractionService
  ) { }

  ngOnInit() {
    // listen to element selection
    this.interactionService.selectedItem.subscribe(el => {
      this.toggleNodePropertiesSidenav(el)
    });

    this.networkService.networkObservable
      .pipe(
        tap((network: Network) => this.updateNodeList(network?.nodeList)),
        debounceTime(1000)
      )
      .subscribe((network: Network) => {
        // only update if network is not locked
        if (network?.documentMetadata?.locked) {
          return;
        }
        // update network
        this.updateNetwork();
      })
  }

  /**
   * Update the node list in the toolbar
   */
  private updateNodeList(nodeList: Node[]): void {
    document.dispatchEvent(new CustomEvent('updateNodeList', {
      detail: nodeList
    }));
  }

  /**
   * Persist the changes by updating the network in the backend
   */
  private updateNetwork(): void {
    const payload = JSON.stringify(this.networkService.getNetworkJson());
    this.http.post(this.saveUrl, payload)
      .subscribe()
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
  private toggleNodePropertiesSidenav(element: SelectedGraphItemRef): void {
    // if not a node, close sidenav
    if (element?.type !== ElementType.NODE) {
      this.sidenav.close();
      return;
    }

    // check if node exists
    const node = this.networkService.getNodeById(element.id);

    // do not open sidenav if node does not exist
    if (!node) {
      return;
    }

    this.sidenav.open(node);
  }
}
