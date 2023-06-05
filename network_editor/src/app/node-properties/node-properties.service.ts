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
    this.networkService.networkSettingsObservable.subscribe(networkSettings => {
      this._networkSettings = networkSettings;

      if (!this._nodePropertiesFormGroup) {
        return;
      }

      if (networkSettings.entryNode.set_random_entry_nodes) {
        this._nodePropertiesFormGroup.get('entry_node')?.setValue(false)
      }

      if (networkSettings.highValueNode.set_random_high_value_nodes) {
        this._nodePropertiesFormGroup.get('high_value_node')?.setValue(false)
      }

      if (networkSettings.vulnerability.set_random_vulnerabilities) {
        this._nodePropertiesFormGroup.get('vulnerability')?.setValue(
          networkSettings.vulnerability.node_vulnerability_lower_bound.toFixed(2)
        )
      }

      this.loadDetails(
        this.networkService.getNodeById(this.currentNode?.uuid)
      );
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
    if (!node || this.currentNode?.uuid == node?.uuid) {
      return;
    }

    this.currentNode = node;

    // create new form group
    this._nodePropertiesFormGroup = this.formBuilder.group({
      uuid: new FormControl({ value: node.uuid, disabled: true }),
      name: new FormControl(node.name, Validators.required),
      vulnerability: new FormControl(node.vulnerability, Validators.required),
      x_pos: new FormControl(node.x_pos, Validators.required),
      y_pos: new FormControl(node.y_pos, Validators.required),
      // set to false and disable if random high value nodes are to be set on network
      high_value_node: new FormControl(node.high_value_node, Validators.required),
      entry_node: new FormControl(node.entry_node, Validators.required),
    });

    // update form group
    this.nodePropertiesFormGroupSubject.next(this._nodePropertiesFormGroup);
  }

  /**
   * Function that triggers the persisting of the updated node properties
  */
  public updateNodeProperties(node: Node): void {
    // update
    this.networkService.editNodeDetails(node);
  }

  /**
   * Update input fields with the new node
   * @param evt
   */
  public updateNodePositions(val: { id: string, position: { x: number, y: number } }): void {
    // only need to care if the node being dragged is displayed
    if (!val || !(val.id == this.currentNode?.uuid)) {
      return;
    }

    // update x pos and y pos
    this._nodePropertiesFormGroup.get('x_pos').setValue(Number.parseFloat(val.position.x.toFixed()));
    this._nodePropertiesFormGroup.get('y_pos').setValue(Number.parseFloat(val.position.y.toFixed()));
  }
}
