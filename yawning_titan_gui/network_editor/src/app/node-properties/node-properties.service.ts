import { Injectable } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { debounceTime, Subject } from 'rxjs';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';

@Injectable()
export class NodePropertiesService {
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
    const node = this.cytoscapeService.network.getNodeById(id);

    if (!node) {
      return;
    }

    // create new form group
    this._nodePropertiesFormGroup = this.formBuilder.group({
      uuid: new FormControl({ value: node.uuid, disabled: true }),
      name: new FormControl(node.name, Validators.required),
      vulnerability: new FormControl(node.vulnerability, Validators.required),
      x_pos: new FormControl(node.x_pos, Validators.required),
      y_pos: new FormControl(node.y_pos, Validators.required),
      high_value_node: new FormControl(node.high_value_node, Validators.required),
      entry_node: new FormControl(node.entry_node, Validators.required),
    });

    // update form group
    this.nodePropertiesFormGroupSubject.next(this._nodePropertiesFormGroup);

    this.listenToNodePositionChange();

    // update node on each change
    this._nodePropertiesFormGroup.valueChanges
      .pipe(debounceTime(50))
      .subscribe(() => this.updateNodeProperties());
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
    this.cytoscapeService.updateNode({
      uuid: this._nodePropertiesFormGroup.get('uuid').value,
      name: this._nodePropertiesFormGroup.get('name').value,
      x_pos: Number(this._nodePropertiesFormGroup.get('x_pos').value),
      y_pos: Number(this._nodePropertiesFormGroup.get('y_pos').value),
      vulnerability: this._nodePropertiesFormGroup.get('vulnerability').value,
      high_value_node: this._nodePropertiesFormGroup.get('high_value_node').value,
      entry_node: this._nodePropertiesFormGroup.get('entry_node').value,
    })
  }

  /**
   * Function used to listen to node repositioning via drag
  */
  private listenToNodePositionChange(): void {
    this.cytoscapeService.elementDragEvent.subscribe(res => {
      if (!(res.id === this._nodePropertiesFormGroup.get('uuid').value)) {
        return;
      }
      // update x pos and y pos
      this._nodePropertiesFormGroup.get('x_pos').setValue(res.position.x);
      this._nodePropertiesFormGroup.get('y_pos').setValue(res.position.y);
      this.updateNodeProperties();
    })
  }
}
