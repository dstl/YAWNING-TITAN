import { HttpClient } from '@angular/common/http';
import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { of, Subject } from 'rxjs';
import { AppComponent } from './app.component';
import { DJANGO_SAVE_URL } from './app.tokens';

import { CytoscapeService } from './services/cytoscape/cytoscape.service';
import { ElementType } from './services/cytoscape/graph-objects';
import { InteractionService } from './services/interaction/interaction.service';
import { Network } from './network-class/network';
import { test_network } from '../testing/test-network';
import { NetworkService } from './network-class/network.service';

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

  const networkServiceStub: any = {
    networkObservable: new Subject(),
    getNodeById: () => '',
    getNetworkJson: () => { }
  }

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [AppComponent],
      providers: [
        { provide: CytoscapeService, useValue: stubCytoscapeService },
        { provide: InteractionService, useValue: stubIteractionService },
        { provide: NetworkService, useValue: networkServiceStub },
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

  it('should not try to update the network if the document is locked', fakeAsync(() => {
    component.ngOnInit();
    const spy = spyOn<any>(component, 'updateNetwork');
    tick(1100);

    const network = new Network(test_network);
    networkServiceStub.networkObservable.next(network)
    tick(1100);
    expect(spy).not.toHaveBeenCalled();
  }));

  it('should update the network if the document is not locked', fakeAsync(() => {
    component.ngOnInit();
    const spy = spyOn<any>(component, 'updateNetwork');
    tick(1100);

    const network = new Network(test_network);
    network.documentMetadata.locked = false;
    networkServiceStub.networkObservable.next(network)
    tick(1100);
    expect(spy).toHaveBeenCalled();
  }));

  describe('METHOD: updateNetwork', () => {
    it('should send the correct post body', () => {
      component['saveUrl'] = '';
      const testStr = JSON.stringify(test_network);
      spyOn(component['networkService'], 'getNetworkJson').and.returnValue(test_network as any)
      const spy = spyOn(component['http'], 'post').and.returnValue(of());

      component['updateNetwork']();

      expect(spy).toHaveBeenCalledWith('', testStr);
    });
  });

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
