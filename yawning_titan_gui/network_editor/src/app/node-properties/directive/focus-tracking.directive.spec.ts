import { FocusTrackingDirective } from './focus-tracking.directive';

describe('FocusTrackingDirective', () => {
  const interactionServiceStub: any = {
    setInputFocusStatus: () => { }
  }

  let directive: FocusTrackingDirective;

  beforeEach(() => {
    directive = new FocusTrackingDirective(interactionServiceStub);
  })

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  describe('METHOD: onFocus', () => {
    it('should set interactionService focus status to true', () => {
      const spy = spyOn(directive['interactionService'], 'setInputFocusStatus').and.callFake(() => { });
      directive.onFocus();
      expect(spy).toHaveBeenCalledWith(true);
    });
  });

  describe('METHOD: onBlur', () => {
    it('should set interactionService focus status to false', () => {
      const spy = spyOn(directive['interactionService'], 'setInputFocusStatus').and.callFake(() => { });
      directive.onBlur();
      expect(spy).toHaveBeenCalledWith(false);
    });
  });
});
