import { Injectable } from '@angular/core';
import { CytoscapeService } from '../cytoscape/cytoscape.service';

@Injectable({
  providedIn: 'root'
})
export class InteractionService {

  /**
   * boolean flag used to keep track of whether or not a user is typing in an input field
  */
  private inputFocus: boolean;

  /**
   * Service used to keep track of key inputs and interaction with the user interface
   */
  constructor(
    private cytoscapeService: CytoscapeService
  ) {
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

    switch(event.key) {
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
    this.cytoscapeService.deleteItem();
  }
}
