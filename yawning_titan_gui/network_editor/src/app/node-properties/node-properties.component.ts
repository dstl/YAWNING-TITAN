import { Component, Input, OnChanges, OnDestroy, OnInit, SimpleChanges } from '@angular/core';
import { FormGroup } from '@angular/forms';
import { Subscription } from 'rxjs';
import { PropertiesEditorService } from './node-properties.service';

@Component({
  selector: 'app-node-properties',
  templateUrl: './node-properties.component.html',
  styleUrls: ['./node-properties.component.scss']
})
export class NodePropertiesComponent implements OnInit, OnChanges, OnDestroy {

  @Input('nodeId') nodeId: string = null;

  public formGroup: FormGroup = null;

  public vulnerabilityVal = 0;

  private vulnerabilityChangeListener: Subscription;

  constructor(
    private propertiesEditorService: PropertiesEditorService
  ) {
  }

  ngOnInit() {
    this.propertiesEditorService.nodePropertiesFormGroupSubject.subscribe(res => {
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
    if (changes?.nodeId?.currentValue == changes?.nodeId?.previousValue) {
      return;
    }

    // load the details of the new selected node
    this.propertiesEditorService.loadDetails(this.nodeId);
  }

  ngOnDestroy(): void {
    if (!!this.vulnerabilityChangeListener) {
      this.vulnerabilityChangeListener.unsubscribe();
    }
  }

  public isFormValid(): boolean {
    return !!this.formGroup && this.formGroup.valid;
  }

  /**
   * Persists the node properties that the user has changed
   */
  public updateNode(): void {
    this.propertiesEditorService.updateNodeProperties();
  }
}
