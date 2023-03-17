/// <reference types="cypress" />
// ***********************************************
// This example commands.ts shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add('login', (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands.add('drag', { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands.add('dismiss', { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite('visit', (originalFn, url, options) => { ... })
//
let testName;

import { v4 as uuid } from 'uuid';

/**
 * Function used to create an empty network for tests
 */
export function openEmptyNetwork() {
  // get to the network editor page
  cy.visit(`${Cypress.env('TEST_URL')}${Cypress.env('NETWORKS_PATH')}`);

  // create new network
  cy.get('#create').click();
  testName = uuid()
  cy.get('#create-dialogue > [data-cy="new-item-name-input"]').type(testName);
  cy.get('.custom-network').click();

  cy.wait(500)
    .get('[data-cy="cytoscape-canvas"]');
}

/**
 * Function used to clean up networks created during tests
 * @param networkId
 */
export function cleanUpNetwork(networkId?: string) {
  // go to the networks and delete what was created
  cy.visit(`${Cypress.env('TEST_URL')}${Cypress.env('NETWORKS_PATH')}`);
  cy.get('.head').should('be.visible');

  // find the correct item and delete
  cy.get(`[data-item-name="${networkId ? networkId : testName}"] > .icons > .delete`).click();
  cy.contains('Delete network').click();
}

/**
 * Deletes a game mode with the given id
 * @param gameModeId
 */
export function cleanUpGameMode(gameModeId?: string) {
  // go to the networks and delete what was created
  cy.visit(`${Cypress.env('TEST_URL')}${Cypress.env('GAME_MODE_PATH')}`);
  cy.get('.head').should('be.visible');

  // find the correct item and delete
  cy.get(`[data-item-name="${gameModeId ? gameModeId : testName}"] > .icons > .delete`).click();
  cy.contains('Delete game mode').click();
}

/**
 * Function that fails the test if the element exists and is visible
 * @param selector
 */
export function existsButNotVisible(selector: string) {
  cy.wait(500) // wait for things to update
    .get(selector).each((el) => {
      // check if the client height and width is more than 0
      if (el[0].clientHeight > 0 && el[0].clientWidth > 0) {
        // element is visible
        throw new Error(`${selector} is visible`);
      }
    })
}

Cypress.Commands.add('openEmptyNetwork', openEmptyNetwork);
Cypress.Commands.add('cleanUpNetwork', cleanUpNetwork);
Cypress.Commands.add('cleanUpGameMode', cleanUpGameMode);
Cypress.Commands.add('existsButNotVisible', existsButNotVisible);

declare global {
  namespace Cypress {
    interface Chainable {
      openEmptyNetwork: typeof openEmptyNetwork
      cleanUpNetwork: typeof cleanUpNetwork
      cleanUpGameMode: typeof cleanUpGameMode
      existsButNotVisible: typeof existsButNotVisible
    }
  }
}

