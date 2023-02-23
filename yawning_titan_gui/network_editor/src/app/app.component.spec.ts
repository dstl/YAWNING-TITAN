import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { Subject } from 'rxjs';
import { AppComponent } from './app.component';

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
    keyInput: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      providers: [
        { provide: CytoscapeService, useValue: stubCytoscapeService },
        { provide: InteractionService, useValue: stubIteractionService }
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

    stubCytoscapeService.selectedElementEvent.next({});

    tick();
    expect(spy).toHaveBeenCalled();
  }));

  describe('METHOD: toggleNodePropertiesSidenav', () => {
    it('should do nothing if the selected element is an edge', () => {
      const openSpy = spyOn(component.sidenav, 'open');

      component['toggleNodePropertiesSidenav']({ id: 'test', type: ElementType.EDGE });

      expect(openSpy).not.toHaveBeenCalled();
    });

    it('should open the sidenav if the selected element is a node', () => {
      const openSpy = spyOn(component.sidenav, 'open');

      component['toggleNodePropertiesSidenav']({ id: 'test', type: ElementType.NODE });

      expect(openSpy).toHaveBeenCalled();
    });
  });
});
