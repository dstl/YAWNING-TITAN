import { Injectable } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { debounceTime, Subject } from 'rxjs';
import { Node } from '../network-class/network-interfaces';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';

@Injectable()
export class PropertiesEditorService {

  private nodeDetails: any

  public nodeDetailsSubject = new Subject<any>();

  private _nodePropertiesFormGroup: FormGroup;

  public nodePropertiesFormGroupSubject = new Subject<FormGroup>();

  constructor(
    private cytoscapeService: CytoscapeService,
    private formBuilder: FormBuilder
  ) { }

  /**
   * Loads the details of the selected
   * @param id
   */
  public loadDetails(id: string) {
    // get the node details
    const cyNode = this.cytoscapeService.cytoscapeObj.nodes().getElementById(id);

    this.nodeDetails = {
      uuid: cyNode.id(),
      name: cyNode.data('name'),
      x_pos: cyNode.position().x,
      y_pos: cyNode.position().y,
      vulnerability: cyNode.data('vulnerability'),
      high_value_node: cyNode.data('high_value_node'),
      entry_node: cyNode.data('entry_node')
    }

    // create new form group
    this._nodePropertiesFormGroup = this.formBuilder.group({
      uuid: new FormControl({ value: this.nodeDetails.uuid, disabled: true }),
      name: new FormControl(this.nodeDetails.name, Validators.required),
      vulnerability: new FormControl(this.nodeDetails.vulnerability, Validators.required),
      x_pos: new FormControl(this.nodeDetails.x_pos, Validators.required),
      y_pos: new FormControl(this.nodeDetails.y_pos, Validators.required),
      high_value_node: new FormControl(this.nodeDetails.high_value_node, Validators.required),
      entry_node: new FormControl(this.nodeDetails.entry_node, Validators.required),
    });

    // listen to changes
    this._nodePropertiesFormGroup.valueChanges.pipe(debounceTime(200))
      .subscribe(res => this.updateCytoscapeObject(res))

    // update form group
    this.nodePropertiesFormGroupSubject.next(this._nodePropertiesFormGroup);
  }

  /**
   * Update the cytoscape object
   * @param changes
   */
  private updateCytoscapeObject(changes: Node): void {
    this.cytoscapeService.updateNode(this._nodePropertiesFormGroup.controls['uuid'].value, changes);
  }
}
