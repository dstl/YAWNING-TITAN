import { Injectable } from '@angular/core';
import * as cytoscape from 'cytoscape';
import { Observable, Subject } from 'rxjs';
import { NetworkService } from 'src/app/network-class/network.service';
import { CytoscapeService } from '../cytoscape/cytoscape.service';
import { ElementType, SelectedGraphRef } from '../cytoscape/graph-objects';

@Injectable({
  providedIn: 'root'
})
export class InteractionService {

  /**
   * boolean flag used to keep track of whether or not a user is typing in an input field
  */
  private inputFocus: boolean;

  /**
   * Keeps track of the currently selected node
   */
  private _selectedItem: SelectedGraphRef = null;
  private selectedItemSubject = new Subject<SelectedGraphRef>();
  get selectedItem(): Observable<SelectedGraphRef> {
    return this.selectedItemSubject.asObservable();
  }

  /**
   * Trigger updates when a node is dragged
   */
  private dragSubject = new Subject<{ id: string, position: { x: number, y: number } }>();
  get dragEvent(): Observable<{ id: string, position: { x: number, y: number } }> {
    return this.dragSubject.asObservable();
  }

  /**
   * Service used to keep track of key inputs and interaction with the user interface
   */
  constructor(
    private networkService: NetworkService,
    private cytoscapeService: CytoscapeService
  ) {
    this.cytoscapeService.doubleClickEvent.subscribe((event) => this.handleDoubleClick(event));
    this.cytoscapeService.singleClickEvent.subscribe((event) => this.handleSingleClick(event));
    this.cytoscapeService.dragEvent.subscribe((event) => this.handleDrag(event));
  }

  /**
   * Handle double click inputs
   * @param evt
   */
  private handleDoubleClick(evt: cytoscape.EventObject): void {
    // check if a node or edge is being double clicked
    if (Array.isArray(evt.target) || !!evt.target.length) {
      return;
    }

    // create a new node
    this.networkService.addNode(evt.position.x, evt.position.y);
  }

  /**
   * Handle single click inputs
   * @param evt
   */
  private handleSingleClick(evt: cytoscape.EventObject): void {
    // check if target is a node
    if (evt.target?.isNode && evt.target?.isNode()) {
      this.handleNodeCreation(evt);
    }

    // if target is neither node or edge, set selected to null
    if (!evt || !evt.target || !evt.target.isNode || !evt.target.isEdge) {
      // clicked on background
      this._selectedItem = null;
      this.selectedItemSubject.next(this._selectedItem);
      return;
    }

    // set element as selected
    this._selectedItem = {
      id: evt.target?.id(),
      type: evt.target.isNode() ? ElementType.NODE : ElementType.EDGE
    }
    this.selectedItemSubject.next(this._selectedItem);
  }

  /**
   * Handle node creation action
   * @param evt
   * @returns
   */
  private handleNodeCreation(evt: cytoscape.EventObject) {
    if (this._selectedItem?.type == ElementType.NODE) {
      // create an edge between 2 nodes
      const res = this.networkService.addEdge({
        edgeId: null,
        nodeA: this._selectedItem.id,
        nodeB: evt.target?.id()
      });

      // check if successful
      if (!res) {
        return;
      }

      this._selectedItem = null;
      this.selectedItemSubject.next(this._selectedItem);
    }
  }

  /**
     * Handle click and drag inputs
     * @param evt
     */
  private handleDrag(evt: cytoscape.EventObject): void {
    const node = this.networkService.getNodeById(evt?.target?.id());
    node.x_pos = evt.target.position().x;
    node.y_pos = evt.target.position().y;
    this.networkService.editNodeDetails(node);
    this.dragSubject.next({
      id: node.uuid,
      position: { x: node.x_pos, y: node.y_pos }
    })
  }

  /**
   * Function that is used to update if the user is typing in input fields or not
   * @param focused
   */
  public setInputFocusStatus(focused: boolean) {
    this.inputFocus = focused;
  }

  /**
   * Function that is used to handle key inputs
   * @param event
   */
  public keyInput(event: KeyboardEvent) {
    // if the user is focused on an input, do nothing
    if (this.inputFocus) {
      return;
    }

    // handle shift key inputs
    if (event.shiftKey) {
      this.handleShiftKeyInput(event);
    }

    if (event.ctrlKey) {
      this.handleControlKeyInput(event);
    }

    switch (event.key) {
      case 'Delete':
      case 'Backspace':
        this.deleteItem();

      default:
        break;
    }
  }

  private handleShiftKeyInput(event: KeyboardEvent): void {

  }

  private handleControlKeyInput(event: KeyboardEvent): void {

  }

  /**
   * Trigger an element deletion in cytoscape
   */
  private deleteItem(): void {
    this.networkService.removeItem(this._selectedItem);
  }
}
