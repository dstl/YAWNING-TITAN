import { Injectable } from '@angular/core';
import { Network } from 'src/app/network-class/network';
import { NetworkSettings, RandomEntryNodePreference, RandomHighValueNodePreference } from 'src/app/network-class/network-interfaces';
import { NetworkService } from '../../network-class/network.service';

@Injectable({
  providedIn: 'root'
})
export class ImportService {

  constructor(
    private networkService: NetworkService
  ) { }

  /**
   * Converts the network settings update into an object the angular side of
   * the network editor can process
   * @param update
   */
  public processNetworkSettingsChanges(update: any): void {
    const processedVal: NetworkSettings = {
      entryNode: {
        set_random_entry_nodes: update?.set_random_entry_nodes == 'on' ? true : false,
        num_of_random_entry_nodes: Number(update?.num_of_random_entry_nodes),
        random_entry_node_preference: update?.random_entry_node_preference as RandomEntryNodePreference
      },
      highValueNode: {
        set_random_high_value_nodes: update?.set_random_high_value_nodes == 'on' ? true: false,
        num_of_random_high_value_nodes: Number(update?.num_of_random_high_value_nodes),
        random_high_value_node_preference: update?.random_high_value_node_preference as RandomHighValueNodePreference
      },
      vulnerability: {
        set_random_vulnerabilities: update?.set_random_vulnerabilities == 'on' ? true : false,
        node_vulnerability_upper_bound: Number(update?.node_vulnerability_upper_bound),
        node_vulnerability_lower_bound: Number(update?.node_vulnerability_lower_bound),
      }
    };

    this.networkService.updateNetworkSettings(processedVal);
  }

  /**
   * Parse the dropped file and load the network if the file is valid
   * @param $event
   *
   * @returns
   */
  public async loadFile($event): Promise<void> {
    // read first file
    if (!$event || !$event[0]) {
      return;
    }

    try {
      const content = await ($event[0] as File).text();
      const network = new Network(JSON.parse(content));

      this.networkService.loadNetwork(network);
    } catch (e) {
      throw new Error("Unable to parse file", e);
    }
  }

  /**
   * Load the JSON passed from the window.NETWORK variable that is loaded from the Django side
   * @param windowNetwork
   */
  public loadNetworkFromWindow(windowNetwork: any): void {
    // read first file
    if (!windowNetwork) {
      return;
    }

    try {
      const network = new Network(JSON.parse(windowNetwork));
      this.networkService.loadNetwork(network);
    } catch (e) {
      throw new Error("Unable to parse JSON", e);
    }
  }
}
