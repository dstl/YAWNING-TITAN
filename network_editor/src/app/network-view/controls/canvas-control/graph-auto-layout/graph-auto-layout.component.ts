import { HttpClient } from '@angular/common/http';
import { Component, Inject } from '@angular/core';
import { UPDATE_NETWORK_LAYOUT_URL } from '../../../../app.tokens';
import { NetworkService } from '../../../../network-class/network.service';
import { Network } from '../../../../network-class/network';
import { Node } from '../../../../network-class/network-interfaces';

@Component({
  selector: 'app-graph-auto-layout',
  templateUrl: './graph-auto-layout.component.html',
  styleUrls: ['./graph-auto-layout.component.scss']
})
export class GraphAutoLayoutComponent {

  public layouts: string[] = [];

  constructor(
    @Inject(UPDATE_NETWORK_LAYOUT_URL) private updateNetworkLayoutUrl,
    private httpClient: HttpClient,
    private networkService: NetworkService
  ) { }

  /**
   * Parse the list of layouts available to sort the network with
   * @returns
   */
  public autoLayoutsAvailable(): boolean {
    const layouts = (<any>window)?.NETWORK_LAYOUTS;
    if (!layouts) {
      this.layouts = [];
      return;
    }

    this.layouts = JSON.parse(layouts);
    return !!this.layouts?.length;
  }

  /**
   * Send a request to sort the network nodes into a layout that was picked
   * @param layout
   */
  public applyLayout(layout: string): void {
    this.httpClient.post(this.updateNetworkLayoutUrl, {
      'layout': layout,
      'network': this.networkService.getNetworkJson()
    })
      .subscribe((body: any) => {
        try {
          const network = new Network(body);
          this.networkService.loadNetwork(this.scaleUpNodePositions(network));
        } catch (e) {
          throw new Error("Unable to parse JSON", e);
        }
      });
  }

  /**
   * Scales up the node positions
   */
  private scaleUpNodePositions(network: Network): Network {
    // get window sizes
    const winWidth = document.getElementById('cytoscapeCanvas')?.clientWidth;
    const winHeight = document.getElementById('cytoscapeCanvas')?.clientHeight;
    network.nodeList.forEach((node: Node) => {
      node.x_pos = node.x_pos * winWidth
      node.y_pos = node.y_pos * winHeight
    });

    return network;
  }
}
