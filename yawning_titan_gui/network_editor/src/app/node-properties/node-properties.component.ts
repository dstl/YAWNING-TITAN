import { Component, EventEmitter, Input, OnChanges, OnDestroy, OnInit, Output, SimpleChanges } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { Node } from '../network-class/network-interfaces';
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

      this.vulnerabilityVal = this.formGroup.get('vulnerability').value;

      this.vulnerabilityChangeListener = this.formGroup.get('vulnerability').valueChanges
        .subscribe(val => {
          this.vulnerabilityVal = val;
        })
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
    this.nodePropertiesService.updateNodeProperties();
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
