import { NO_ERRORS_SCHEMA } from '@angular/core';
import { ComponentFixture, fakeAsync, TestBed, tick } from '@angular/core/testing';
import { test_network } from '../../testing/test-network';
import { NODE_KEY_CONFIG } from '../app.tokens';
import { CytoscapeService } from '../services/cytoscape/cytoscape.service';
import { ImportService } from '../services/export-import/import.service';

import { NetworkViewComponent } from './network-view.component';

describe('NetworkViewComponent', () => {
  let component: NetworkViewComponent;
  let fixture: ComponentFixture<NetworkViewComponent>;

  let cytoscapeServiceStub: any = {
    init: () => { }
  }

  let importServiceStub = {
    loadNetworkFromWindow: () => { },
    loadFile: () => { }
  }

  let stubNodeKeyConfig = []

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      declarations: [NetworkViewComponent],
      providers: [
        { provide: CytoscapeService, cytoscapeServiceStub },
        { provide: ImportService, useValue: importServiceStub },
        { provide: NODE_KEY_CONFIG, useValue: stubNodeKeyConfig }
      ],
      schemas: [
        NO_ERRORS_SCHEMA
      ]
    })
      .compileComponents();

    fixture = TestBed.createComponent(NetworkViewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });

  it('should call the import service when a load file event is triggered', () => {
    const spy = spyOn(component['importService'], 'loadFile');

    component.loadFile({});
    expect(spy).toHaveBeenCalled();
  });

  it('should process the network from the global window object', fakeAsync(() => {
    (<any>window).NETWORK = test_network;

    const spy = spyOn<any>(component['importService'], 'loadNetworkFromWindow').and.callFake(() => { });
    component.ngAfterViewInit();
    tick(200);
    expect(spy).toHaveBeenCalled();
  }));

  describe('METHOD: listenToNetworkChange', () => {
    it('should load the network if the networkUpdate event is triggered', fakeAsync(() => {
      const spy = spyOn<any>(component['importService'], 'loadNetworkFromWindow').and.callFake(() => { });
      document.dispatchEvent(new CustomEvent('networkUpdate', { detail: JSON.stringify(test_network) }));
      component.ngAfterViewInit();
      tick(200);
      expect(spy).toHaveBeenCalled();
    }));
  });

  describe('METHOD: listenToNetworkSettingsChange', () => {
    it('should process network settings changes', () => {
      const spy = spyOn(component['interactionService'], 'processNetworkSettingsChanges');
      const formData = new FormData();
      formData.append('_operation', 'UPDATE_NETWORK_DETAILS');
      component['listenToNetworkSettingsChange']({ detail: formData })
      expect(spy).toHaveBeenCalled();
    });

    it('should process network metadata changes', () => {
      const spy = spyOn(component['interactionService'], 'processNetworkMetadataChanges');
      const formData = new FormData();
      formData.append('_operation', 'UPDATE_NETWORK_METADATA');
      component['listenToNetworkSettingsChange']({ detail: formData })
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: listenToSelectedNodeListItem', () => {
    it('should process the selected node event', () => {
      const spy = spyOn(component['interactionService'], 'processNodeSelected');
      component['listenToSelectedNodeListItem']({});
      expect(spy).toHaveBeenCalled();
    });
  });

  describe('METHOD: listenToNodeListItemDelete', () => {
    it('should process the delete node event', () => {
      const spy = spyOn(component['interactionService'], 'processNodeDelete');
      component['listenToNodeListItemDelete']({});
      expect(spy).toHaveBeenCalled();
    });
  });
});
