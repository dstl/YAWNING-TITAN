import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { debounceTime, Subscription, tap } from 'rxjs';
import { Node } from '../network-class/network-interfaces';
import { roundNumber } from '../utils/utils';
import { NodePropertiesService } from './node-properties.service';

@Component({
  selector: 'app-node-properties',
  templateUrl: './node-properties.component.html',
  styleUrls: ['./node-properties.component.scss']
})
export class NodePropertiesComponent implements OnInit, OnChanges, OnDestroy {

  @Input('node') node: Node = null;

  @Output() close = new EventEmitter();

  public formGroup: FormGroup = null;

  public vulnerabilityVal = 0;

  private vulnerabilityChangeListener: Subscription;

  constructor(
    private nodePropertiesService: NodePropertiesService
  ) {
  }

  ngOnInit() {
    this.nodePropertiesService.nodePropertiesFormGroupSubject.subscribe(res => {
      this.formGroup = res;

      // update node when there are changes
      this.formGroup.valueChanges
        .subscribe(() => {
          this.vulnerabilityVal = roundNumber(this.formGroup.get('vulnerability')?.value);
          this.updateNode();
        });
    });
  }

  ngOnChanges(changes: SimpleChanges) {
    // do nothing if the previous value is the same that the current
    if (changes?.node?.currentValue == changes?.node?.previousValue) {
      return;
    }

    // load the details of the new selected node
    this.nodePropertiesService.loadDetails(this.node);
  }

  ngOnDestroy(): void {
    if (!!this.vulnerabilityChangeListener) {
      this.vulnerabilityChangeListener.unsubscribe();
    }
  }

  /**
   * Persists the node properties that the user has changed
   */
  public updateNode(): void {
    if (!this.formGroup?.valid) {
      return;
    }

    const nodeProperty = {
      uuid: this.formGroup.get('uuid')?.value,
      name: this.formGroup.get('name')?.value,
      x_pos: roundNumber(this.formGroup.get('x_pos')?.value),
      y_pos: roundNumber(this.formGroup.get('y_pos')?.value),
      high_value_node: this.formGroup.get('high_value_node')?.value,
      entry_node: this.formGroup.get('entry_node')?.value,
      vulnerability: roundNumber(this.formGroup.get('vulnerability')?.value, 6),
    }

    this.nodePropertiesService.updateNodeProperties(nodeProperty);
  }

  /**
   * Triggers the event that closes the sidenav
   */
  public closeSideNav(): void {
    this.close.emit();
  }

  /**
   * Show the vulnerability slider if true
   * @returns
   */
  public showVulnerabilitySlider(): boolean {
    return !this.nodePropertiesService.randomVulnerabilitiesOnReset();
  }

  /**
   * Show the entry node toggle if true
   * @returns
   */
  public showEntryNodeToggle(): boolean {
    return !this.nodePropertiesService.randomEntryNodesOnReset();
  }

  /**
   * Show the high value node toggle if true
   * @returns
   */
  public showHighValueNodeToggle(): boolean {
    return !this.nodePropertiesService.randomHighValueNodesOnReset();
  }
}
