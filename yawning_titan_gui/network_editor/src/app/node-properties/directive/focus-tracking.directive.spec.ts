import { FocusTrackingDirective } from './focus-tracking.directive';

describe('FocusTrackingDirective', () => {
  const interactionServiceStub: any = {

  }

  let directive: FocusTrackingDirective;

  beforeEach(() => {
    directive = new FocusTrackingDirective(interactionServiceStub);
  })

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });
});
