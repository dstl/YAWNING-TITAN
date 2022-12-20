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
      console.error("Unable to parse file", e);
    }
  }
}
