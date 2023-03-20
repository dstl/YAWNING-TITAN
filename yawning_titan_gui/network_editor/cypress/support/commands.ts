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
let testId;

import { v4 as uuid } from 'uuid';

export function openEmptyNetwork() {
  // get to the network editor page
  cy.visit(`${Cypress.env('TEST_URL')}${Cypress.env('NETWORKS_PATH')}`);

  // create new network
  cy.get('#create').click();
  testId = uuid()
  cy.get('#create-dialogue > [data-cy="new-item-name-input"]').type(testId);
  cy.get('.custom-network').click();
}

export function cleanUpNetwork(networkId?: string) {
  // go to the networks and delete what was created
  cy.visit(`${Cypress.env('TEST_URL')}${Cypress.env('NETWORKS_PATH')}`);
  cy.get('.head').should('be.visible');

  // find the correct item and delete
  cy.get(`[data-item-name="${networkId ? networkId : testId}"] > .icons > .delete`).click();
  cy.contains('Delete network').click();
}

Cypress.Commands.add('openEmptyNetwork', openEmptyNetwork);
Cypress.Commands.add('cleanUpNetwork', cleanUpNetwork);

declare global {
  namespace Cypress {
    interface Chainable {
      openEmptyNetwork: typeof openEmptyNetwork
      cleanUpNetwork: typeof cleanUpNetwork
    }
  }
}
