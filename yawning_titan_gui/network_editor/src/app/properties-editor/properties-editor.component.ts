import { Component, Input, OnChanges, OnInit, SimpleChanges } from '@angular/core';
import { Node } from '../network-class/network-interfaces';
import { PropertiesEditorService } from './properties-editor.service';

@Component({
  selector: 'app-properties-editor',
  templateUrl: './properties-editor.component.html',
  styleUrls: ['./properties-editor.component.scss']
})
export class PropertiesEditorComponent implements OnInit, OnChanges {

  @Input('nodeId') nodeId: string = null;

  public currentNode: Node;

  constructor(
    private propertiesEditorService: PropertiesEditorService
  ) { }

  ngOnInit() {
    this.propertiesEditorService.nodeDetailsSubject?.subscribe(node => this.currentNode = node)
  }

  ngOnChanges(changes: SimpleChanges) {
    // do nothing if the previous value is the same that the current
    if (changes?.nodeId?.currentValue == changes?.nodeId?.previousValue) {
      return;
    }

    // load the details of the new selected node
    this.propertiesEditorService.loadDetails(this.nodeId);
  }

}
