import { Component, Inject } from '@angular/core';
import { MAT_SNACK_BAR_DATA, MatSnackBarRef } from '@angular/material/snack-bar';
import { Network } from 'src/app/network-class/network';
import { NetworkService } from 'src/app/network-class/network.service';

@Component({
  selector: 'app-undo-layout',
  templateUrl: './undo-layout.component.html',
  styleUrls: ['./undo-layout.component.scss']
})
export class UndoLayoutComponent {
  constructor(
    @Inject(MAT_SNACK_BAR_DATA) public data: any,
    private networkService: NetworkService,
    private snackBarRef: MatSnackBarRef<UndoLayoutComponent>
  ) { }

  /**
   * Close the snackbar
   */
  public dismissSnackbar(): void {
    this.snackBarRef.dismiss();
  }

  /**
   * Undo the layout that was applied
   */
  public undoLayout(): void {
    const network = new Network(this.data);
    this.networkService.loadNetwork(network);
    this.snackBarRef.dismiss();
  }
}
