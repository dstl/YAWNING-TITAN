import { Injectable } from '@angular/core';
import { Subject } from 'rxjs';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';

@Injectable()
export class PropertiesEditorService {

  private nodeDetails: any

  public nodeDetailsSubject = new Subject<any>();

  constructor(
    private cytoscapeService: CytoscapeService
  ) { }

  public loadDetails(id: string) {
    // get the node details
    const cyNode = this.cytoscapeService.cytoscapeObj.nodes().getElementById(id);

    this.nodeDetails = {
        uuid: cyNode.id(),
        name: cyNode.data('name'),
        high_value_node: cyNode.data('high_value_node'),
        entry_node: cyNode.data('entry_node'),
        classes: cyNode.data('classes'),
        x_pos: cyNode.position().x,
        y_pos: cyNode.position().y
    }
    this.nodeDetailsSubject.next(this.nodeDetails);
  }
}
