import { HttpClient } from '@angular/common/http';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { AppComponent } from './app.component';
import { DJANGO_SAVE_URL } from './app.tokens';

import { CytoscapeService } from './services/cytoscape/cytoscape.service';
import { ElementType } from './services/cytoscape/graph-objects';
import { InteractionService } from './services/interaction/interaction.service';

describe('AppComponent', () => {
  let component: AppComponent;
  let fixture: ComponentFixture<AppComponent>;

  const stubCytoscapeService = {
    selectedElementEvent: new Subject()
  }
  const stubIteractionService = {
    keyInput: () => { },
    selectedItem: new Subject()
  }

  const httpStub = {
    post: () => of()
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      providers: [
        { provide: CytoscapeService, useValue: stubCytoscapeService },
        { provide: InteractionService, useValue: stubIteractionService },
        { provide: DJANGO_SAVE_URL, useValue: '' },
        { provide: HttpClient, useValue: httpStub }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(AppComponent);
    component = fixture.componentInstance;
    component.sidenav = { close: () => { }, open: () => { } } as any;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call toggleNodePropertiesSidenav when the selectedElement is changed', fakeAsync(() => {
    const spy = spyOn<any>(component, 'toggleNodePropertiesSidenav').and.callFake(() => { });

    stubIteractionService.selectedItem.next({});

    tick();
    expect(spy).toHaveBeenCalled();
  }));

  describe('METHOD: handleKeyboardEvent', () => {
    it('should trigger the keyInput method in the interaction service', () => {
      const spy = spyOn(component, 'handleKeyboardEvent');
      component.handleKeyboardEvent(null);
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: toggleNodePropertiesSidenav', () => {
    it('should do nothing if the selected element is an edge', () => {
      const openSpy = spyOn(component.sidenav, 'open');

      component['toggleNodePropertiesSidenav']({ id: 'test', type: ElementType.EDGE });

      expect(openSpy).not.toHaveBeenCalled();
    });

    it('should open the sidenav if the selected element is a node', () => {
      const openSpy = spyOn(component.sidenav, 'open');
      spyOn(component['networkService'], 'getNodeById').and.returnValue({} as any);

      component['toggleNodePropertiesSidenav']({ id: 'test', type: ElementType.NODE });

      expect(openSpy).toHaveBeenCalled();
    });
  });
});
