import { Injectable } from '@angular/core';
import { FormBuilder, FormControl, FormGroup, Validators } from '@angular/forms';
import { debounceTime, Subject } from 'rxjs';
import { NetworkSettings, Node } from '../network-class/network-interfaces';
import { NetworkService } from '../network-class/network.service';
import { InteractionService } from '../services/interaction/interaction.service';

@Injectable()
export class NodePropertiesService {
  // formgroup for the node properties
  private _nodePropertiesFormGroup: FormGroup;
  public nodePropertiesFormGroupSubject = new Subject<FormGroup>();

  // network settings
  private _networkSettings: NetworkSettings

  // id of the current node being edited
  private currentNode: Node = null;

  constructor(
    private networkService: NetworkService,
    private interactionService: InteractionService,
    private formBuilder: FormBuilder
  ) {
    this.networkService.networkObservable.subscribe(network => {
      this._networkSettings = network.networkSettings;

      if (!this._nodePropertiesFormGroup) {
        return;
      }

      if (network.networkSettings.entryNode.set_random_entry_nodes) {
        this._nodePropertiesFormGroup.get('entry_node')?.setValue(false)
      }

      if (network.networkSettings.highValueNode.set_random_high_value_nodes) {
        this._nodePropertiesFormGroup.get('high_value_node')?.setValue(false)
      }

      if (network.networkSettings.vulnerability.set_random_vulnerabilities) {
        this._nodePropertiesFormGroup.get('vulnerability')?.setValue(
          network.networkSettings.vulnerability.node_vulnerability_lower_bound.toFixed(2)
        )
      }
    });

    this.interactionService.dragEvent.subscribe(evt => {
      this.updateNodePositions(evt);
    });
  }

  /**
   * Returns true if the network sets a random entry node on reset
   * @returns
   */
  public randomEntryNodesOnReset(): boolean {
    return this._networkSettings?.entryNode.set_random_entry_nodes;
  }

  /**
   * Returns true if the network sets a random high value node on reset
   * @returns
   */
  public randomHighValueNodesOnReset(): boolean {
    return this._networkSettings?.highValueNode.set_random_high_value_nodes;
  }

  /**
   * Returns true if the network sets random node vulnerabilities on reset
   * @returns
   */
  public randomVulnerabilitiesOnReset(): boolean {
    return this._networkSettings?.vulnerability.set_random_vulnerabilities;
  }

  /**
   * Loads the details of the selected
   * @param id
   */
  public loadDetails(node: Node) {
    if (!node) {
      return;
    }

    this.currentNode = node;

    // create new form group
    this._nodePropertiesFormGroup = this.formBuilder.group({
      uuid: new FormControl({ value: node.uuid, disabled: true }),
      name: new FormControl(node.name, Validators.required),
      vulnerability: new FormControl(this.randomVulnerabilitiesOnReset() ?
        this._networkSettings.vulnerability.node_vulnerability_lower_bound.toFixed(2) : node.vulnerability.toFixed(2), Validators.required),
      x_pos: new FormControl(node.x_pos, Validators.required),
      y_pos: new FormControl(node.y_pos, Validators.required),
      // set to false and disable if random high value nodes are to be set on network
      high_value_node: new FormControl(this.randomHighValueNodesOnReset() ? false : node.high_value_node, Validators.required),
      entry_node: new FormControl(this.randomEntryNodesOnReset() ? false : node.entry_node, Validators.required),
    });

    // update form group
    this.nodePropertiesFormGroupSubject.next(this._nodePropertiesFormGroup);

    // update node on each change
    this._nodePropertiesFormGroup.valueChanges
      .pipe(debounceTime(100))
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
    this.networkService.editNodeDetails({
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
   * Update input fields with the new node
   * @param evt
   */
  public updateNodePositions(val: { id: string, position: { x: number, y: number } }): void {
    // only need to care if the node being dragged is displayed
    if (!val || !(val.id == this.currentNode.uuid)) {
      return;
    }

    // update x pos and y pos
    this._nodePropertiesFormGroup.get('x_pos').setValue(val.position.x);
    this._nodePropertiesFormGroup.get('y_pos').setValue(val.position.y);
  }
}
