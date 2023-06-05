import { LayoutLabelPipeDirective } from './layout-label-pipe.directive';

describe('LayoutLabelPipeDirective', () => {
  let directive: LayoutLabelPipeDirective;

  beforeEach(() => {
    directive = new LayoutLabelPipeDirective();
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  it('should perform the correct transforms', () => {
    expect(directive.transform('test')).toBe('Test');
    expect(directive.transform('test_string')).toBe('Test String');
    expect(directive.transform('test____string')).toBe('Test String');
    expect(directive.transform('test-string')).toBe('Test String');
    expect(directive.transform('test-----string')).toBe('Test String');
    expect(directive.transform('test-_string')).toBe('Test String');
  });
});
