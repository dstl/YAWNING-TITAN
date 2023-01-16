import { Injectable } from '@angular/core';
import { Network } from 'src/app/network-class/network';
import { CytoscapeService } from '../cytoscape/cytoscape.service';

@Injectable({
  providedIn: 'root'
})
export class ImportService {

  constructor(
    private cytoscapeService: CytoscapeService
  ) { }

  /**
   * Parse the dropped file and load the network if the file is valid
   * @param $event
   *
   * @returns
   */
  public async loadFile($event): Promise<void> {
    // read first file
    if (!$event || !$event[0]) {
      return;
    }

    try {
      const content = await ($event[0] as File).text();
      const network = new Network(JSON.parse(content));

      this.cytoscapeService.loadNetwork(network);
    } catch (e) {
      throw new Error("Unable to parse file", e);
    }
  }

  /**
   * Load the JSON passed from the window.NETWORK variable that is loaded from the Django side
   * @param windowNetwork
   */
  public loadNetworkFromWindow(windowNetwork: any) {
    // read first file
    if (!windowNetwork) {
      return;
    }

    try {
      const network = new Network(JSON.parse(windowNetwork));
      this.cytoscapeService.loadNetwork(network);
    } catch (e) {
      throw new Error("Unable to parse JSON", e);
    }
  }
}
