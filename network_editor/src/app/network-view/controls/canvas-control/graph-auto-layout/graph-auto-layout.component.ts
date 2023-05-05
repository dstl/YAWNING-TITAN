import { HttpClient } from '@angular/common/http';
import { Component, Inject } from '@angular/core';
import { UPDATE_NETWORK_LAYOUT_URL } from '../../../../app.tokens';
import { NetworkService } from '../../../../network-class/network.service';
import { Network } from '../../../../network-class/network';
import { NetworkJson } from '../../../../network-class/network-interfaces';
import { MatSnackBar } from '@angular/material/snack-bar';
import { UndoLayoutComponent } from './undo-layout/undo-layout.component';

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
    private networkService: NetworkService,
    private snackBar: MatSnackBar
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
          const currentJson = this.networkService.getNetworkJson();
          body = this.scaleUpNodePositions(body);
          const network = new Network(body);
          this.networkService.loadNetwork(network);
          this.openUndoLayout(currentJson);
        } catch (e) {
          console.error(e);
          throw new Error("Unable to parse JSON", e);
        }
      });
  }

  /**
   * Scales up the node positions
   */
  private scaleUpNodePositions(network: NetworkJson): NetworkJson {
    if (!network || !network.nodes) {
      throw new Error();
    }

    const canvas = document.getElementById('cytoscapeCanvas');

    const winWidth = canvas ? canvas.clientWidth : 0;
    const winHeight = canvas ? canvas.clientHeight : 0;

    const mult = Math.min(winHeight, winWidth)

    Object.keys(network.nodes).forEach((key: string) => {
      network.nodes[`${key}`].x_pos *= mult;
      network.nodes[`${key}`].y_pos *= mult;
    });

    return network;
  }

  /**
   * Open the undo layout snackbar
   */
  private openUndoLayout(data: any): void {
    this.snackBar.openFromComponent(
      UndoLayoutComponent,
      { data, horizontalPosition: 'center' }
    )
  }
}
