import { Directive, HostListener } from '@angular/core';
import { InteractionService } from 'src/app/services/interaction/interaction.service';

@Directive({
  selector: '[appFocusTracking]'
})
export class FocusTrackingDirective {
  constructor(
    private interactionService: InteractionService
  ) {}

  @HostListener('focus', ['$event']) onFocus() {
    this.interactionService.setInputFocusStatus(true);
  }

  @HostListener('blur', ['$event']) onBlur() {
    this.interactionService.setInputFocusStatus(false);
  }
}
