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

    // update form group
    this.nodePropertiesFormGroupSubject.next(this._nodePropertiesFormGroup);
  }

  /**
   * Function that triggers the persisting of the updated node properties
   */
  public updateNodeProperties(): void {
    // check if form is valid
    if (!this._nodePropertiesFormGroup || !this._nodePropertiesFormGroup.valid) {
      return;
    }

    // update
    this.cytoscapeService.updateNode(this._nodePropertiesFormGroup.get('uuid').value, {
      uuid: this._nodePropertiesFormGroup.get('uuid').value,
      name: this._nodePropertiesFormGroup.get('name').value,
      x_pos: this._nodePropertiesFormGroup.get('x_pos').value,
      y_pos: this._nodePropertiesFormGroup.get('y_pos').value,
      vulnerability: this._nodePropertiesFormGroup.get('vulnerability').value,
      high_value_node: this._nodePropertiesFormGroup.get('high_value_node').value,
      entry_node: this._nodePropertiesFormGroup.get('entry_node').value,
    })
  }
}
