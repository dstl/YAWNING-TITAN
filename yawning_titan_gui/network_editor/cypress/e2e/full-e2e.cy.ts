import { v4 as uuid } from 'uuid';

describe('End To End', () => {
  it('should be able to set up and run a full end to end run of Yawning Titan', () => {
    // game mode id
    const gameModeId = uuid();
    const networkId = uuid();

    /**
     * Create game mode copy from default
     */
    cy.get('[data-cy="menu-manage-game-modes"]').click();

    // click create from in default game mode list item
    cy.get('[data-item-name="Default Game Mode"]').find('.create-from').click();

    cy.get('#create-from-dialogue > [data-cy="new-item-name-input"]').type(gameModeId);

    cy.get('#create-from-dialogue').find('.btn').contains('Create game mode').click();

    // should open the game mode editor
    cy.get('#config-forms').should('be.visible');

    // return to home page
    cy.get('[data-cy="toolbar-home"]').click();

    /**
     * Create network copy from default
     */

    // open networks
    cy.get('[data-cy="menu-manage-networks"]').click();

    // click on create from
    cy.get('[data-item-name="Default 18-node network"]').find('.create-from').click();

    cy.get('#create-from-dialogue > [data-cy="new-item-name-input"]').type(networkId);

    cy.get('#create-from-dialogue').find('.btn').contains('Create network').click();

    cy.wait(500)
      .get('[data-cy="cytoscape-canvas"]').should('be.visible');

    // return to home page
    cy.get('[data-cy="toolbar-home"]').click();

    /**
     * Yawning Titan Run
     */
    // open page
    cy.get('[data-cy="menu-run-yt"]').click();

    /**
     * CLEAN UP
     */
    cy.cleanUpGameMode(gameModeId);
    cy.cleanUpNetwork(networkId);
  });
})
