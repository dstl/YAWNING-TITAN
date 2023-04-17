import { fakeAsync, tick } from '@angular/core/testing';
import { FileDragDropDirective } from './file-drag-drop.directive';

describe('FileDragDropDirective', () => {
  let directive: FileDragDropDirective;

  const eventStub = {
    preventDefault: () => { },
    stopPropagation: () => { },
    dataTransfer: {
      files: ['test']
    }
  }

  beforeEach(() => {
    directive = new FileDragDropDirective();
  });

  it('should create an instance', () => {
    expect(directive).toBeTruthy();
  });

  it('should set fileOver to true', () => {
    expect(directive.fileOver).toBeUndefined();
    directive.onDragOver(eventStub);
    expect(directive.fileOver).toBeTruthy()
  });

  it('should set fileOver to false', () => {
    expect(directive.fileOver).toBeUndefined();
    directive.onDragLeave(eventStub);
    expect(directive.fileOver).toBeFalsy()
  });

  it('should emit that files have been dropped onto the component', fakeAsync(() => {
    expect(directive.fileOver).toBeUndefined();
    directive.ondrop(eventStub);
    tick();

    directive.fileDropped.subscribe(() => {
      expect(directive.fileOver).toBeFalsy();
    });
  }));
});
